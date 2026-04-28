import os
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "music-recommender"
TOP_K = 10

def retrieve(query: str) -> list[dict]:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    # Fetch more than needed so we still have 5 after deduplication
    results = index.search(
        namespace="music",
        query={"inputs": {"text": query}, "top_k": TOP_K},
        fields=["track_name", "artists", "album_name", "track_genre", "popularity"]
    )

    songs = []
    seen = set()
    for hit in results["result"]["hits"]:
        key = (hit["fields"]["track_name"].lower(), hit["fields"]["artists"].lower())
        if key in seen:
            continue
        seen.add(key)
        songs.append({
            "track_name": hit["fields"]["track_name"],
            "artists": hit["fields"]["artists"],
            "album_name": hit["fields"]["album_name"],
            "track_genre": hit["fields"]["track_genre"],
            "popularity": hit["fields"]["popularity"],
            "score": round(hit["_score"], 3),
        })
        if len(songs) == 5:
            break

    return songs
