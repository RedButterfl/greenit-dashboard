import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pandas as pd
from calculator import compute_it_score, compute_trend, get_ranking

SAMPLE = pd.DataFrame([
    {"country":"France","year":2020,"co2_per_capita":4.1,"it_co2_per_capita":0.131,"gdp_per_capita":39000},
    {"country":"France","year":2021,"co2_per_capita":3.9,"it_co2_per_capita":0.125,"gdp_per_capita":40000},
    {"country":"USA","year":2020,"co2_per_capita":14.9,"it_co2_per_capita":0.566,"gdp_per_capita":55000},
    {"country":"USA","year":2021,"co2_per_capita":14.2,"it_co2_per_capita":0.540,"gdp_per_capita":57000},
])

def test_compute_it_score_adds_columns():
    result = compute_it_score(SAMPLE)
    assert "it_co2_share_pct" in result.columns
    assert "co2_per_gdp" in result.columns

def test_it_share_range():
    result = compute_it_score(SAMPLE)
    assert (result["it_co2_share_pct"] > 0).all()
    assert (result["it_co2_share_pct"] < 100).all()

def test_trend_france_decreasing():
    enriched = compute_it_score(SAMPLE)
    trend = compute_trend(enriched, "France")
    assert trend["direction"] == "baisse"
    assert trend["trend_pct"] < 0

def test_ranking_ordered():
    enriched = compute_it_score(SAMPLE)
    ranking = get_ranking(enriched, 2020)
    assert ranking.iloc[0]["country"] == "USA"  # USA > France en CO2

def test_ranking_empty_year():
    enriched = compute_it_score(SAMPLE)
    ranking = get_ranking(enriched, 1900)
    assert len(ranking) == 0
