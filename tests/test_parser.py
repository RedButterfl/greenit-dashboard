import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest, pandas as pd
from pathlib import Path
from parser import load_data, get_countries, get_years, filter_data

DATA = Path(__file__).parent.parent / "data" / "emissions.csv"

def test_load_data_shape():
    df = load_data(DATA)
    assert len(df) == 90
    assert "country" in df.columns

def test_get_countries_sorted():
    df = load_data(DATA)
    countries = get_countries(df)
    assert countries == sorted(countries)
    assert "France" in countries

def test_filter_data():
    df = load_data(DATA)
    filtered = filter_data(df, ["France","Germany"], (2018, 2020))
    assert set(filtered["country"]) == {"France","Germany"}
    assert filtered["year"].min() >= 2018
    assert filtered["year"].max() <= 2020

def test_missing_column_raises():
    bad_df = pd.DataFrame({"country":["France"],"year":[2020]})
    with pytest.raises(ValueError):
        from parser import load_data as ld
        import io, csv, tempfile
        tmp = tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False)
        bad_df.to_csv(tmp.name, index=False)
        ld(Path(tmp.name))
