import ast
import os

def get_imports(file_path):
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                imports.add(node.module)
    return imports

def write_requirements(file_path, imports):
    with open(file_path, "w") as file:
        for imp in sorted(imports):
            file.write(f"{imp}\n")

def gather_imports_from_directory(directory):
    all_imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_imports.update(get_imports(file_path))
    return all_imports

directory = "."  # Set your project directory here
all_imports = gather_imports_from_directory(directory)
write_requirements("requirements.txt", all_imports)
print("requirements.txt file has been generated.")