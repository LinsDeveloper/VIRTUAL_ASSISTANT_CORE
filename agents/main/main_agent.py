from langchain.agents import initialize_agent, AgentType


def build_agent_main(llm, tools):
    """
    Build the main agent with the specified model and tools.
    """
    agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=3)
    
    return agent
    

def invoke_agent_main(llm, tools, prompt):
    """
    Invoke the agent with the specified prompt.
    """
    agent = build_agent_main(llm, tools)
    response = agent.run(prompt)
    
    return response