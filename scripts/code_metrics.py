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
    Extracts class, method, dependency, and inheritance information in a single AST traversal.

    Returns:
        - class_methods: Dictionary mapping class names to their methods.
        - class_dependencies: List of unique class dependencies at the file level.
        - defined_classes: Set of class names defined in the file.
        - imported_classes: Set of class names imported into the file.
        - class_hierarchy: Dictionary mapping class names to their base classes.
    """
    class_methods = defaultdict(list)  # Methods per class
    class_dependencies = set()  # Dependencies per file
    defined_classes = set()  # Defined class names
    imported_classes = set()  # Imported class names
    class_hierarchy = {}  # Inheritance
    special_dependencies = {"game": "Game", "player": "Player"}  # Mapping for special dependencies

    # Iterate through all nodes in AST
    for node in ast.walk(tree):

        # Class Definition: Track class name, methods and inheritance
        if isinstance(node, ast.ClassDef):
            defined_classes.add(node.name)
            class_methods[node.name] = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
            class_hierarchy[node.name] = [base.id for base in node.bases if isinstance(base, ast.Name)]

        # Import Statement: Store imported class names
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_classes.update(alias.name for alias in node.names)

        # Method Calls: Capture function and method calls affecting dependencies
        elif isinstance(node, ast.Call):
            # Direct function call: `func_name()`
            if isinstance(node.func, ast.Name):
                called_class = node.func.id
            # Method call on object: `obj.method()`
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                called_class = node.func.value.id
            else:
                continue

            # Register dependency (only if it refers to a class)
            if called_class in defined_classes or called_class in imported_classes:
                class_dependencies.add(called_class)

        # Capture attribute access that references other classes
        elif isinstance(node, ast.Attribute):
            # Direct attribute access (self.game or self.player)
            if isinstance(node.value, ast.Name) and node.value.id == "self":
                accessed_var = node.attr  # Extracts "game" or "player"
                if accessed_var in special_dependencies:
                    class_dependencies.add(special_dependencies[accessed_var])  # Maps to "Game" or "Player"

            # Handle nested attribute access (self.game.player → "Player")
            elif isinstance(node.value, ast.Attribute) and isinstance(node.value.value,
                                                                      ast.Name) and node.value.value.id == "self":
                root_var = node.value.attr  # Extracts "game"
                final_attr = node.attr  # Extracts "player"
                if root_var in special_dependencies and final_attr == "player":
                    class_dependencies.add("Player")  # Recognizes "self.game.player" as "Player"

            # General case: If the accessed attribute belongs to a defined/imported class, register it as a dependency
            elif isinstance(node.value, ast.Name) and node.value.id in defined_classes | imported_classes:
                class_dependencies.add(node.value.id)

    return class_methods, list(class_dependencies), class_hierarchy


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
    """Calculates Coupling Between Objects (CBO)."""
    return len(class_dependencies)


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
    class_methods, class_dependencies, class_hierarchy = extract_class_info(tree)

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