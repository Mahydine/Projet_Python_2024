#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 18:07:28 2025

@author: ubuntu
"""
import step4
import matplotlib.pyplot as plt
import numpy as np

def plot_cvss_histogram_with_custom_bins(df):
    """
    Affiche un histogramme des scores CVSS avec des plages de gravité personnalisées, des couleurs et une légende.

    Args:
        df (pd.DataFrame): DataFrame contenant les données consolidées.
    """
    if df.empty:
        print("Le DataFrame est vide. Impossible de tracer l'histogramme.")
        return

    # Nettoyage et conversion des scores CVSS
    try:
        cvss_scores = pd.to_numeric(df["Score CVSS"], errors="coerce").dropna()
    except KeyError:
        print("La colonne 'Score CVSS' est absente du DataFrame.")
        return

    if cvss_scores.empty:
        print("Aucun score CVSS valide trouvé dans le DataFrame.")
        return

    # Définir les intervalles (bins) et les couleurs associées
    bins = [0, 3, 6, 8, 10]  # Plages personnalisées
    colors = ["green", "yellow", "orange", "red"]
    labels = ["Faible (0-3)", "Moyenne (4-6)", "Élevée (7-8)", "Critique (9-10)"]

    # Compter les scores par tranche
    counts, _ = np.histogram(cvss_scores, bins=bins)

    # Créer l'histogramme coloré
    plt.figure(figsize=(10, 6))
    for i in range(len(bins) - 1):
        plt.bar(
            x=str(labels[i]), 
            height=counts[i], 
            color=colors[i], 
            label=labels[i]
        )

    # Ajouter des informations au graphique
    plt.xlabel("Gravité CVSS")
    plt.ylabel("Nombre de CVE")
    plt.title("Répartition des scores CVSS par gravité")
    plt.legend(title="Légende", loc="upper right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Afficher le graphique
    plt.show()

# Exemple d'utilisation avec consolidation des données
rss_url = "https://www.cert.ssi.gouv.fr/avis/feed"  # URL RSS
final_df = consolidate_data(rss_url)

# Appeler la fonction pour tracer l'histogramme avec couleurs
plot_cvss_histogram_with_custom_bins(final_df)
