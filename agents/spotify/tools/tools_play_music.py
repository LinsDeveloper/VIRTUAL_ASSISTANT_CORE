from langchain.tools import StructuredTool
from ..resources.resource_play_music import play_specific_song,  play_pause_music

tools = [
    StructuredTool.from_function(
        name="Play Song",
        func=play_specific_song,
        description="Toca uma música específica no Spotify. Use quando o usuário pedir para tocar uma música."
    ),
    StructuredTool.from_function(
        name="Pause Song",
        func=play_pause_music,
        description="Pausa a música atualmente tocando no Spotify. Use quando o usuário pedir para pausar a música."
    ),
    StructuredTool.from_function(
        name="Resume Song",
        func=play_pause_music,
        description="Retoma a reprodução da música pausada no Spotify. Use quando o usuário pedir para continuar a música."
    )
]

def get_tools_spotify():
    """
    Retorna a lista de ferramentas para o Spotify Play.
    """
    return tools
