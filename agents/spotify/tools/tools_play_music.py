from typing import Optional
from langchain.tools import Tool
from agents.spotify.chains.extract_artist_music import ExtractArtistMusicChain
from agents.spotify.resources.resource_play_music import play_pause_music, play_specific_song

from langchain.tools import Tool
from agents.spotify.resources.resource_play_music import play_pause_music

def search_song_by_artist_and_name(query: str) -> str:
    extractor_chain = ExtractArtistMusicChain()
    try:
        artist, music = extractor_chain.run(query)
        result = play_specific_song(artist_name=artist, track_name=music)
        return result.response
    except Exception as e:
        return f"Erro ao extrair artista e música: {str(e)}"

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
        ),
        Tool(
            name="search_song",
            func=search_song_by_artist_and_name,
            description="Utilize essa ferramenta para tocar uma música específica no Spotify que tenha o nome do artista e o nome da música. Sem esses dois, Não utilize. "
        ),
    ]


__all__ = ["get_spotify_tools"]
