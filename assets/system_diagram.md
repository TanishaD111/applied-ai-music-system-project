flowchart TD
    subgraph Pipeline ["Data Pipeline (One-Time Setup)"]
        A[dataset.csv] --> B[preprocess.py]
        B --> C[dataset_clean.csv]
        C --> D[ingest.py + Sentence Transformers]
        D --> E[(Pinecone Vector DB)]
    end

    subgraph Runtime ["Runtime Query Flow"]
        F([User]) -->|types query| G[Streamlit UI]
        G --> H[retriever.py]
        H -->|embed query locally| H
        H -->|vector search| E
        E -->|top 5 songs| H
        H --> I[recommender.py]
        H --> J[spotify.py]
        I -->|calls Groq LLM| K[Groq API]
        J -->|fetches album art + links| L[Spotify API]
        K -->|recommendation text| G
        L -->|album art + Spotify links| G
        G -->|displays results| F
    end
