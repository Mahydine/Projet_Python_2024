# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:43:48 2025

@author: MahydineLAZZOULI
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import step4

# Nom du fichier de sauvegarde
data_file = "final_df.csv"

if os.path.exists(data_file):
    print("Chargement du fichier existant...")
    df = pd.read_csv(data_file)  # Charger le DataFrame
else:
    print("Fichier non trouvé, calcul des données...")
    rss_url = "https://www.cert.ssi.gouv.fr/avis/feed"  # Remplacez par l'URL de l'RSS ANSSI
    step4.consolidate_data(rss_url)
    

temp_df= df['Score CVSS' && df['Score EPSS']]
print(temp_df)

plt.figure(figsize=(8, 6))  # Taille de la figure
sns.heatmap(df, annot=True, cmap="coolwarm", fmt="g")  # Heatmap
plt.title("Heatmap Example")
plt.show()