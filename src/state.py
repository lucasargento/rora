from typing_extensions import TypedDict


# Define the state for the workflow
class State(TypedDict):
    problem_statement: str  # Input problem statement
    problem_name: str  # User-defined problem name
    expected_output: str
    
    math_result: str
    code_result: str
    code_feedback: str
    validation_result: str
    execution_result: str
    execution_error: bool = False
    reflection_status: str
    coherent: bool = True
    last_failure_reason: str

    global_retries: int = 0
    model_saved: bool  # Track if model was successfully saved