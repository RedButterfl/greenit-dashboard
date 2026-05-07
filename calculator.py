import pandas as pd

# Facteur d'emission moyen mondial (kgCO2e / kWh)
EMISSION_FACTOR_KWH = 0.233

def compute_it_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["it_co2_share_pct"] = (df["it_co2_per_capita"] / df["co2_per_capita"] * 100).round(2)
    df["co2_per_gdp"] = (df["co2_per_capita"] / df["gdp_per_capita"] * 1000).round(4)
    return df

def compute_trend(df: pd.DataFrame, country: str) -> dict:
    sub = df[df["country"] == country].sort_values("year")
    if len(sub) < 2:
        return {"trend_pct": 0.0, "direction": "stable"}
    first = sub.iloc[0]["co2_per_capita"]
    last = sub.iloc[-1]["co2_per_capita"]
    trend = (last - first) / first * 100
    direction = "baisse" if trend < -1 else "hausse" if trend > 1 else "stable"
    return {"trend_pct": round(trend, 2), "direction": direction}

def get_ranking(df: pd.DataFrame, year: int) -> pd.DataFrame:
    year_df = df[df["year"] == year].copy()
    return year_df.sort_values("co2_per_capita", ascending=False)[
        ["country","co2_per_capita","it_co2_per_capita","it_co2_share_pct"]
    ].reset_index(drop=True)
