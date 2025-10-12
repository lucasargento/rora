from langchain_openai import ChatOpenAI
from src.agent.state import State
from src.agent.tools.tools import code_validator, code_executor, save_model_files
import os


api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="o3-mini-2025-01-31", api_key=api_key)

# Node: expert_math_agent (formulates mathematical model)
def expert_math_agent(state: State):
    print("📐 [DEBUG] expert_math_agent: Starting mathematical formulation")
    #print(f"📐 [DEBUG] expert_math_agent: Problem statement: {state['problem_statement']}")
    
    # Check if this is a reformulation attempt
    is_coherent= state["coherent"]
    reformulation_context = ""
    
    if not is_coherent:
        reformulation_context = f"""
            
            **REFORMULATION REQUEST**: Your previous five-elements mathematical formulation did not lead to an optimal or coherent solution.
            
            **Previous Formulation**:
            {state['math_result']}
            
            **Expert's reflection on the solution**:
            {state["reflection_status"]}
            
            **Instructions for Reformulation**:
            - Analyze why the previous formulation failed to produce an optimal solution
            - Check for logical errors, missing constraints, or incorrect variable definitions
            - Ensure the problem is properly bounded and feasible
            - Consider if the objective function is correctly formulated
            - Make sure all constraints are mathematically sound and complete
            - Avoid trivial solutions (e.g., all variables = 0 when that's not meaningful)
        """
    
    five_elements_prompt = f"""
        You are an expert in mathematical optimization. Your task is to translate the following real-world optimization problem into a precise and structured mathematical model using the five-element framework.

        Problem description:
        \"\"\"
        {state['problem_statement']}
        \"\"\"
        {reformulation_context}

        Use the following five-element structure to express the model:

        ---

        ### Example:

        **Problem description:**
        A factory produces two products: A and B. Each unit of A gives a profit of $30, and each unit of B gives a profit of $20. Product A requires 2 machine hours and product B requires 1 machine hour. There are at most 100 machine hours available. Also, product A requires 1 labor hour and product B requires 2 labor hours. There are at most 80 labor hours available. The factory wants to determine how many units of each product to produce in order to maximize profit.

        **Structured Model:**

        ## Sets:
        - P: set of products = {{A, B}}

        ## Parameters:
        - profit_p: profit per unit of product p [USD]
        - time_p: machine hours required per unit of p [hours]
        - labor_p: labor hours required per unit of p [hours]
        - max_machine_time: total available machine hours [hours]
        - max_labor_time: total available labor hours [hours]

        ## Variables:
        - x_p: number of units of product p to produce [integer ≥ 0] [units]

        ## Objective:
        - Maximize total profit = sum over p in P of (profit_p * x_p)

        ## Constraints:
        - Machine time constraint: sum over p in P of (time_p * x_p) ≤ max_machine_time
        - Labor constraint: sum over p in P of (labor_p * x_p) ≤ max_labor_time

        ---

        Now, apply the same structure to the new problem below.

        Requirements:
        1. Be complete and faithful to the original problem.
        2. Do NOT use LaTeX or any math formatting syntax.
        3. Ensure the model is self-contained and logically consistent.
        4. Do not invent data or simplify the problem unless explicitly instructed.
        5. Use simple mathematical expressions that are easy to map to Python or OR-Tools code.
        6. The model will be used by another LLM to generate a working implementation, so make it readable and unambiguous.
        7. Check that the units of all parameters are consistent with the problem description.
            - If units are unclear or inconsistent, make reasonable assumptions and explicitly state them in the model comments.
            - If ambiguity remains (for example if different units are stated in problem data/parametrs and problem description), produce an alternative version of the model alongside the main one, so the coding agent can implement and compare both.
            - You dont need to always create two models, only if you consider that two formulations are required.
            - If you are REFORMULATING this problem dont include math models for previously proven unfeasible formulations
            
        Additional important guidelines for modeling:
        - If the objective involves both revenues and costs, clearly separate them into two expressions: total revenue and total cost. Then define the net objective as their difference.
        - Always specify the unit and interpretation of economic parameters like costs, prices, or revenues (e.g., per unit produced, per batch, per hour).
        - Use consistent naming and consider defining helper variables (e.g., total input used, total output produced) to improve readability and implementation.
        - Avoid duplicating the same expression in multiple places; define and reuse intermediate expressions where possible.
        - If helpful, include sanity-check expectations (e.g., typical variable ranges, expected magnitudes) as comments or hints — these are optional and for interpretability only.
        - Be explicit about whether each decision variable is continuous, integer, or binary.
        - If there is any investment or delay that affects future capacity, define a parameter for investment effectiveness or capacity gain.
        - Use semantically clear names for parameters and variables that reflect their economic or physical meaning (e.g., InputFinal, InvestmentGain, etc).
        - Clearly define when stock becomes available (beginning of period or end?) and whether it can be used in the same period.
        - For complex dynamics like stock balance or delayed effects, define intermediate expressions to improve traceability and code generation.

        Respond strictly using the five-element format:
        Sets, Parameters, Variables, Objective, Constraints.
    """


    msg = llm.invoke(five_elements_prompt)
    math_result = msg.content
    
    print("--"*60)
    print("--> Problem Description")
    print(state['problem_statement'])
    print(".."*60)
    print("--> Mathematical Problem Formulation:")
    print(math_result)
    print("--"*60)

    return {"math_result": math_result}

