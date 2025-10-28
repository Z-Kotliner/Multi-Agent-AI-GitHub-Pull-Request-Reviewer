from llama_index.core.agent.workflow import AgentWorkflow
from agents import get_context_agent, get_commentator_agent, get_review_and_post_agent


def get_workflow_agent():
    # Get the agents
    context_agent = get_context_agent()
    commentor_agent = get_commentator_agent()
    review_and_post_agent = get_review_and_post_agent()

    # Init the workflow
    workflow_agent = AgentWorkflow(
        agents=[context_agent, commentor_agent, review_and_post_agent],
        root_agent=review_and_post_agent.name,
        initial_state={
            "gathered_contexts": "",
            "review_comment": "",
            "final_review_comment": "",
        },
    )

    return workflow_agent
