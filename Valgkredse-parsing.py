# %% get ready
import os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from itertools import combinations

aar = "2026"

rows_data = []

files = sorted(os.listdir(aar))

# %% read html files and extract data
for file in files:
    with open(os.path.join(aar, file), 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    faktabox = soup.find("div", class_="faktabox")
    kreds = faktabox.find("h2").text.strip()

    for row in soup.select("tr"):
        parti = row.find("td", class_="vaelgeropg_parti", recursive=False)
        numbers = row.find_all("td", class_="vaelgeropg_tal", recursive=False)

        if parti is None or len(numbers) < 2:
            continue

        parti = parti.text.strip().replace(" - Inger Støjberg","").replace(" - Socialistisk Folkeparti","").replace(" - De Rød-Grønne","").replace(", Danmarks Liberale Parti","").replace(" - Lars Boje Mathiesen","")
        if parti == "Uden for partierne":
            continue

        stemmer = int(numbers[0].text.replace(".", ""))

        rows_data.append({
            "kreds": kreds,
            "parti": parti,
            "stemmer": stemmer
        })

# %% create DataFrame and pivot
df = pd.DataFrame(rows_data)
df_pivot = df.pivot(index="kreds", columns="parti", values="stemmer")
df_total = df.groupby("kreds")["stemmer"].sum()
df_pivot.to_csv('fv26.csv', index=True, encoding='utf-8', sep=';')

# %% definer lorenz-kurven

def lorenz_weighted(party_votes, total_votes):
    party_votes = np.array(party_votes)
    total_votes = np.array(total_votes)

    share = party_votes / total_votes
    order = np.argsort(share)

    party_votes = party_votes[order]
    total_votes = total_votes[order]

    cum_total = np.cumsum(total_votes) / np.sum(total_votes)
    cum_party = np.cumsum(party_votes) / np.sum(party_votes)

    cum_total = np.insert(cum_total, 0, 0)
    cum_party = np.insert(cum_party, 0, 0)

    return cum_total, cum_party



# %% plot the Lorenz curves for each party
plt.figure(figsize=(10, 8))
colorsa = plt.cm.tab10.colors + 14*plt.cm.Pastel1.colors[:5]
colorsb = 60*plt.cm.Pastel1.colors[:5]
for i, party in enumerate(df_pivot.columns):
     values = df_pivot[party].fillna(0).values
     x, y = lorenz_weighted(values, df_total.values)
     plt.plot(x, y, label=party, color=colorsa[i])
plt.plot([0, 1], [0, 1], linestyle="--")

plt.xlabel("Andel af valgkredse vægtet med samlet antal stemmer")
plt.ylabel("Andel af partiets stemmer")
plt.title(f"Geografisk skævhed i partiernes tilslutning ved folketingsvalget {aar}")
plt.legend(fontsize=8)
plt.grid()
plt.tight_layout()
plt.savefig(f"lorenzkurver {aar}.png", dpi=300)  # ← save here
plt.show()

# %% Gini-coefficients  
gini_dict = {}
total_votes_dict = {}
def gini_weighted(party_votes, total_votes):
    x, y = lorenz_weighted(party_votes, total_votes)
    return 1 - 2 * trapezoid(y, x)


def gini_standard(values):
    values = np.sort(values)
    n = len(values)
    cumx = np.cumsum(values)
    return (n + 1 - 2 * np.sum(cumx) / cumx[-1]) / n

print(f"\nIGS {aar}:")
for party in df_pivot.columns:
    party_votes = df_pivot[party].fillna(0).values
    total_votes = df_total.loc[df_pivot.index].values

    g = gini_weighted(party_votes, total_votes)
    total = np.sum(party_votes)

    gini_dict[party] = g
    total_votes_dict[party] = total

    print(f"{party}: {g:.3f}")

ginis = np.array(list(gini_dict.values()))
totals = np.array(list(total_votes_dict.values()))
weighted_gini = np.sum(ginis * totals) / np.sum(totals)

print(f"\nVægtet gennemsnitlig IGS {aar}:", round(weighted_gini, 4))

