import pandas as pd
import numpy as np
import re

data = pd.read_csv('personnes.csv')
print(data)

print("Nombre d'observations avant le nettoyage: ", len(data))

data = data.drop_duplicates()

data = data.dropna(subset=["prenom", "taille"])

data["pays"] = data["pays"].str.strip()

VALID_COUNTRIES = ['France', 'Côte d\'ivoire', 'Madagascar', 'Bénin', 'Allemagne', 'USA']
mask = ~data['pays'].isin(VALID_COUNTRIES)
data.loc[mask, 'pays'] = np.NaN

data['taille'] = data['taille'].str[:-1]
data['taille'] = pd.to_numeric(data['taille'], errors='coerce')
data.loc[data['taille'].isnull(), 'taille'] = data['taille'].mean()

data["date_naissance"] = pd.to_datetime(data["date_naissance"], format='%d/%m/%Y', errors="coerce")

data["pays"] = data["pays"].fillna("Inconnu")

data['email'] = data['email'].str.split(',', n=1, expand=True)[0]
data["email"] = data["email"].apply(lambda x: np.nan if not re.match(r"[^@]+@[^@]+.[^@]+", str(x)) else x)

print("Nombre de valeurs manquantes par variable:")
print(data.isnull().sum())

print("Nombre d'observations après le nettoyage: ", len(data))
print(data)
