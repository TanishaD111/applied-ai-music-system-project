import os
import logging
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "my-music-recommender"
TOP_K = 10

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query: str) -> list[dict]:
    logging.info(f"Query received: {query}")
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(INDEX_NAME)

        # Embed the query locally with the same model used during ingestion
        query_vector = model.encode(query).tolist()

        results = index.query(
            namespace="music",
            vector=query_vector,
            top_k=TOP_K,
            include_metadata=True
        )

        songs = []
        seen = set()
        for match in results["matches"]:
            meta = match["metadata"]
            key = (meta["track_name"].lower(), meta["artists"].lower())
            if key in seen:
                continue
            seen.add(key)
            songs.append({
                "track_id": match["id"],
                "track_name": meta["track_name"],
                "artists": meta["artists"],
                "album_name": meta["album_name"],
                "track_genre": meta["track_genre"],
                "popularity": meta["popularity"],
                "score": round(match["score"], 3),
            })
            if len(songs) == 5:
                break

        logging.info(f"Retrieved {len(songs)} songs: {[s['track_name'] for s in songs]}")
        return songs

    except Exception as e:
        logging.error(f"Retrieval failed: {e}")
        raise
