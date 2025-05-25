import os
from langchain.agents import initialize_agent, AgentType
from agents.spotify.spotify_agent import invoke_agent_spotify
from core.llms.invoke_model import get_model_class
from core.enum.model_type_enum import ModelTypeEnum
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
load_dotenv()

def prompt_base():
    """
    Base prompt for the agent.
    """
    return SystemMessage(
        content="You are a helpful assistant that can play music on Spotify."
    )

def build_agent_main(agentype=AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations: int = 3):
    """
    Build the main agent with the specified model and tools.
    """
    
    
    llm = get_model_class(ModelTypeEnum.LLAMA3)
    verbose = os.getenv("VERBOSE", "False").lower() == "true"
    tools = [invoke_agent_spotify]
    agent = initialize_agent(tools, llm, agent_type=agentype, verbose=verbose, max_iterations=max_iterations)
    
    return agent


def invoke_agent_main(prompt):
    """
    Invoke the agent with the specified prompt.
    """
    agent = build_agent_main()
    response = agent.run(prompt)
    
    return response

