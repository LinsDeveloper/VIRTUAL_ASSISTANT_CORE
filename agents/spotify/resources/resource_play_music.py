import requests
from agents.spotify.auth.spotify_auth import authenticate_spotify

def play_specific_song(artist_name, track_name, device_id=None):
    token = authenticate_spotify()
    search_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": f"track:{track_name} artist:{artist_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    tracks = results.get('tracks', {}).get('items', [])
    if not tracks:
        print("Música não encontrada.")
        return

    track_uri = tracks[0]['uri']

    play_url = "https://api.spotify.com/v1/me/player/play"
    if device_id:
        play_url += f"?device_id={device_id}"
    play_data = {
        "uris": [track_uri]
    }
    play_response = requests.put(play_url, headers=headers, json=play_data)
    if play_response.status_code == 204:
        print(f"Tocando '{track_name}' de '{artist_name}'.")
    else:
        print("Não foi possível iniciar a reprodução:", play_response.text)
        
        
def play_pause_music(action="play", device_id=None):
    """
    Controla a reprodução da música (play ou pause) no Spotify.
    """
    if action not in ["play", "pause"]:
        print("Ação inválida. Use 'play' ou 'pause'.")
        return

    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/me/player/{action}"
    if device_id:
        url += f"?device_id={device_id}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(url, headers=headers)

    if response.status_code in [204, 202]:
        print(f"Música {('tocando' if action == 'play' else 'pausada')}.")
    else:
        print(f"Não foi possível {action} a música:", response.text)
