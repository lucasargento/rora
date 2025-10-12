import ast
import subprocess
import tempfile
import os

from langchain_core.tools import tool


# Tool: code_validator (validates the generated code)
@tool
def code_validator(code: str) -> str:
    """Validates Python code for syntax errors and basic issues."""
    try:
        # Extract code from markdown if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        # Parse the code to check for syntax errors
        ast.parse(code)
        
        # Basic checks
        if (
            ("import ortools" not in code and "from ortools" not in code) and
            ("import pulp" not in code and "from pulp" not in code)
        ):
            return "ERROR: Code must import either OR-Tools or PuLP library"
        
        if "def main()" not in code and "if __name__" not in code:
            return "WARNING: Code should have a main function or proper entry point"
        
        return "VALID: Code passed basic validation checks"
        
    except SyntaxError as e:
        return f"ERROR: Syntax error - {str(e)}"
    except Exception as e:
        return f"ERROR: Validation error - {str(e)}"

# Tool: code_executor (executes code in sandbox)
@tool
def code_executor(code: str) -> str:
    """Executes Python code in a sandbox environment and returns the output."""
    try:
        # Extract code from markdown if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()
        
        #print("Code to execute:\n\n", code, "\n", "--"*60)
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute the code
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                return f"SUCCESS:\n{result.stdout}"
            else:
                return f"ERROR:\n{result.stderr}"
                
        finally:
            # Clean up temporary file
            os.unlink(temp_file)
            
    except subprocess.TimeoutExpired:
        return "ERROR: Code execution timed out (30 seconds)"
    except Exception as e:
        return f"ERROR: Execution error - {str(e)}"

# Tool: save_model_files (saves the model code and results)
@tool
def save_model_files(description: str, model_name: str, code: str, math_formulation: str, execution_results: str, expected_output: str) -> str:
    """
    Saves the model code and execution results to files.
    This is called deterministically from the tool environment only if the result is valid
    """
    try:
        # Create the proposed_models directory if it doesn't exist
        models_dir = "satisfaction_results"
        os.makedirs(models_dir, exist_ok=True)
        
        # Create subdirectory for the specific problem
        problem_dir = os.path.join(models_dir, model_name)
        os.makedirs(problem_dir, exist_ok=True)
        
        # Extract clean code
        if "```python" in code:
            clean_code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            clean_code = code.split("```")[1].split("```")[0].strip()
        else:
            clean_code = code
        
        # Create the Python file with mathematical formulation as comments
        py_file_path = os.path.join(problem_dir, f"{model_name}.py")
        
        with open(py_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# Problem Description:\n")
            f.write(f"'''{description}'''\n\n")
            f.write(f"# Mathematical Formulation:\n")
            f.write(f"'''{math_formulation}'''\n\n")
            f.write(f"# Generated Code:\n")
            f.write(clean_code)
            f.write("\n\n")
            f.write(f"'''Execution Results:\n{execution_results}'''\n\n")
            f.write(f"'''Expected Output:\n{expected_output}'''\n\n")
        
        # Create a results file
        results_file_path = os.path.join(problem_dir, f"{model_name}_results.txt")
        with open(results_file_path, 'w', encoding='utf-8') as f:
            f.write(f"Problem Name: {model_name}\n\n")
            f.write(f"# Problem Description:\n")
            f.write(f"'''{description}'''\n\n")
            f.write(f"Mathematical Formulation:\n{math_formulation}\n\n")
            f.write(f"Execution Results:\n{execution_results}\n\n")
            f.write(f"Expected Output:\n{expected_output}\n")
        
        # Save a JSON file with only the execution results
        import json

        execution_results_json = {
            "execution_results": execution_results
        }
        json_file_path = os.path.join(problem_dir, f"{model_name}_execution_results.json")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(execution_results_json, f, indent=2, ensure_ascii=False)

        return f"Files saved successfully:\n- {py_file_path}\n- {results_file_path}"
        
    except Exception as e:
        return f"Error saving files: {str(e)}"