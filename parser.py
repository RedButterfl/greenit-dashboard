import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "emissions.csv"

def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    expected = {"country","year","co2_per_capita","it_co2_per_capita","gdp_per_capita"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes: {missing}")
    df["year"] = df["year"].astype(int)
    return df

def get_countries(df: pd.DataFrame) -> list:
    return sorted(df["country"].unique().tolist())

def get_years(df: pd.DataFrame) -> list:
    return sorted(df["year"].unique().tolist())

def filter_data(df: pd.DataFrame, countries: list, year_range: tuple) -> pd.DataFrame:
    return df[
        df["country"].isin(countries) &
        df["year"].between(year_range[0], year_range[1])
    ].copy()
