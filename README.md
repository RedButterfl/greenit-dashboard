# 🌱 GreenIT Dashboard

> **Projet portfolio**  Empreinte carbone du numérique · Python · Streamlit · GitHub Actions · AWS

---

## Contexte business

La directive CSRD (2024) impose aux grandes entreprises un reporting ESG couvrant l'impact environnemental
du numérique. Ce dashboard prototype la phase de **diagnostic d'empreinte carbone IT** telle qu'un
consultant CTO l'outillerait en mission.

**Enjeux adressés :**
- Visualiser les émissions CO₂ IT par pays et par période
- Identifier les pays à fort potentiel de réduction
- Fournir une base de benchmarking pour les plans de réduction

---

## Architecture

```
greenit-dashboard/
├── data/
│   ├── emissions.csv          # Données CO₂ (simulées d'après Our World in Data)
│   └── generate_sample.py     # Script de génération
├── parser.py                  # Chargement et filtrage des données
├── calculator.py              # Calcul des scores CO₂ et tendances
├── dashboard.py               # Interface Streamlit
├── tests/
│   ├── test_parser.py
│   └── test_calculator.py
├── .github/workflows/
│   └── deploy.yml             # Pipeline CI/CD (test → deploy EC2)
└── requirements.txt
```

**Stack :** Python 3.14.4 · Streamlit · Plotly · Pandas · pytest · GitHub Actions · AWS EC2 (Free Tier)

---

## Lancer le projet en local

```bash
git clone https://github.com/<ton-user>/greenit-dashboard.git
cd greenit-dashboard
pip install -r requirements.txt
streamlit run dashboard.py
```

Dashboard accessible sur `http://localhost:8501`

---

## Tests

```bash
pytest tests/ -v
```

9 tests unitaires couvrant : chargement CSV, filtrage, calcul de score, tendances, classement.

---

## Pipeline CI/CD

Chaque `push` sur `main` déclenche automatiquement :
1. **Test**  `pytest` sur GitHub Actions
2. **Deploy**  SSH vers EC2, redémarrage de l'app Streamlit

Secrets nécessaires dans GitHub : `EC2_HOST`, `EC2_SSH_KEY`

---

## Hypothèses du modèle

| Paramètre | Valeur | Source |
|---|---|---|
| Part IT des émissions | 2–4% selon les pays | GeSI / Shift Project |
| Facteur d'émission | 0,233 kgCO₂e/kWh | IEA 2022 (moyenne mondiale) |
| Données CO₂ | Simulées (ordres de grandeur réels) | Our World in Data |

**Limites :** périmètre Scope 2 uniquement, agrégat national (pas de décomposition usage/fabrication/réseau).

---

## Et si c'était un vrai projet client ?

**Phase de cadrage (semaine 1–2) :**
- Définir le périmètre : SI interne seulement ou produits inclus ?
- Identifier les acteurs : DSI, DAF, équipe RSE, direction métier
- Collecter les données réelles : inventaire GLPI, factures énergie, contrats cloud

**Phase de diagnostic (semaine 3–4) :**
- Cartographier les postes d'émission (datacenter, postes, réseau, SaaS)
- Benchmark sectoriel
- Identifier les leviers de réduction (Green Cloud, éco-conception, obsolescence)

**Phase de plan d'action :**
- Priorisation par ratio impact/effort
- Feuille de route à 3 ans
- KPIs et gouvernance du suivi

---

*Auteur : Elsa MOUKOUDI. | INSA Lyon | Projet personnel*
