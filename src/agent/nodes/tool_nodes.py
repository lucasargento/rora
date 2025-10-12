from src.state import State
from src.agent.tools.tools import code_validator, code_executor, save_model_files

def code_validator_node(state: State):
    print("🔍 [DEBUG] code_validator_node: Validating code")
    validation_result = code_validator.invoke({"code": state['code_result']})
    print(f"🔍 [DEBUG] code_validator_node: Validation result: {validation_result}")
    return {"validation_result": validation_result}

def code_executor_node(state: State):
    print("🚀 [DEBUG] code_executor_node: Executing code")
    execution_result = code_executor.invoke({"code": state['code_result']})
    print(f"🚀 [DEBUG] code_executor_node: Execution result: {execution_result}...")
    execution_success = execution_result.startswith("SUCCESS")

    if not execution_success:
        return {
            "execution_result": execution_result,
            "execution_error": True
        }
    else:
        return {
            "execution_result": execution_result,
            "execution_error": False
        }
    
def save_model_node(state: State):
    print("Succesfully reached a feasible solution, saving results.")
    params = {
        "description": state["problem_statement"],
        "model_name": state["problem_name"],
        "code":state["code_result"],
        "math_formulation":state["math_result"],
        "execution_results":state["execution_result"],
        "expected_output":state["expected_output"]
    }
    save_model_files.invoke(
       params
    )

def end_execution_on_max_retries(state: State):
    print("Max Retries reached. Ending agent execution.")