import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from parser import load_data, get_countries, get_years, filter_data
from calculator import compute_it_score, compute_trend, get_ranking

st.set_page_config(
    page_title="GreenIT Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 GreenIT Dashboard")
st.caption("Empreinte carbone du numérique par pays — projet portfolio Wavestone SEF")

# --- Chargement ---
@st.cache_data
def load():
    df = load_data()
    return compute_it_score(df)

df = load()
all_countries = get_countries(df)
all_years = get_years(df)

# --- Sidebar filtres ---
with st.sidebar:
    st.header("Filtres")
    selected_countries = st.multiselect(
        "Pays", all_countries, default=["France","Germany","USA","China"]
    )
    year_range = st.slider(
        "Période", min_value=all_years[0], max_value=all_years[-1],
        value=(all_years[0], all_years[-1])
    )
    selected_year = st.selectbox("Année de référence (classement)", all_years, index=len(all_years)-1)
    st.divider()
    st.markdown("**Stack technique**")
    st.markdown("Python · Streamlit · Plotly · GitHub Actions · AWS EC2")

if not selected_countries:
    st.warning("Sélectionnez au moins un pays dans le panneau gauche.")
    st.stop()

filtered = filter_data(df, selected_countries, year_range)

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
latest = filtered[filtered["year"] == filtered["year"].max()]
avg_co2 = latest["co2_per_capita"].mean()
avg_it = latest["it_co2_per_capita"].mean()
avg_share = latest["it_co2_share_pct"].mean()
n_countries = latest["country"].nunique()

col1.metric("Pays analysés", n_countries)
col2.metric("CO₂/hab moyen", f"{avg_co2:.1f} t")
col3.metric("CO₂ IT/hab moyen", f"{avg_it:.3f} t")
col4.metric("Part numérique", f"{avg_share:.1f}%")

st.divider()

# --- Graphique 1 : évolution CO2 total ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Évolution CO₂/hab")
    fig1 = px.line(
        filtered, x="year", y="co2_per_capita", color="country",
        labels={"co2_per_capita": "tCO₂/hab", "year": "Année", "country": "Pays"},
        markers=True
    )
    fig1.update_layout(height=350, legend=dict(orientation="h", y=-0.25))
    st.plotly_chart(fig1, use_container_width=True)

# --- Graphique 2 : part IT ---
with col_b:
    st.subheader("Part numérique dans les émissions")
    latest_sorted = latest.sort_values("it_co2_share_pct", ascending=True)
    fig2 = px.bar(
        latest_sorted, x="it_co2_share_pct", y="country", orientation="h",
        color="it_co2_share_pct", color_continuous_scale="Greens",
        labels={"it_co2_share_pct": "% du CO₂ total", "country": "Pays"}
    )
    fig2.update_layout(height=350, coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# --- Tableau classement ---
st.subheader(f"Classement {selected_year}")
ranking = get_ranking(filtered[filtered["year"] == selected_year], selected_year)
if ranking.empty:
    st.info("Aucune donnée pour cette sélection.")
else:
    ranking.columns = ["Pays","CO₂/hab (t)","CO₂ IT/hab (t)","Part numérique (%)"]
    st.dataframe(ranking, use_container_width=True, hide_index=True)

# --- Analyse tendances ---
st.subheader("Analyse des tendances")
trend_cols = st.columns(len(selected_countries))
for i, country in enumerate(selected_countries):
    trend = compute_trend(filtered, country)
    icon = "📉" if trend["direction"] == "baisse" else "📈" if trend["direction"] == "hausse" else "➡️"
    trend_cols[i].metric(
        country,
        f"{icon} {trend['direction']}",
        f"{trend['trend_pct']:+.1f}% sur la période"
    )

# --- Note conseil ---
with st.expander("💡 Cadrage consultant — Comment utiliser cet outil en mission ?"):
    st.markdown("""
**Contexte business** : La directive CSRD (2024) impose aux grandes entreprises un reporting ESG incluant
l'empreinte numérique. Ce dashboard outille la phase de diagnostic.

**Hypothèses du modèle** :
- Données CO₂ : simulées à partir d'ordres de grandeur Our World in Data
- Part IT : estimée à 2–4% des émissions totales selon les études GeSI/Shift Project
- Facteur d'émission : 0,233 kgCO₂e/kWh (moyenne mondiale IEA 2022)

**Limites** : périmètre national (Scope 2), pas de décomposition usage/fabrication/réseau.

**En mission réelle**, ce diagnostic serait complété par : collecte des données SI client (GLPI, inventaire),
interview des équipes IT, benchmark sectoriel, puis feuille de route d'amélioration priorisée.
    """)

st.caption("Projet portfolio — Steves D. | Stack : Python 3.11 · Streamlit · Plotly · GitHub Actions · AWS EC2")
