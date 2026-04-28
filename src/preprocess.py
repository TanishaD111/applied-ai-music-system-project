import pandas as pd

INPUT_PATH = "data/dataset.csv"
OUTPUT_PATH = "data/dataset_clean.csv"

# Step 1: Load the raw dataset
df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df)} rows")

# Step 2: Drop rows missing track_name or artists (1 known null row)
df = df.dropna(subset=["track_name", "artists"])
print(f"After dropping nulls: {len(df)} rows")

# Step 3: Deduplicate by track_id — same song appears across multiple genres, keep first occurrence
df = df.drop_duplicates(subset=["track_id"], keep="first")
print(f"After deduplication: {len(df)} rows")

# Step 4: Build a text field that describes each song in plain language
# This is what gets converted into an embedding vector for semantic search
def energy_label(val):
    if val < 0.33:
        return "low energy"
    elif val < 0.66:
        return "moderate energy"
    return "high energy"

def danceability_label(val):
    if val < 0.40:
        return "not danceable"
    elif val < 0.70:
        return "moderately danceable"
    return "danceable"

def mood_label(val):
    if val < 0.33:
        return "sad"
    elif val < 0.66:
        return "neutral mood"
    return "happy"

def tempo_label(val):
    if val < 90:
        return "slow"
    elif val < 120:
        return "mid-tempo"
    return "fast"

def build_text(row):
    return (
        f"{row['track_name']} by {row['artists']} | "
        f"Genre: {row['track_genre']} | "
        f"Energy: {energy_label(row['energy'])} | "
        f"Danceability: {danceability_label(row['danceability'])} | "
        f"Mood: {mood_label(row['valence'])} | "
        f"Tempo: {tempo_label(row['tempo'])} | "
        f"Popularity: {row['popularity']}"
    )

df["text"] = df.apply(build_text, axis=1)

# Step 5: Save the clean dataset
df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved clean dataset to {OUTPUT_PATH}")
