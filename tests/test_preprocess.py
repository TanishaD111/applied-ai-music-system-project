from src.preprocess import (
    energy_label, danceability_label, mood_label, tempo_label,
    popularity_label, acousticness_label, instrumentalness_label,
    speechiness_label, build_text
)

class TestEnergyLabel:
    def test_low_energy(self):
        assert energy_label(0.1) == "low energy"
        assert energy_label(0.0) == "low energy"
        assert energy_label(0.32) == "low energy"

    def test_moderate_energy(self):
        assert energy_label(0.33) == "moderate energy"
        assert energy_label(0.5) == "moderate energy"
        assert energy_label(0.65) == "moderate energy"

    def test_high_energy(self):
        assert energy_label(0.66) == "high energy"
        assert energy_label(0.9) == "high energy"
        assert energy_label(1.0) == "high energy"

class TestMoodLabel:
    def test_sad(self):
        assert mood_label(0.0) == "sad"
        assert mood_label(0.2) == "sad"
        assert mood_label(0.32) == "sad"

    def test_neutral(self):
        assert mood_label(0.33) == "neutral mood"
        assert mood_label(0.5) == "neutral mood"
        assert mood_label(0.65) == "neutral mood"

    def test_happy(self):
        assert mood_label(0.66) == "happy"
        assert mood_label(0.9) == "happy"
        assert mood_label(1.0) == "happy"

class TestTempoLabel:
    def test_slow(self):
        assert tempo_label(60) == "slow"
        assert tempo_label(89) == "slow"

    def test_mid_tempo(self):
        assert tempo_label(90) == "mid-tempo"
        assert tempo_label(100) == "mid-tempo"
        assert tempo_label(119) == "mid-tempo"

    def test_fast(self):
        assert tempo_label(120) == "fast"
        assert tempo_label(180) == "fast"

class TestDanceabilityLabel:
    def test_not_danceable(self):
        assert danceability_label(0.1) == "not danceable"
        assert danceability_label(0.39) == "not danceable"

    def test_moderately_danceable(self):
        assert danceability_label(0.40) == "moderately danceable"
        assert danceability_label(0.55) == "moderately danceable"

    def test_danceable(self):
        assert danceability_label(0.70) == "danceable"
        assert danceability_label(0.95) == "danceable"

class TestPopularityLabel:
    def test_obscure(self):
        assert popularity_label(0) == "obscure"
        assert popularity_label(19) == "obscure"

    def test_emerging(self):
        assert popularity_label(20) == "emerging"
        assert popularity_label(39) == "emerging"

    def test_moderately_popular(self):
        assert popularity_label(40) == "moderately popular"
        assert popularity_label(59) == "moderately popular"

    def test_popular(self):
        assert popularity_label(60) == "popular"
        assert popularity_label(79) == "popular"

    def test_very_popular(self):
        assert popularity_label(80) == "very popular"
        assert popularity_label(100) == "very popular"

class TestAcousticnessLabel:
    def test_acoustic(self):
        assert acousticness_label(0.6) == "acoustic"
        assert acousticness_label(0.9) == "acoustic"

    def test_electronic(self):
        assert acousticness_label(0.5) == "electronic"
        assert acousticness_label(0.1) == "electronic"

class TestInstrumentalnessLabel:
    def test_instrumental(self):
        assert instrumentalness_label(0.5) == "instrumental"
        assert instrumentalness_label(0.9) == "instrumental"

    def test_vocal(self):
        assert instrumentalness_label(0.4) == "vocal"
        assert instrumentalness_label(0.0) == "vocal"

class TestSpeechinessLabel:
    def test_spoken_word(self):
        assert speechiness_label(0.66) == "spoken word"
        assert speechiness_label(0.9) == "spoken word"

    def test_rap_or_spoken(self):
        assert speechiness_label(0.33) == "rap or spoken elements"
        assert speechiness_label(0.5) == "rap or spoken elements"

    def test_sung(self):
        assert speechiness_label(0.1) == "sung"
        assert speechiness_label(0.32) == "sung"

class TestBuildText:
    def test_build_text_format(self):
        row = {
            "track_name": "Test Song",
            "artists": "Test Artist",
            "track_genre": "pop",
            "energy": 0.8,
            "danceability": 0.75,
            "valence": 0.2,
            "tempo": 130,
            "popularity": 80,
            "acousticness": 0.2,
            "instrumentalness": 0.1,
            "speechiness": 0.05,
        }
        result = build_text(row)
        assert "Test Song" in result
        assert "Test Artist" in result
        assert "high energy" in result
        assert "danceable" in result
        assert "sad" in result
        assert "fast" in result
        assert "very popular" in result
        assert "electronic" in result
        assert "vocal" in result
        assert "sung" in result
