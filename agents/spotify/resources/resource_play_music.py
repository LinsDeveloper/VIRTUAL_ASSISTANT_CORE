import requests
from agents.spotify.auth.spotify_auth import authenticate_spotify
from models.AgentResponseModel import ResponseModel


def play_specific_song(artist_name: str, track_name: str, device_id: str = None) -> ResponseModel:
    """
    Toca uma música específica no Spotify com base no artista e nome da faixa.
    """
    try:
        token = authenticate_spotify()
        access_token = token if isinstance(token, str) else token.get("access_token")

        if not access_token:
            return ResponseModel(success=False, response="Erro: Token de autenticação não encontrado.")

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        params = {
            "q": f"track:{track_name} artist:{artist_name}",
            "type": "track",
            "limit": 1
        }

        response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
        response.raise_for_status()

        results = response.json()
        tracks = results.get('tracks', {}).get('items', [])
        if not tracks:
            return ResponseModel(
                success=False,
                response=f"A música '{track_name}' de '{artist_name}' não foi encontrada no Spotify."
            )

        track_uri = tracks[0]['uri']

        play_url = "https://api.spotify.com/v1/me/player/play"
        if device_id:
            play_url += f"?device_id={device_id}"

        play_data = {
            "uris": [track_uri]
        }

        play_response = requests.put(play_url, headers=headers, json=play_data)

        if play_response.status_code in [200, 204]:
            return ResponseModel(success=True, response=f"🎵 Tocando agora: '{track_name}' por {artist_name}.")
        else:
            return ResponseModel(
                success=False,
                response=f"Erro ao tentar tocar a música: {play_response.status_code} - {play_response.text}"
            )

    except requests.exceptions.RequestException as e:
        return ResponseModel(success=False, response=f"Erro de comunicação com a API do Spotify: {str(e)}")
    except Exception as e:
        return ResponseModel(success=False, response=f"Ocorreu um erro inesperado: {str(e)}")


def play_pause_music(action: str = "play", device_id: str = None) -> ResponseModel:
    """
    Toca ou pausa a música no Spotify.
    """
    try:
        action = action.strip().lower().strip("'").strip('"')

        if action not in ["play", "pause"]:
            return ResponseModel(
                success=False,
                response="Ação inválida. Use 'play' para tocar ou 'pause' para pausar."
            )

        token = authenticate_spotify()
        access_token = token if isinstance(token, str) else token.get("access_token")

        if not access_token:
            return ResponseModel(success=False, response="Erro: Token de autenticação não encontrado.")

        url = f"https://api.spotify.com/v1/me/player/{action}"
        if device_id:
            url += f"?device_id={device_id}"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.put(url, headers=headers)

        if response.status_code in [200, 204, 202]:
            msg = "Música retomada com sucesso." if action == "play" else "Música pausada com sucesso."
            return ResponseModel(success=True, response=msg)
        elif response.status_code == 403:
            return ResponseModel(success=False, response="Não há player ativo ou permissões insuficientes.")
        else:
            return ResponseModel(
                success=False,
                response=f"Erro ao executar ação '{action}': {response.status_code} - {response.text}"
            )

    except requests.exceptions.RequestException as e:
        return ResponseModel(success=False, response=f"Erro de comunicação com a API do Spotify: {str(e)}")
    except Exception as e:
        return ResponseModel(success=False, response=f"Ocorreu um erro inesperado: {str(e)}")
