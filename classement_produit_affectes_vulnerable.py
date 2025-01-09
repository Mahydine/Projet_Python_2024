#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:10:57 2025

@author: garance 
"""

import matplotlib.pyplot as plt
import step4
# librairie 

def plot_top_affected_products_or_vendors(df, group_by='Produit'):
    """
    Affiche un graphique des produits ou éditeurs les plus affectés par les vulnérabilités.

    Args:
        df (pd.DataFrame): DataFrame contenant les données consolidées avec une colonne 'Produit' ou 'Éditeur'.
        group_by (str): Colonne sur laquelle effectuer le classement. 'Produit' ou 'Éditeur'.
    """
    if df.empty:
        print("Le DataFrame est vide. Impossible de tracer le classement.")
        return

    # Vérifier que la colonne demandée existe
    if group_by not in df.columns:
        print(f"La colonne '{group_by}' est absente du DataFrame.")
        return

    # Comptabiliser les occurrences des produits ou éditeurs les plus affectés
    counts = df[group_by].value_counts()

    # Garder les 10 premiers produits/éditeurs les plus affectés
    top_affected = counts.head(10)

    # Créer un graphique en barres pour visualiser les produits ou éditeurs les plus affectés
    plt.figure(figsize=(10, 6))
    top_affected.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(f"Top 10 des {group_by} les plus affectés par les vulnérabilités")
    plt.xlabel(group_by)
    plt.ylabel("Nombre de CVE")
    # Ajouter la légende avec un titre
    plt.legend(title="Systèmes vulnérables", loc="upper right")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Exemple d'utilisation avec consolidation des données
rss_url = "https://www.cert.ssi.gouv.fr/avis/feed"  # URL RSS
final_df = consolidate_data(rss_url)

# Afficher le classement des produits les plus affectés
plot_top_affected_products_or_vendors(final_df, group_by='Produit')

# Pour afficher le classement des éditeurs, utilisez :
# plot_top_affected_products_or_vendors(final_df, group_by='Éditeur')