# Node: expert_code_agent (writes implementation code)
def expert_code_agent(state: State):
    print("💻 [DEBUG] expert_code_agent: Starting code implementation")
    #print(f"💻 [DEBUG] expert_code_agent: Problem statement: {state['problem_statement']}")
    #print(f"💻 [DEBUG] expert_code_agent: Math result length: {len(state.get('math_result', ''))} chars")


    or_tools_five_elements_prompt_no_latex = f"""
        You are an expert Python developer specialized in optimization using Google OR-Tools.

        Your task is to implement the following optimization problem using the `ortools.linear_solver` or `ortools.sat.python.cp_model` module, depending on the problem type.

        ---

        **Problem Description**:
        \"\"\"
        {state['problem_statement']}
        \"\"\"

        **Structured Mathematical Formulation (Five-Element Format)**:
        This is a structured formulation of the problem including Sets, Parameters, Variables, Objective, and Constraints. The format is plain text, not LaTeX.

        \"\"\"
        {state['math_result']}
        \"\"\"

        ---

        **Instructions**:
        - Use only **Google OR-Tools**. No other libraries are allowed.
        - If the problem is a linear or mixed-integer program, use `ortools.linear_solver`.
        - If the problem involves logical constraints, scheduling, or complex combinatorics, use `ortools.sat.python.cp_model`.
        - Use the five-element input to:
            - Declare the right variables (type, domain, names)
            - Set up the correct objective function (maximize or minimize)
            - Add all constraints
        - Follow Python best practices: use a `main()` function, add comments when helpful, and keep the code clean and readable.
        - At the end, print the optimal solution and the objective value. If infeasible, print a message explaining it.
        - Output only the Python code inside a single code block. Do not include explanations or markdown outside of the code.
        - If the mathematical formulation includes more than one possible version (e.g., due to ambiguity in units or interpretation), implement all versions provided. ALWAYS in different separate problem implementatations. call both implementations from the main() function and show results for both in a nice structured way.
        - IF more than one formulation is proposed, always keep each version completely separate. Do not mix variables, constraints, or logic between models.        
        - You dont need to always create two models, only if two formulations are required by the math formulation

        Format your answer as an executable Python script in a code block.
    """


    msg = llm.invoke(or_tools_five_elements_prompt_no_latex)
    code_result = msg.content
    
    print(f"💻 [DEBUG] expert_code_agent: Generated code implementation (length: {len(code_result)} chars)")
    return {"code_result": code_result}

