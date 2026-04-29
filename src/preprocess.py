import pandas as pd

INPUT_PATH = "data/dataset.csv"
OUTPUT_PATH = "data/dataset_clean.csv"

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

def popularity_label(val):
    if val < 20:
        return "obscure"
    elif val < 40:
        return "emerging"
    elif val < 60:
        return "moderately popular"
    elif val < 80:
        return "popular"
    return "very popular"

def acousticness_label(val):
    if val >= 0.6:
        return "acoustic"
    return "electronic"

def instrumentalness_label(val):
    if val >= 0.5:
        return "instrumental"
    return "vocal"

def speechiness_label(val):
    if val >= 0.66:
        return "spoken word"
    elif val >= 0.33:
        return "rap or spoken elements"
    return "sung"

def build_text(row):
    return (
        f"{row['track_name']} by {row['artists']} is a "
        f"{energy_label(row['energy'])}, {mood_label(row['valence'])}, "
        f"and {danceability_label(row['danceability'])} {row['track_genre']} track. "
        f"It has a {tempo_label(row['tempo'])} tempo and sounds {acousticness_label(row['acousticness'])}. "
        f"It is {instrumentalness_label(row['instrumentalness'])} with {speechiness_label(row['speechiness'])} style vocals. "
        f"It is {popularity_label(row['popularity'])}."
    )

def main():
    # Step 1: Load the raw dataset
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded {len(df)} rows")

    # Step 2: Drop rows missing track_name or artists (1 known null row)
    df = df.dropna(subset=["track_name", "artists"])
    print(f"After dropping nulls: {len(df)} rows")

    # Step 3: Deduplicate by track_id — same song appears across multiple genres, keep first occurrence
    df = df.drop_duplicates(subset=["track_id"], keep="first")
    print(f"After deduplication: {len(df)} rows")

    # Step 4: Build text field for embedding
    df["text"] = df.apply(build_text, axis=1)

    # Step 5: Save the clean dataset
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved clean dataset to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
