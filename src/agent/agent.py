from langgraph.graph import StateGraph, START, END

from langchain_openai import ChatOpenAI

from src.agent.nodes.experts import expert_math_agent, expert_code_agent, code_critic_agent, reflection_agent
from src.agent.nodes.tool_nodes import code_executor_node, code_validator_node, save_model_node, end_execution_on_max_retries
from src.agent.gates.gates import post_code_validation_gate, post_code_critic_gate, post_code_execution_gate, post_reflection_gate
from src.agent.tools.tools import code_validator, code_executor, save_model_files
from src.agent.state import State



def build_agent(verbose: bool = False, model: str = "o3-mini-2025-01-31", api_key: str = None):
    # Build the workflow graph
    llm = ChatOpenAI(model=model, api_key=api_key)

    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("expert_math_agent", expert_math_agent)
    workflow.add_node("expert_code_agent", expert_code_agent)
    workflow.add_node("code_critic_agent", code_critic_agent)
    workflow.add_node("reflection_agent", reflection_agent)
    workflow.add_node("code_exec_tool", code_executor_node)
    workflow.add_node("code_validation_tool", code_validator_node)
    workflow.add_node("abort_node", end_execution_on_max_retries)
    workflow.add_node("save_revised_model", save_model_node)

    # Add edges to match the diagram
    workflow.add_edge(START, "expert_math_agent")
    workflow.add_edge("expert_math_agent", "expert_code_agent")
    workflow.add_edge("expert_code_agent", "code_validation_tool")
    workflow.add_conditional_edges(
        "code_validation_tool",
        post_code_validation_gate,
        {
            "Critic": "code_critic_agent", # follow happy path
            "CodeExpert": "expert_code_agent", # correct
            "Abort": "abort_node", # abort on max retries
        },
    )
    workflow.add_conditional_edges(
        "code_critic_agent",
        post_code_critic_gate,
        {
            "Execute": "code_exec_tool", # follow happy path
            "CodeExpert": "expert_code_agent", # correct
            "Abort": "abort_node", # abort on max retries
        },
    )
    workflow.add_conditional_edges(
        "code_exec_tool",
        post_code_execution_gate,
        {
            "Math": "expert_math_agent", # Infeasible solution
            "Reflection": "reflection_agent", # Happy path
            "CodeExpert": "expert_code_agent", # Correct execution errors
            "Abort": "abort_node", # abort on max retries
        },
    )
    workflow.add_conditional_edges(
        "reflection_agent",
        post_reflection_gate,
        {
            "Math": "expert_math_agent", # Non coherent solution
            "SaveResults": "save_revised_model", # Happy path
            "Abort": "abort_node", # abort on max retries
        },
    )
    workflow.add_edge("abort_node", END)
    workflow.add_edge("save_revised_model", END)

    # Compile the workflow
    agent = workflow.compile()
    # Show the workflow graph
    if verbose:
        display(Image(agent_v1.get_graph(xray=True).draw_mermaid_png()))
    
    return agent