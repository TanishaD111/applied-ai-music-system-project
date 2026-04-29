# 🎵 VibeFind: A Music Recommender

## Demo Video

<video src="assets/demo.mp4" controls width="100%"></video>

## Original Project

**Base Project:** [\[MyJammer Recommender Base Project\]](https://github.com/TanishaD111/ai110-module3show-musicrecommendersimulation-starter)

MyJammer is a rule-based music recommender that scores every song in a 20-song catalog against a user's taste profile using six features — genre, mood, energy, valence, danceability, and acousticness — and returns the top 5 matches. The scoring recipe awards categorical matches (genre: 3pts, mood: 2pts) and proximity-based points for numeric features, with a maximum of 9.0 points per song. The goal of the project is to simulate how real recommender systems turn structured data into ranked predictions, and to surface the design tradeoffs — like weighting and feature selection — that shape what users actually see.

---

## Title and Summary

**RAG Music Recommender** is an AI-powered music discovery app that understands what you're looking for in natural language and recommends real songs that match your vibe — complete with album art and direct Spotify links.

Instead of keyword search, the app uses **Retrieval-Augmented Generation (RAG)**: it finds semantically similar songs from a database of 89,740 Spotify tracks, then uses an LLM to write a warm, conversational recommendation explaining why each song fits your request.

---

## Architecture Overview

The system has two phases:

**Data Pipeline (one-time setup)**
The raw Spotify dataset is cleaned and preprocessed into human-readable descriptions for each song (e.g. *"high energy, happy, and danceable dance track with a fast tempo"*). These descriptions are embedded into vectors using Sentence Transformers and stored in a Pinecone vector database.

**Runtime Query Flow**
When a user types a query, it is embedded using the same model and compared against all stored song vectors. The top 5 closest matches are retrieved from Pinecone, enriched with album art and Spotify links via the Spotify API, and passed to Groq's LLM which generates a natural language recommendation.

See [assets/system_diagram.md](assets/system_diagram.md) for the full system diagram.

---

## Setup Instructions

### Prerequisites
- Python 3.9+
- A [Pinecone](https://pinecone.io) account (free)
- A [Groq](https://console.groq.com) account (free)
- A [Spotify Developer](https://developer.spotify.com) account (free)

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd applied-ai-music-system-project
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
```

### 5. Create a Pinecone index
In your Pinecone dashboard create an index named `my-music-recommender` with:
- **Dimensions:** 384
- **Metric:** cosine
- **Cloud:** AWS us-east-1

### 6. Preprocess the dataset
Download the [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) and place it at `data/dataset.csv`, then run:
```bash
python src/preprocess.py
```

### 7. Ingest songs into Pinecone
```bash
python src/ingest.py
```
This embeds all 89,740 songs locally and uploads them to Pinecone. Expect 20-40 minutes.

### 8. Run the app
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 9. Run tests
```bash
pytest tests/
```

---

## Sample Interactions

### Example 1
**Input:** `happy upbeat songs to work out to`

**Output:**
> I've got the perfect playlist to power up your workout! **Good Feeling by Flo Rida** is a high-energy dance track guaranteed to keep your motivation high. **Happier by Marshmello & Bastille** brings an infectious feel-good energy that's perfect for pushing through a tough set. **Gabbers Unite by 3 Steps Ahead** is a fast, danceable banger that'll keep your heart rate up from start to finish...

---

### Example 2
**Input:** `sad slow acoustic songs for a rainy day`

**Output:**
> Here are some songs perfect for a quiet, rainy afternoon. **Ghost - Acoustic by Ben Woodward** is a slow, melancholic ballad that feels tailor-made for grey skies. **To Begin Again by Ingrid Michaelson & ZAYN** is a gentle, emotional duet with soft acoustic tones that captures the bittersweet feeling of a rainy day perfectly...

---

### Example 3
**Input:** `chill instrumental jazz to study to`

**Output:**
> These tracks are perfect for staying focused and relaxed. **[Song name]** is a smooth, low-energy instrumental track with a mid-tempo groove that fades into the background beautifully while you work...

---

## Design Decisions

**Why RAG instead of a simple search?**
Keyword search would only match exact words. RAG understands meaning — a user typing "music for a lazy Sunday" can match songs described as "low energy, slow, acoustic" without those exact words appearing in the query.

**Why Sentence Transformers instead of a hosted embedding model?**
We initially used Pinecone's integrated `llama-text-embed-v2` model but hit the free tier's monthly token limit (5M tokens) during re-ingestion. Switching to `all-MiniLM-L6-v2` via Sentence Transformers runs fully locally — no API calls, no limits, no cost.

**Why Groq instead of OpenAI or Anthropic?**
Groq's free tier is generous and their `llama-3.1-8b-instant` model is fast and capable enough for conversational music recommendations without any cost.

**Why preprocess labels instead of raw numbers?**
Spotify's audio features are decimals (e.g. `energy: 0.82`, `valence: 0.14`). Converting these to natural language labels (`high energy`, `sad`) before embedding means user queries like "sad songs" match semantically rather than requiring the model to infer meaning from numbers.

**Trade-offs:**
- Sentence Transformers is slower to embed locally than a hosted model, but removes all API rate limits
- `llama3-8b` is a smaller model — responses are fast but occasionally generic
- Ingestion takes 20-40 minutes but only needs to run once

---

## Testing Summary

**What worked:**
- Unit tests for all label conversion functions in `preprocess.py` pass reliably — 17 tests covering energy, mood, tempo, danceability, popularity, acousticness, instrumentalness, and speechiness labels
- Logging captures every query, retrieved songs, and errors in `logs/app.log`
- Confidence scoring classifies match quality (🟢 High / 🟡 Medium / 🔴 Low) based on Pinecone similarity scores
- Deduplication in `retriever.py` prevents the same song appearing twice in results

**What didn't:**
- Similarity scores sit around 0.35-0.45 (Medium confidence) — this is a known limitation of matching natural language queries against structured song descriptions. The gap between how users describe music and how songs are indexed is hard to fully close without lyrics data or a domain-specific embedding model.
- Artist-specific searches (e.g. "songs by Taylor Swift") work partially but are not guaranteed — semantic search is better suited for vibe-based queries than exact name lookups.

**What I learned:**
- Hosted embedding APIs have usage limits that become a real constraint at scale — local embeddings are more sustainable for large datasets
- The quality of the text field used for embedding matters enormously — converting raw numbers to natural language labels meaningfully improves retrieval relevance

---

## Reflection

Building this project taught me that AI systems are only as good as the data pipeline behind them. The most impactful decisions weren't about which LLM to use — they were about how to represent data so the model could understand it. Converting Spotify's numeric audio features into natural language descriptions was a small change that made a large difference in search quality.

I also learned the practical realities of working with third-party APIs: rate limits, deprecated models, and free tier constraints are real engineering problems, not just footnotes. Switching from a hosted embedding model to Sentence Transformers mid-project taught me why production systems favour infrastructure they control over vendor-managed services.

RAG as a pattern showed me how to give an LLM grounding in real, specific data rather than relying on its training knowledge alone — making responses more accurate, relevant, and trustworthy.
