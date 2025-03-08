import ast
import json
import os
import re
import subprocess
from collections import defaultdict


# ----------------------------------------
# Utility Functions
# ----------------------------------------
def parse_python_file(file_path):
    """Reads a Python file and returns its AST tree."""
    with open(file_path, "r", encoding="utf-8") as f:
        return ast.parse(f.read())

def run_radon_analysis(command, file_path):
    """Executes radon analysis and returns parsed JSON output."""
    ansi = r'\x1b\[[0-9;]*m'  # Regex to remove ANSI escape sequences
    result = subprocess.run(["radon", command, file_path, "-j"], capture_output=True, text=True)
    return json.loads(re.sub(ansi, '', result.stdout.strip()))


def extract_class_info(tree):
    """
    Extracts class, method, and inheritance information.
    Returns:
        - class_methods: Dictionary mapping class names to their methods.
        - class_hierarchy: Dictionary mapping class names to their base classes.
    """
    class_methods = {}  # Methods per class
    class_hierarchy = {}  # Inheritance

    # Collect class definitions and methods
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
            bases = [base.id for base in node.bases if isinstance(base, ast.Name)]

            class_methods[class_name] = methods
            class_hierarchy[class_name] = bases

    return class_methods, class_hierarchy


def extract_class_dependencies(tree, class_methods, class_hierarchy):
    """
    Extracts class dependencies for each class in the AST.
    Returns:
        - class_dependencies: Dictionary mapping each class to its unique dependencies.
    """
    class_dependencies = defaultdict(set)
    defined_classes = set(class_methods.keys())  # Defined class names
    imported_classes = set()  # Imported class names
    special_dependencies = {"game": "Game", "player": "Player"}  # Mapping for special dependencies

    # Identify imported classes
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported_classes.update(alias.name for alias in node.names)

    # Identify dependencies for each class
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            current_class = node.name  # Track the class being analyzed

            if current_class in class_hierarchy:
                class_dependencies[current_class].update(class_hierarchy[current_class])

            for sub_node in ast.walk(node):  # Only analyze this class' subtree
                # Detect function and method calls affecting dependencies
                if isinstance(sub_node, ast.Call):
                    called_class = None
                    if isinstance(sub_node.func, ast.Name):  # Direct function call
                        called_class = sub_node.func.id
                    elif isinstance(sub_node.func, ast.Attribute) and isinstance(sub_node.func.value, ast.Name):
                        called_class = sub_node.func.value.id

                    if called_class and (called_class in defined_classes or called_class in imported_classes):
                        class_dependencies[current_class].add(called_class)

                # Detect attribute access that references other classes
                elif isinstance(sub_node, ast.Attribute):
                    if isinstance(sub_node.value, ast.Name) and sub_node.value.id == "self":
                        accessed_var = sub_node.attr
                        if accessed_var in special_dependencies:
                            class_dependencies[current_class].add(special_dependencies[accessed_var])

                    elif (isinstance(sub_node.value, ast.Attribute) and
                          isinstance(sub_node.value.value, ast.Name) and
                          sub_node.value.value.id == "self"):
                        root_var = sub_node.value.attr
                        final_attr = sub_node.attr
                        if root_var in special_dependencies and final_attr == "player":
                            class_dependencies[current_class].add("Player")

                    elif isinstance(sub_node.value,
                                    ast.Name) and sub_node.value.id in defined_classes | imported_classes:
                        class_dependencies[current_class].add(sub_node.value.id)

    for class_name in defined_classes:
        if class_name not in class_dependencies:
            class_dependencies[class_name] = set()

    return class_dependencies


# ----------------------------------------
# 1️⃣ WMC (Weighted Methods per Class)
# ----------------------------------------
def calculate_wmc(class_methods):
    """
    Calculates the average Weighted Methods per Class (WMC) for a file.
    """
    wmc_values = [len(methods) for methods in class_methods.values()]
    avg_wmc = sum(wmc_values) / len(wmc_values)
    return round(avg_wmc, 2)


