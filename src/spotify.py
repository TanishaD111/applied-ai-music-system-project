import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def enrich_songs(songs: list[dict]) -> list[dict]:
    track_ids = [s["track_id"] for s in songs if "track_id" in s]

    if not track_ids:
        return songs

    try:
        results = client.tracks(track_ids)
        track_data = {t["id"]: t for t in results["tracks"] if t}

        for song in songs:
            track = track_data.get(song.get("track_id"))
            if track:
                images = track.get("album", {}).get("images", [])
                song["album_art"] = images[0]["url"] if images else None
                song["spotify_url"] = track["external_urls"].get("spotify")
                song["preview_url"] = track.get("preview_url")

    except Exception:
        # API unavailable (e.g. no premium) — fall back to constructing links directly
        for song in songs:
            track_id = song.get("track_id")
            if track_id:
                song["spotify_url"] = f"https://open.spotify.com/track/{track_id}"

    return songs
