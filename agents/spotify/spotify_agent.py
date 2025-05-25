import os
from langchain.agents import initialize_agent, AgentType

from agents.spotify.tools.tools_play_music import get_tools_spotify
from core.enum.model_type_enum import ModelTypeEnum
from core.llms.invoke_model import get_model_class


def build_agent_spotify(agentype=AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations: int = 1):
    """
    Build the main agent with the specified model and tools.
    """
    
    llm = get_model_class(ModelTypeEnum.LLAMA3)
    verbose = os.getenv("VERBOSE", "False").lower() == "true"
    tools = [get_tools_spotify()]
    agent = initialize_agent(tools, llm, agent_type=agentype, verbose=verbose, max_iterations=max_iterations)
    
    return agent
    

def invoke_agent_spotify(prompt: str):
    """
    Invoke the agent with the specified prompt.
    """
    agent = build_agent_spotify()
    return agent.run(prompt)