# ----------------------------------------
# 2️⃣ CBO (Coupling Between Objects)
# ----------------------------------------
def calculate_cbo(class_dependencies):
    """Calculates the average Coupling Between Objects (CBO) for a file."""
    if not class_dependencies:
        return 0
    cbo_values = [len(dep) for dep in class_dependencies.values()]
    avg_cbo = sum(cbo_values) / len(cbo_values)
    return round(avg_cbo, 2)


# ----------------------------------------
# 3️⃣ LCOM (Lack of Cohesion in Methods)
# ----------------------------------------
def calculate_lcom(tree):
    """Calculates Lack of Cohesion in Methods (LCOM)."""
    method_attributes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    accessed_attributes = {stmt.attr for stmt in ast.walk(item)
                                           if isinstance(stmt, ast.Attribute) and isinstance(stmt.value, ast.Name) and stmt.value.id == "self"}
                    method_attributes.append(accessed_attributes)

    num_methods = len(method_attributes)
    if num_methods < 2:
        return 0  # LCOM is 0 if fewer than 2 methods exist

    non_cohesive_pairs = sum(1 for i in range(num_methods) for j in range(i + 1, num_methods)
                             if method_attributes[i].isdisjoint(method_attributes[j]))
    total_pairs = num_methods * (num_methods - 1) / 2

    return round(non_cohesive_pairs / total_pairs if total_pairs > 0 else 0, 2)


# ----------------------------------------
# 4️⃣ DIT (Depth of Inheritance Tree)
# ----------------------------------------
def calculate_dit(class_hierarchy):
    """Calculates the average Depth of Inheritance Tree (DIT) for a file."""
    def find_depth(cls, depth=0):
        if cls not in class_hierarchy or not class_hierarchy[cls]:
            return depth
        return max(find_depth(base, depth + 1) for base in class_hierarchy[cls])

    dit_values = [find_depth(cls) for cls in class_hierarchy]
    avg_dit = sum(dit_values) / len(dit_values)

    return round(avg_dit, 2)


# ----------------------------------------
# 5️⃣ Maintainability Index (MI)
# ----------------------------------------
def calculate_mi(file_path):
    """Calculates Maintainability Index (MI)."""
    mi_data = run_radon_analysis("mi", file_path)
    return round(mi_data[file_path]["mi"], 2)


# ----------------------------------------
# 6️⃣ Halstead Volume (HV)
# ----------------------------------------
def calculate_hv(file_path):
    """Calculates Halstead Volume (HV)."""
    hv_data = run_radon_analysis("hal", file_path)
    return round(hv_data[file_path]["total"]["volume"], 2)


# ----------------------------------------
# Full Code Analysis
# ----------------------------------------
def analyze_code_metrics(file_path):
    """Analyzes all metrics for a given file."""
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    tree = parse_python_file(file_path)
    class_methods, class_hierarchy = extract_class_info(tree)
    class_dependencies = extract_class_dependencies(tree, class_methods, class_hierarchy)

    return {
        "WMC": calculate_wmc(class_methods),
        "CBO": calculate_cbo(class_dependencies),
        "LCOM": calculate_lcom(tree),
        "DIT": calculate_dit(class_hierarchy),
        "MI": calculate_mi(file_path),
        "HV": calculate_hv(file_path)
    }


# ----------------------------------------
# Run Code Analysis for all files in src/
# ----------------------------------------
SRC_PATH = "src"
if os.path.exists(SRC_PATH):
    file_path_list = [os.path.join(SRC_PATH, file_name) for file_name in os.listdir(SRC_PATH) if
                      file_name.endswith(".py")]
    results_list = {}

    for file_path in file_path_list:
        results = analyze_code_metrics(file_path)
        results_list[file_path] = results
        print(f"\n--- Code Metrics for '{file_path}' ---")
        for key, value in results.items():
            print(f"{key}: {value}")

    # Save results in json-file for GitHub Actions
    with open("metrics_report.json", "w", encoding="utf-8") as file:
        json.dump(results_list, file, indent=4)

    print("\nCode Metrics report saved as 'metrics_report.json'.")

else:
    print(f"Source path '{SRC_PATH}' not found!")
    exit(1)