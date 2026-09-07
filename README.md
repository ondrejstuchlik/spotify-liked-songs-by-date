# Spotify Liked Songs by Date

A Python Spotipy script that filters your Spotify "Liked Songs" by a specific date range and automatically creates a new custom playlist from them. 

## Features & Functions

- Interactive CLI to set start and end dates (defaults to the current month).
- `get_saved_tracks_by_date()` fetches and filters saved tracks using Spotipy's pagination.
- `chunk_list()` splits track URIs into batches of 50 items to respect Spotify API limits.
- `create_playlist()` creates a private playlist for the authenticated user.
- `add_to_playlist()` safely populates the playlist in API-friendly batches.
- `new_playlist()` wraps the creation and population processes.

## Setup

1. Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Set the Redirect URI in your Spotify app settings to `http://127.0.0.1:8888/callback`.
3. Install dependencies:

   ```bash
   python -m pip install spotipy python-dateutil
   ```

4. Create a `client_secrets.py` file in the same directory and add your credentials:
   ```python
   CLIENT_ID = "your_client_id_here"
   CLIENT_SECRET = "your_client_secret_here"
   REDIRECT_URI = "http://127.0.0.1:8888/callback"
   ```

## Usage

Run the script directly from your terminal:

```bash
python main.py
```

The script will prompt you for a start and end date (format: `DD.MM.YYYY`). If you press `ENTER` without typing anything, it defaults to the beginning and end of the current month.

The first run will open your web browser for Spotify authorization. Spotipy will create a local `.cache` file with your token.

## Notes

- The script requires the `user-library-read` scope to access your Liked Songs.
- **Security Warning:** Never commit `client_secrets.py` or the Spotipy `.cache` file to version control. Always use a `.gitignore` file!
```
