# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:51:01 2025

@author: MahydineLAZZOULI
"""

import pandas as pd
import logging
import rss_fetch, enrichissement_fetch, services


def consolidate_data(rss_url):
    """
    Consolidate data into a single DataFrame with all required information.

    Args:
        rss_url (str): URL of the RSS feed to fetch bulletins.

    Returns:
        pd.DataFrame: Consolidated DataFrame with all required columns.
    """
    # Fetch RSS data
    rss_data = rss_fetch.fetch_bulletins_to_df(rss_url)

    consolidated_data = []

    for index, row in rss_data.iterrows():
        try:
            # Extract bulletin details
            title = row['title']
            bulletin_type = "Alerte" if "alerte" in rss_url.lower() else "Avis"
            publication_date = services.date_formatter(row['date'])
            bulletin_link = row['link']
            
            #formattage des données nécéssaire, mais étape validée
            
            # Fetch additional data from bulletin link
            cert_data = rss_fetch.fetch_cert_json_to_dict(bulletin_link)

            # Get EPSS score
            epss_df = enrichissement_fetch.get_epss_score(cert_data.get('cves'))

            for cve_id in cert_data.get('cves'):
                epss_score = epss_df.loc[epss_df['Identifiant CVE'] == cve_id, 'Score EPSS'].iloc[0] if cve_id in epss_df['Identifiant CVE'].values else "N/A"
                
                # Get CVSS, CWE, and affected product details
                cve_details_df = enrichissement_fetch.get_cvss_cwe(cve_id)
                if cve_details_df is not None and not cve_details_df.empty:
                    cve_details = cve_details_df.iloc[0]

                    consolidated_data.append({
                        "Titre du bulletin (ANSSI)": title,
                        "Type de bulletin": bulletin_type,
                        "Date de publication": publication_date,
                        "Identifiant CVE": cve_id,
                        "Score CVSS": cve_details["Score CVSS"],
                        "Base Severity": cve_details["Score Severity"],
                        "Type CWE": cve_details["CWE"],
                        "Score EPSS": epss_score,
                        "Lien du bulletin (ANSSI)": bulletin_link,
                        "Description": cve_details["Description"],
                        "Éditeur/Vendor": cve_details["Éditeur"],
                        "Produit": cve_details["Produit"],
                        "Versions affectées": cve_details["Versions"]
                    })

        except Exception as e:
            logging.error(f"Erreur lors du traitement de l'entrée {index}: {e}")

    # Create final DataFrame
    return pd.DataFrame(consolidated_data)

# Exemple d'utilisation
rss_url = "https://www.cert.ssi.gouv.fr/avis/feed"  # Remplacez par l'URL de l'RSS ANSSI
final_df = consolidate_data(rss_url)

# Sauvegarder dans un fichier CSV ou afficher
#final_df.to_csv("consolidated_cve_data.csv", index=False)

