#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 18:10:05 2025

@author: ubuntu
"""

import matplotlib.pyplot as plt
import step4
# librairie 


def plot_cwe_pie_chart(df):
    """
    Affiche un diagramme circulaire des types de vulnérabilités (CWE) les plus fréquents.

    Args:
        df (pd.DataFrame): DataFrame contenant les données consolidées avec une colonne 'Type CWE'.
    """
    if df.empty:
        print("Le DataFrame est vide. Impossible de tracer le diagramme circulaire.")
        return

    # Compter les occurrences de chaque type CWE
    try:
        cwe_counts = df["Type CWE"].value_counts()
    except KeyError:
        print("La colonne 'Type CWE' est absente du DataFrame.")
        return

    if cwe_counts.empty:
        print("Aucune donnée dans la colonne 'Type CWE'.")
        return

    # Garder les 5 catégories les plus fréquentes et regrouper les autres sous 'Autres'
    top_cwe = cwe_counts.head(5)
    others_count = cwe_counts.iloc[5:].sum()
    if others_count > 0:
        top_cwe["Autres"] = others_count

    # Créer le diagramme circulaire
    plt.figure(figsize=(0, 8))
    top_cwe.plot(
        kind="pie",
        autopct="%1.1f%%",
        colors=plt.cm.tab10.colors,
        startangle=90,
        labels=top_cwe.index,
        wedgeprops={"edgecolor": "black"},
    )
    plt.title("Répartition des types de vulnérabilités (CWE)")
    plt.ylabel("")  # Supprimer l'étiquette de l'axe Y
    plt.show()

# Exemple d'utilisation avec consolidation des données
rss_url = "https://www.cert.ssi.gouv.fr/avis/feed"  # URL RSS
final_df = consolidate_data(rss_url)

# Appeler la fonction pour tracer le diagramme circulaire
plot_cwe_pie_chart(final_df)
