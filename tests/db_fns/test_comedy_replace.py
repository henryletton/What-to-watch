import pytest
from src.db_fns import create_engine2, search_film

# Check "comedy" is replaced correctly"
def test_for_comedy_replace():
    engine = create_engine2()
    search_df = search_film(engine, "Addams Family Values", "comedy")
    assert "Addams Family Values" in search_df["title"].values

# Check "comedies" is replaced correctly"
def test_for_comedies_replace():
    engine = create_engine2()
    search_df = search_film(engine, "The IT Crowd", "comedy")
    assert "The IT Crowd" in search_df["title"].values

