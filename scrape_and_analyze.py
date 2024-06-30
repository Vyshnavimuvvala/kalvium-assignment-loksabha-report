#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tables = soup.find_all("table")
party_results = []
for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if len(cols) == 4:
            party_results.append(cols)
df = pd.DataFrame(party_results, columns=["Party", "Won", "Leading", "Total"])
df["Won"] = pd.to_numeric(df["Won"], errors='coerce')
df["Leading"] = pd.to_numeric(df["Leading"], errors='coerce')
df["Total"] = pd.to_numeric(df["Total"], errors='coerce')
df.to_csv("lok_sabha_election_results_2024.csv", index=False)


# In[4]:


import pandas as pd
df = pd.read_csv("lok_sabha_election_results_2024.csv")
insights = {
    "total_seats": df["Total"].sum(),
    "bjp_seats": df[df["Party"] == "Bharatiya Janata Party - BJP"]["Total"].sum(),
    "congress_seats": df[df["Party"] == "Indian National Congress - INC"]["Total"].sum(),
    "top_5_parties": df.nlargest(5, "Total")[["Party", "Total"]].values.tolist(),
    "regional_parties": df[(df["Party"] != "Bharatiya Janata Party - BJP") & 
                           (df["Party"] != "Indian National Congress - INC")]["Party"].unique().tolist()
}
with open("insights.md", "w") as f:
    f.write("# Lok Sabha Election 2024 Insights\n")
    f.write(f"Total Seats: {insights['total_seats']}\n")
    f.write(f"BJP Seats: {insights['bjp_seats']}\n")
    f.write(f"Congress Seats: {insights['congress_seats']}\n")
    f.write("Top 5 Parties:\n")
    for party in insights["top_5_parties"]:
        f.write(f"  - {party[0]}: {party[1]} seats\n")
    f.write("Regional Parties:\n")
    for party in insights["regional_parties"]:
        f.write(f"  - {party}\n")

