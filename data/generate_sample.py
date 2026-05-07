import pandas as pd
import numpy as np
import os

np.random.seed(42)
countries = ["France","Germany","USA","China","India","Brazil","UK","Japan","Australia","Spain"]
years = list(range(2015, 2024))
base_co2 = {"France":4.1,"Germany":8.9,"USA":14.9,"China":7.4,"India":1.9,
            "Brazil":2.4,"UK":5.4,"Japan":8.5,"Australia":15.0,"Spain":5.8}
it_share = {"France":0.032,"Germany":0.028,"USA":0.038,"China":0.025,"India":0.018,
            "Brazil":0.022,"UK":0.035,"Japan":0.031,"Australia":0.041,"Spain":0.026}
rows = []
for country in countries:
    for year in years:
        trend = 1 - 0.015*(year-2015)
        co2 = base_co2[country]*trend*np.random.uniform(0.97,1.03)
        it_co2 = co2*it_share[country]*np.random.uniform(0.95,1.05)
        rows.append({"country":country,"year":year,
                     "co2_per_capita":round(co2,3),
                     "it_co2_per_capita":round(it_co2,4),
                     "gdp_per_capita":round(np.random.uniform(20000,60000),0)})
df = pd.DataFrame(rows)
out = os.path.join(os.path.dirname(__file__),"emissions.csv")
df.to_csv(out,index=False)
print(f"Generated {len(df)} rows -> {out}")
