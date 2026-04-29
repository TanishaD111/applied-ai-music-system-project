import os
import pandas as pd
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "my-music-recommender"
BATCH_SIZE = 200

def ingest():
    # Load clean dataset
    df = pd.read_csv("data/dataset_clean.csv")
    print(f"Loaded {len(df)} songs")

    # Load embedding model locally — no API calls, no rate limits
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded")

    # Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)
    print(f"Connected to Pinecone index: {INDEX_NAME}")

    # Embed and upload in batches
    total = len(df)
    for i in range(0, total, BATCH_SIZE):
        batch = df.iloc[i : i + BATCH_SIZE]

        # Embed the text field locally
        texts = batch["text"].tolist()
        vectors = model.encode(texts, show_progress_bar=False)

        # Build records for Pinecone
        records = [
            (
                str(row["track_id"]),
                vectors[j].tolist(),
                {
                    "track_name": row["track_name"],
                    "artists": row["artists"],
                    "album_name": str(row["album_name"]),
                    "track_genre": row["track_genre"],
                    "popularity": int(row["popularity"]),
                }
            )
            for j, (_, row) in enumerate(batch.iterrows())
        ]

        index.upsert(vectors=records, namespace="music")
        print(f"Uploaded {min(i + BATCH_SIZE, total)}/{total} songs")

    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()
