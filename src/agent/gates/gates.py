from src.state import State


# aux functions
def update_retry_count(state: State):
    retries = state.get("global_retries", 0)
    state["global_retries"] = retries + 1

def should_retry(state: State):
    MAX_GLOBAL_RETRIES = 5
    retries = state.get("global_retries", 0)
    if retries + 1 >= MAX_GLOBAL_RETRIES:
        return False
    else:
        return True
    
# gates
def post_code_validation_gate(state: State):
    """
    Determines the next step in the pipeline based on the result of code validation.

    Args:
        state (State): The current state object containing the validation result.

    Returns:
        str: The name of the next node in the pipeline. Returns "Critic" if the validation result starts with "VALID" or "WARNING",
             otherwise returns "CodeExpert" for further correction.
    """
    if state["validation_result"].startswith("VALID") or state["validation_result"].startswith("WARNING"):
        return "Critic"
    else:
        if should_retry(state=state):
            update_retry_count(state=state)
            state["last_failure_reason"] = "validation_error"
            return "CodeExpert" # this a retry in code expert
        else:
            return "Abort"

def post_code_critic_gate(state: State):
    """
    Determines the next step in the pipeline based on the result of the code critic's feedback.

    Args:
        state (State): The current state object containing the critic's result.

    Returns:
        str: The name of the next node in the pipeline. Returns "Execute" if the critic's result contains "OK",
             otherwise returns "CodeExpert" for further correction.
    """
    if "OK" in state["code_feedback"]:
        return "Execute"
    else:
        state["last_failure_reason"] = "code_critic"
        if should_retry(state=state):
            update_retry_count(state=state)
            return "CodeExpert" # this a retry in code expert
        else:
            return "Abort"

def post_code_execution_gate(state: State):
    """
    Determines the next step in the pipeline based on the result of code execution.

    Args:
        state (State): The current state object containing the execution result and error status.

    Returns:
        str: The name of the next node in the pipeline.
            - Returns "Reflection" if execution was successful and an optimal solution was found.
            - Returns "Math" if execution was successful but no optimal solution was found.
            - Returns "CodeExpert" if there was an execution error.
    """
    execution_result = state["execution_result"]

    # validate run execution and that optimal solution was found
    has_optimal_solution = True
    if state["execution_error"] == False:
        # Check for indicators of no optimal solution
        output_lower = execution_result.lower()
        no_solution_indicators = [
            "no solution",
            "no optimal solution", 
            "infeasible",
            "unbounded",
            "model is infeasible",
            "no feasible solution",
            "solution not found",
            "optimal solution not found",
            "the problem does not have an optimal solution.",
            "did not find an optimal solution"
        ]
        
        for indicator in no_solution_indicators:
            if indicator in output_lower:
                has_optimal_solution = False
                break
            # If theres an optimal solution found, send that to the reflect agent
        if has_optimal_solution:
            # Solution found and valid, sending to reflection agent
            return "Reflection"
        else:
            # Infeasible solution, sending back to math formulator. This is a retry!
            state["last_failure_reason"] = "infeasible_solution"
            if should_retry(state=state):
                update_retry_count(state=state)
                return "Math"
            else:
                return "Abort"    
    else:
        # Execution error! (retry)
        state["last_failure_reason"] = "execution_error"
        if should_retry(state=state):
            update_retry_count(state=state)
            return "CodeExpert"
        else:
            return "Abort"  
        
def post_reflection_gate(state: State):
    if state["coherent"]:
        # everything ok! communicate and save
        return "SaveResults"
    else:
        state["last_failure_reason"] = "reflection_noncoherent"
        # back to math expert to reformulate the entire problem.
        if should_retry(state=state):
            update_retry_count(state=state)
            return "Math"
        else:
            return "Abort"    