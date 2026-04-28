import os
import time
import pandas as pd
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "music-recommender"
BATCH_SIZE = 50

def upsert_with_retry(index, records, retries=5):
    delay = 10
    for attempt in range(retries):
        try:
            index.upsert_records("music", records)
            return
        except Exception as e:
            if "429" in str(e) and attempt < retries - 1:
                print(f"Rate limited — waiting {delay}s before retry...")
                time.sleep(delay)
                delay *= 2
            else:
                raise

def ingest():
    # Load clean dataset
    df = pd.read_csv("data/dataset_clean.csv")
    print(f"Loaded {len(df)} songs")

    # Connect to Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)
    print(f"Connected to Pinecone index: {INDEX_NAME}")

    # Upload in batches — Pinecone embeds the text field using llama-text-embed-v2
    total = len(df)
    for i in range(0, total, BATCH_SIZE):
        batch = df.iloc[i : i + BATCH_SIZE]
        records = [
            {
                "_id": str(row["track_id"]),
                "text": row["text"],
                "track_name": row["track_name"],
                "artists": row["artists"],
                "album_name": str(row["album_name"]),
                "track_genre": row["track_genre"],
                "popularity": int(row["popularity"]),
            }
            for _, row in batch.iterrows()
        ]
        upsert_with_retry(index, records)
        print(f"Uploaded {min(i + BATCH_SIZE, total)}/{total} songs")
        time.sleep(2)

    print("Ingestion complete!")

if __name__ == "__main__":
    ingest()