# Node: expert_code_agent (writes implementation code)
def code_critic_agent(state: State):
    print("💻 [DEBUG] code_critic_agent: Starting code critic")
    #print(f"💻 [DEBUG] expert_code_agent: Problem statement: {state['problem_statement']}")
    #print(f"💻 [DEBUG] expert_code_agent: Math result length: {len(state.get('math_result', ''))} chars")
    
    or_tools_critic_prompt_no_latex = f"""
        You are an expert code critic specializing in optimization models implemented with Google OR-Tools.

        Your task is to carefully review the following Python code and compare it against a structured mathematical formulation. The formulation follows a "five-element format", where the problem is broken down into Sets, Parameters, Variables, Objective, and Constraints — all written in plain text (not LaTeX).

        ---

        **REVIEW CRITERIA:**

        1. **Mathematical Correctness:**
        - Does the code correctly implement all decision variables from the formulation?
        - Are variable domains (e.g., integer, binary, real ≥ 0) respected?
        - Is the objective function (min/max) correctly implemented?
        - Are all constraints correctly translated from the formulation?

        2. **OR-Tools Best Practices:**
        - Is the appropriate module used (`linear_solver` for LP/MILP, `cp_model` for constraint-based problems)?
        - Are variables declared with clear names, bounds, and types?
        - Are all constraints and the objective properly added to the model?

        3. **Code Quality & Efficiency:**
        - Is the code readable and logically structured?
        - Are there any redundant or inefficient parts?
        - Does it include appropriate error handling (e.g., infeasible models)?

        4. **Problem-Specific Logic:**
        - Does the solution make sense in the context of the problem?
        - Are there missing edge cases or logical inconsistencies?
        - Is the output clear and informative?

        5. **Potential Issues:**
        - Could the model be unbounded or infeasible?
        - Are there any numerical or scaling issues?
        - Is solver configuration appropriate (timeouts, tolerances)?

        ---

        **Structured Mathematical Formulation (Five-Element Format):**
        \"\"\"
        {state['math_result']}
        \"\"\"

        **Code Implementation (Python with OR-Tools):**
        \"\"\"
        {state['code_result']}
        \"\"\"

        ---

        **INSTRUCTIONS:**
        - Compare the Python code line by line with the formulation above.
        - If you find issues, list them clearly and concisely.
        - If the code is correct and matches the formulation, respond with "OK".
        - Focus only on issues that affect correctness or performance — ignore minor stylistic choices.

        **RESPONSE FORMAT:**
        - If issues found: List each issue with a short explanation
        - If no issues found: Respond with "OK"
    """


    msg = llm.invoke(or_tools_critic_prompt_no_latex)
    feedback = msg.content
    
    print(f"💻 [DEBUG] code_critic_agent: Generated code feedback:\n {feedback}")
    return {"code_feedback": feedback}

# Node: expert_code_agent (writes implementation code)
def reflection_agent(state: State):
    print("💻 [DEBUG] reflection_agent: Starting reflection step")
    #print(f"💻 [DEBUG] expert_code_agent: Problem statement: {state['problem_statement']}")
    #print(f"💻 [DEBUG] expert_code_agent: Math result length: {len(state.get('math_result', ''))} chars")


    reflection_prompt_no_latex = f"""
        You are an Operations Research Expert specializing in optimization problems. Your task is to evaluate whether the solution found is coherent and reasonable given the original problem statement and its mathematical formulation.

        The formulation is written in a structured "five-element format" (Sets, Parameters, Variables, Objective, Constraints), expressed in plain text.

        ---

        **REFLECTION CRITERIA:**

        1. **Solution Relevance:**
        - Does the solution directly address the original problem?
        - Are the decision variables meaningful and present?
        - Is the objective value consistent with what is being optimized?

        2. **Solution Plausibility:**
        - Are the numerical results realistic for the type of problem?
        - Do the values fall within expected ranges given the constraints?
        - Are there any negative or extreme values that don’t make sense?

        3. **Solution Completeness:**
        - Are all decision variables included in the output?
        - Is the objective value present?
        - Is the output format clear and unambiguous?

        4. **Logical Consistency:**
        - Does the solution satisfy all constraints?
        - Is there any contradiction between the output and the problem formulation?
        - Is the logic consistent with what would be expected in this domain?

        5. **Context Appropriateness:**
        - Do the results make sense in the real-world context described?
        - Would this solution be usable in practice?
        - Does it reflect common-sense understanding of the problem?

        ---

        **ORIGINAL PROBLEM STATEMENT:**
        \"\"\"
        {state['problem_statement']}
        \"\"\"

        **STRUCTURED MATHEMATICAL FORMULATION (Five-Element Format):**
        \"\"\"
        {state['math_result']}
        \"\"\"

        **EXECUTION RESULTS:**
        \"\"\"
        {state['code_result']}
        \"\"\"

        ---

        **INSTRUCTIONS:**
        - Analyze whether the solution is reasonable, complete, and matches the context and formulation.
        - Focus on critical issues: missing data, incoherent values, unrealistic outputs, or contradictions.

        **RESPONSE FORMAT:**
        - If the solution is coherent and reasonable: Respond with **"OK"** and nothing else.
        - If the solution is problematic: Respond with **"NON COHERENT"** followed by specific issues.

        **IMPORTANT:**
        If the response is NON COHERENT, your feedback will be used by a math expert agent to reformulate the problem from scratch. Be precise and helpful.

        **COMMON ISSUES TO FLAG:**
        - Missing or incomplete output
        - Negative values where not allowed
        - Outputs that violate known constraints
        - Objective values that are absurdly high/low
        - Solutions that don't match what the problem asked
    """


    msg = llm.invoke(reflection_prompt_no_latex)
    reflection = msg.content
    
    print(f"💻 [DEBUG] reflection_agent: Generated solution reflection:\n {reflection}")
    coherent = "OK" in reflection
    return {"reflection_status": reflection, "coherent": coherent}