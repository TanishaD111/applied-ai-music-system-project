import streamlit as st
from src.retriever import retrieve
from src.recommender import recommend
from src.spotify import enrich_songs

st.set_page_config(page_title="VibeFind", page_icon="🎵", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🎵 VibeFind</h1>
    <p style='text-align: center; color: gray; font-size: 18px;'>
        Describe the vibe you're looking for and get personalized song recommendations
    </p>
""", unsafe_allow_html=True)

st.divider()

query = st.text_input("Search", placeholder="e.g. sad slow songs for a rainy day", label_visibility="collapsed")

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    search = st.button("Find Songs", use_container_width=True)

def confidence_label(score: float) -> str:
    if score >= 0.50:
        return "🟢 High"
    elif score >= 0.35:
        return "🟡 Medium"
    return "🔴 Low"

if search and query.strip():
    with st.spinner("Finding songs for you..."):
        songs = retrieve(query)
        songs = enrich_songs(songs)
        recommendation = recommend(query, songs)

    st.divider()

    st.markdown("### 🎧 Your Recommendation")
    st.info(recommendation)

    st.markdown("### 🎼 Songs Retrieved")
    for song in songs:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                if song.get("album_art"):
                    st.image(song["album_art"], width=80)
                st.markdown(f"**{song['track_name']}**  \n{song['artists']}")
                st.caption(f"🎸 {song['track_genre'].title()}  •  💿 {song['album_name']}")
                if song.get("spotify_url"):
                    st.markdown(f"[▶ Listen on Spotify]({song['spotify_url']})")
            with col2:
                st.metric("Popularity", int(song['popularity']))
                st.caption(f"Match: {confidence_label(song['score'])} ({song['score']})")
