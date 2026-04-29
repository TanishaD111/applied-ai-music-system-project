# Model Card: VibeFind

## Responsible AI Reflection

### Limitations and Biases

VibeFind has several limitations worth acknowledging:

**Dataset bias:** The Spotify Tracks Dataset skews toward Western, English-language music. Users searching for regional genres, such as Afrobeats, K-pop, Latin trap, Bollywood, may receive weaker or irrelevant results because those genres are underrepresented in the training dataset.

**Popularity bias:** Songs with very low popularity scores (obscure or independent artists) are present in the dataset but may be ranked lower in results compared to mainstream tracks, since the embedding model has likely seen more text about popular artists during its own training.

**Vibe vs. artist search:** The system is designed for semantic, vibe-based queries. Searching for a specific artist by name works inconsistently, semantic search understands meaning, not exact name matching. A user asking for "Taylor Swift songs" may not reliably get Taylor Swift.

**Confidence scoring:** Similarity scores consistently sit in the medium range (0.35–0.45) regardless of how good the match actually is. This makes the confidence indicator less meaningful than intended, a 🟡 Medium score can still return a highly relevant result.

**No feedback loop:** The system has no way to learn from user preferences over time. It cannot improve based on whether a user liked or disliked a recommendation. This can be added in a future iteration with user feedback, such as thumbs up or down.

---

### Could VibeFind Be Misused?

The direct misuse risk for a music recommender is low, but there are scenarios worth considering:

**Content amplification:** The system could disproportionately surface certain artists or labels if the underlying dataset is skewed, unintentionally acting as a promotion tool rather than a neutral recommender.

**Mood manipulation:** A system that identifies and targets emotional states (e.g. "I'm feeling really low") could theoretically be used to serve music that deepens rather than helps those emotions. This is a broader concern with mood-aware AI systems.

**Prevention measures:**
- Be transparent about the data source and its limitations
- Avoid collecting or storing user queries beyond logging for debugging
- Do not build user profiles or track query history
- Keep the system's scope narrow — it recommends music, nothing more

---

### What Surprised Me During Testing

The biggest surprise was how well the system handled abstract, emotional queries even with moderate similarity scores. Queries like "music for a lazy Sunday morning" or "songs that feel like driving at night" returned results that genuinely matched the feeling, even though none of those exact words appeared in the song descriptions.

What didn't work as expected was the confidence scoring. I assumed higher-scoring results would feel more relevant and lower-scoring ones would feel off. In practice, the scores were clustered so tightly with the top 5 given that they didn't reliably distinguish a great match from a mediocre one. The scores reflect mathematical vector distance is what I learned, not human perception of relevance, and those two things are not the same. I changed from the llama model on Pinecone to sentence-transformers but still it did not increase confidence scores much higher. Though I did change from using pipes to natural language in the text field before running the embeddings. I think this improved the search results.

I also didn't anticipate hitting Pinecone's monthly embedding token limit mid-project. Having 89,740 songs re-embedded twice in one month exhausted the free tier entirely, but I was already planning to make a switch to local embeddings with Sentence Transformers. It was a good lesson about the real constraints of hosted AI APIs at scale.

---

### Collaboration With AI

This project was built through pair programming with Claude (Anthropic). Claude served as a technical collaborator throughout, explaining concepts, writing code, debugging errors, and suggesting architectural decisions.

**One instance where AI gave a helpful suggestion:**
When I asked whether to use pipe-separated text (`Energy: 0.46 | Valence: 0.12`) or human-readable labels (`high energy | sad`) in the song descriptions, Claude explained that embedding models are trained on natural language and would match user queries more accurately against descriptive words than raw numbers. This was non-obvious advice that meaningfully improved the quality of search results, converting decimals to labels like "sad", "danceable", and "slow" made vibe-based queries work much better.

**One instance where the AI's suggestion was flawed:**
Claude initially recommended using Pinecone's integrated `llama-text-embed-v2` model as the simpler option for embedding, noting it would reduce code complexity. While that was true, Claude did not adequately flag that the free tier had a hard monthly token limit of 5 million tokens. Uploading 89,740 songs twice (for re-ingestion after preprocessing improvements) hit that limit and broke the pipeline mid-run. The suggestion to use the hosted model was technically correct but incomplete — the practical consequence for a large dataset was a significant blocker that required switching the entire embedding approach. A more thorough recommendation would have included the token limit as a key trade-off upfront.
