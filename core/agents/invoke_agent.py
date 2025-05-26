from agents.spotify.spotify_agent import invoke_agent_spotify
from core.enum.agents_enum import AgentsCoreEnum

def get_agent_type(agent_type: AgentsCoreEnum):
    """
    This function is a placeholder for getting an agent based on the type.
    It currently does not perform any operations.
    """
    
    match agent_type:
        case AgentsCoreEnum.SPOTIFY_PLAY:
            return invoke_agent_spotify
    
    pass

def invoke_agent(agent_type: AgentsCoreEnum):
    """
    This function is a placeholder for invoking an agent.
    It currently does not perform any operations.
    """
    
    agent = get_agent_type(agent_type)
    
    
    pass

