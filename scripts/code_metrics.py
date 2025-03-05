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
    """Extracts class, method, and dependency information in a single AST traversal."""
    class_methods = defaultdict(list)  # Methods per class
    class_dependencies = defaultdict(set)  # Dependencies per class
    defined_classes = set()  # Defined class names
    imported_classes = set()  # Imported class names

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            defined_classes.add(node.name)
            class_methods[node.name] = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_classes.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            for class_name in defined_classes:
                if node.func.id in defined_classes or node.func.id in imported_classes:
                    class_dependencies[class_name].add(node.func.id)

    return class_methods, class_dependencies, defined_classes, imported_classes


# ----------------------------------------
# 1️⃣ WMC (Weighted Methods per Class)
# ----------------------------------------
def calculate_cc(file_path):
    """Calculates Cyclomatic Complexity (CC) for each method."""
    cc_data = run_radon_analysis("cc", file_path)
    return {m['name']: m['complexity'] for methods in cc_data.values() for m in methods}

def calculate_wmc(class_methods, file_path):
    """Calculates Weighted Methods per Class (WMC)."""
    method_cc = calculate_cc(file_path)  # Get CC per method
    return sum(sum(method_cc.get(m, 1) for m in methods) for methods in class_methods.values())


# ----------------------------------------
# 2️⃣ CBO (Coupling Between Objects)
# ----------------------------------------
def calculate_cbo(class_dependencies):
    """Calculates Coupling Between Objects (CBO)."""
    return sum(len(deps) for deps in class_dependencies.values())


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
def calculate_dit(tree):
    """Calculates Depth of Inheritance Tree (DIT)."""
    class_hierarchy = {node.name: [base.id for base in node.bases if isinstance(base, ast.Name)]
                       for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}

    def find_depth(cls, depth=0):
        if cls not in class_hierarchy or not class_hierarchy[cls]:
            return depth
        return max(find_depth(base, depth + 1) for base in class_hierarchy[cls])

    return max((find_depth(cls) for cls in class_hierarchy), default=0)


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
    class_methods, class_dependencies, _, _ = extract_class_info(tree)

    return {
        "WMC": calculate_wmc(class_methods, file_path),
        "CBO": calculate_cbo(class_dependencies),
        "LCOM": calculate_lcom(tree),
        "DIT": calculate_dit(tree),
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