import sys
import re
import os

def extract_class_name(header_content):
    # Regular expression to find the class name in the header file
    class_pattern = re.compile(r'class\s+(\w+)\s*(?::\s*\w+\s*\w+\s*)?(?=\s*\{)')
    match = class_pattern.search(header_content)
    if match:
        return match.group(1)
    return None

def add_stdout_calls_to_cpp_methods(folder_path):
    try:
        # Read the C++ source file
        with open(cpp_file_path, 'r') as cpp_file:
            cpp_content = cpp_file.read()

            # Extract the corresponding header file path
            header_file_path = os.path.splitext(cpp_file_path)[0] + '.h'

            # Read the header file
            with open(header_file_path, 'r') as header_file:
                header_content = header_file.read()

                # Extract the class name from the header
                class_name = extract_class_name(header_content)

                if class_name:
                    # Regular expression to match C++ method declarations
                    method_pattern = re.compile(r'\b' + re.escape(class_name) + r'\s*::\s*(\w+)\s*\([^)]*\)\s*{')

                    # Find all method declarations
                    method_matches = method_pattern.finditer(cpp_content)

                    # Iterate over method matches
                    for match in method_matches:
                        function_name = match.group(1)
                        std_out_call = f'    std::cout << "Calling {class_name}::{function_name}." << std::endl;'
                        cpp_content = cpp_content.replace(match.group(), f'{match.group()}\n{std_out_call}')

                    # Write modified content back to the file
                    with open(cpp_file_path, 'w') as modified_cpp_file:
                        modified_cpp_file.write(cpp_content)

                    print(f"Added std::cout calls to methods in '{cpp_file_path}' successfully.")
                else:
                    print(f"Class name not found in '{header_file_path}'.")
    except FileNotFoundError:
        print(f"File '{cpp_file_path}' not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_stdout_calls.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        for root, _, files in os.walk(folder_path):
            for cpp_file in files:
                if cpp_file.endswith(".cpp"):
                    cpp_file_path = os.path.join(root, cpp_file)
                    add_stdout_calls_to_cpp_methods(cpp_file_path)
