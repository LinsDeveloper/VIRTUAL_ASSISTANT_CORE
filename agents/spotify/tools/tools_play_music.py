from typing import Optional
from langchain.tools import Tool
from agents.spotify.resources.resource_play_music import play_pause_music


def pause_song(_action: str = None) -> str:
    response = play_pause_music("pause")
    return response.response


def resume_song(_action: str = None) -> str:
    response = play_pause_music("play")
    return response.response


def get_spotify_tools():
    return [
        Tool(
            name="pause_song",
            func=pause_song,
            description="Pausa a música que está tocando no Spotify"
        ),
        Tool(
            name="resume_song",
            func=resume_song,
            description="Continua a música pausada no Spotify"
        )
    ]


__all__ = ["get_spotify_tools"]
