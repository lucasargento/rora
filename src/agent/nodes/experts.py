from langchain_openai import ChatOpenAI
from src.agent.state import State
from src.agent.tools.tools import code_validator, code_executor, save_model_files
from src.agent.prompts.loader import load_prompt, render_prompt
import os


api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="o3-mini-2025-01-31", api_key=api_key)

# Node: expert_math_agent (formulates mathematical model)
def expert_math_agent(state: State):
    print("📐 [DEBUG] expert_math_agent: Starting mathematical formulation")
    
    # Check if this is a reformulation attempt
    is_coherent = state["coherent"]
    reformulation_context = ""
    
    if not is_coherent:
        reformulation_block = load_prompt("reformulation_block.txt")
        reformulation_context = render_prompt(
            reformulation_block,
            {
                "math_result": state.get("math_result", ""),
                "reflection_status": state.get("reflection_status", ""),
            },
        )
    
    template = load_prompt("expert_math_agent.txt")
    prompt = render_prompt(
        template,
        {
            "problem_statement": state["problem_statement"],
            "reformulation_context": reformulation_context,
        },
    )

    msg = llm.invoke(prompt)
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

    template = load_prompt("expert_code_agent.txt")
    prompt = render_prompt(
        template,
        {
            "problem_statement": state["problem_statement"],
            "math_result": state["math_result"],
        },
    )

    msg = llm.invoke(prompt)
    code_result = msg.content
    
    print(f"💻 [DEBUG] expert_code_agent: Generated code implementation (length: {len(code_result)} chars)")
    return {"code_result": code_result}

# Node: code_critic_agent (reviews code)
def code_critic_agent(state: State):
    print("💻 [DEBUG] code_critic_agent: Starting code critic")

    template = load_prompt("code_critic_agent.txt")
    prompt = render_prompt(
        template,
        {
            "math_result": state["math_result"],
            "code_result": state["code_result"],
        },
    )

    msg = llm.invoke(prompt)
    feedback = msg.content
    
    print(f"💻 [DEBUG] code_critic_agent: Generated code feedback:\n {feedback}")
    return {"code_feedback": feedback}

# Node: reflection_agent (reflects on solution)
def reflection_agent(state: State):
    print("💻 [DEBUG] reflection_agent: Starting reflection step")

    template = load_prompt("reflection_agent.txt")
    prompt = render_prompt(
        template,
        {
            "problem_statement": state["problem_statement"],
            "math_result": state["math_result"],
            "code_result": state["code_result"],
        },
    )

    msg = llm.invoke(prompt)
    reflection = msg.content
    
    print(f"💻 [DEBUG] reflection_agent: Generated solution reflection:\n {reflection}")
    coherent = "OK" in reflection
    return {"reflection_status": reflection, "coherent": coherent}