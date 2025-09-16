import requests
import base64


def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def search_artist_id(artist_name, access_token):
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': artist_name, 'type': 'artist', 'limit': 1}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    items = response.json()['artists']['items']
    return items[0]['id'] if items else None

def get_top_tracks(artist_id, access_token, market='US'):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'market': market}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['tracks']

def main():
    print("Autenticación en Spotify")
    print(f"print para saber tu client debes crear una app en https://developer.spotify.com/dashboard")
    client_id = input("Client ID: 7d5bfc37b91a4c2da76cda4c0656e15d")
    client_secret = input("Client Secret :cf90208191214a4881628c0e081a78f7 ")
    artist_name = input("Nombre del artista que querés buscar : ")
    market = input(" Código del mercado (ej: AR, US, MX) [US]: ") or "US"

    try:
        token = get_access_token(client_id, client_secret)
        artist_id = search_artist_id(artist_name, token)

        if not artist_id:
            print("No se encontró el artista.")
            return

        top_tracks = get_top_tracks(artist_id, token, market)

        if not top_tracks:
            print(f" El artista no tiene canciones populares en el mercado '{market}'.")
            return

        print(f"\n Top Tracks de {artist_name} en {market.upper()}:")
        for i, track in enumerate(top_tracks, 1):
            print(f"{i}. {track['name']} - {track['external_urls']['spotify']}")
    except requests.exceptions.RequestException as e:
        print("Error de conexión o autenticación:", e)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

if __name__ == "__main__":
    main()
