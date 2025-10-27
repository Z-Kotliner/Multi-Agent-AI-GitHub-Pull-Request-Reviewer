from llama_index.core.agent.workflow import AgentWorkflow
from agents import get_context_agent, get_commentator_agent


def get_workflow_agent():
    # Get the agents
    context_agent = get_context_agent()
    commentor_agent = get_commentator_agent()
    workflow_agent = AgentWorkflow(
        agents=[context_agent, commentor_agent],
        root_agent=commentor_agent.name,
        initial_state={
            "gathered_contexts": "",
            "draft_comment": ""
        },
    )

    return workflow_agent
