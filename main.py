import spotipy
from spotipy.oauth2 import SpotifyOAuth
from client_secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from datetime import datetime
from dateutil.relativedelta import relativedelta

SCOPE = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


def chunk_list(lst, size=50):
    """Rozdělí seznam na části po velikosti `size` (Spotify limit = 100)."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def add_to_playlist(track_uris, playlist_id):
    """
    Přidá skladby do existujícího playlistu.
    """
    try:
        for chunk in chunk_list(track_uris):
            sp.playlist_add_items(playlist_id, chunk)
        print(f"✅ Přidáno {len(track_uris)} skladeb do playlistu {playlist_id}")
    except Exception as e:
        print(f"❌ Chyba při přidávání skladeb do playlistu: {e}")

def create_playlist(name, private=True, description=""):
    try:
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(
            user=user_id,
            name=name,
            public=not private,
            description=description
        )
        print(f"🎵 Playlist '{name}' vytvořen (ID: {playlist['id']})")
        return playlist['id']
    except Exception as e:
        print(f"❌ Chyba při vytváření playlistu: {e}")
        return None

def new_playlist(track_uris, name, private=True, description=""):
    """
    Vytvoří nový playlist a přidá do něj skladby.
    """
    try:
        playlist_id = create_playlist(name, private, description)
        if playlist_id:
            add_to_playlist(track_uris, playlist_id)
        return playlist_id
    except Exception as e:
        print(f"❌ Chyba při přidávání skladeb do playlistu: {e}")
        return None


# --- PŘIDANÁ FUNKCE PRO FILTRACI SKLADEB ---
def get_saved_tracks_by_date(date_from, date_to):
    """
    Projde Oblíbené skladby a vrátí URI těch, které byly přidány v daném rozmezí.
    """
    track_uris = []
    results = sp.current_user_saved_tracks(limit=50)
    
    date_is_over_given_minimum = True
    
    while results and date_is_over_given_minimum:
        for item in results['items']:
            # Datum ze Spotify přichází ve formátu "2023-10-25T12:34:56Z"
            date_added_string = item['added_at']
            date_added = datetime.strptime(date_added_string, "%Y-%m-%dT%H:%M:%SZ")
            
            # Spotify řadí od nejnovějších. Pokud narazíme na moc starou, můžeme rovnou končit.
            if date_added < date_from:
                date_is_over_given_minimum = False
                break
                
            if date_added < date_to:
                track_uris.append(item['track']['uri'])
        
        # Načtení další stránky, pokud ještě nejsme u konce a nepodlezli jsme datum
        if date_is_over_given_minimum and results['next']:
            results = sp.next(results)
        else:
            results = None
            
    return track_uris


#=======MAIN===========
if __name__ == "__main__":
    load_df = "%d.%m.%Y"

    D0S = input("Zadej počáteční datum ve formátu 24.12.2000: (ENTER pro začátek tohoto měsíce)\t")
    D1S = input("Zadej koncové datum ve formátu 24.12.2000: (ENTER pro konec tohoto měsíce)\t")

    D0 = datetime.strptime(D0S, load_df) if D0S else datetime(datetime.now().year, datetime.now().month, 1)
    D1 = datetime.strptime(D1S, load_df) if D1S else datetime(datetime.now().year, datetime.now().month + 1, 1)

    # Vytvoření názvu playlistu podle staré logiky
    if D1 == D0 + relativedelta(months=1) and D0.day == 1:
        playlist_name = D0.strftime('%m/%Y') + " liked songs"
    else:
        playlist_name = D0.strftime("%d/%m/%Y") + " - " + D1.strftime("%d/%m/%Y") + " liked songs"
    
    description = f"{playlist_name} by custom spotipy program"

    print("⏳ Hledám skladby podle data, může to chvíli trvat...")
    tracks_to_add = get_saved_tracks_by_date(D0, D1)
    
    if not tracks_to_add:
        print("🤷♂️ V tomto období nebyly přidány žádné skladby.")
    else:
        print(f"🔍 Nalezeno {len(tracks_to_add)} skladeb. Vytvářím playlist...")
        my_playlist_id = new_playlist(tracks_to_add, playlist_name, private=True, description=description)
        print(f"🔗 Odkaz na playlist: https://open.spotify.com/playlist/{my_playlist_id}")