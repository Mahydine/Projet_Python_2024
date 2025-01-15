# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:51:01 2025

@author: MahydineLAZZOULI
"""

import pandas as pd
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
    max_row = 10

    for index, row in rss_data.head(max_row).iterrows():
        print(f'[START] traitement de la ligne : {index+1}/{len(rss_data.head(max_row))}')
        try:
            # Extract bulletin details
            title = row['title']
            bulletin_type = "Alerte" if "alerte" in rss_url.lower() else "Avis"
            publication_date = services.date_formatter(row['date'])
            bulletin_link = row['link']
            print(f'{bulletin_link}')
            #formattage des données nécéssaire, mais étape validée
            
            # Fetch additional data from bulletin link
            cert_data = rss_fetch.fetch_cert_json_to_dict(bulletin_link)
            
            #TEMPORAIRE - ce bulletin ne contient que 3 ou 4 CVE enrichissables sur plus de 600
            #TEMPORAIRE - pour l'instant je le blacklist manuellement mais faut trouver autre chose
            if(title == "Multiples vulnérabilités dans le noyau Linux d'Ubuntu (13 décembre 2024)"):
                print('Blacklisted, passage au bulletin suivant.\n')
                continue
            
            #passage au prochain bulletin si aucun CVE
            if(cert_data.get('cves')== []):
                print('Aucun CVE trouvé, passage au bulletin suivant.\n')
                continue

            # Get EPSS score
            epss_df = enrichissement_fetch.get_epss_score(cert_data.get('cves'))

            compteur = 1
            for cve_id in cert_data.get('cves'):
                
                # Si on dépasse 10 CVE, on passe directement à la CVE suivante
                if compteur > 10:
                    print("Plus de 10 CVEs, on skip cette itération.")
                    continue
                
                print(f'enrichissement du CVE : {cve_id} - {compteur}/{len(cert_data.get("cves"))}')
                compteur += 1
                
                epss_score = "N/A"
                
                if(epss_df is not None and epss_df is not epss_df.empty):
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
                    
            print(f'[END] fin du traitement de la ligne : {index+1} \n')
                    
        except Exception as e:
            return pd.DataFrame(row)
            print(f"Erreur lors du traitement de l'entrée {index+1}: {e}")

    # Create final DataFrame
    pd.DataFrame(consolidated_data).to_csv("final_df.csv", index=False)
    return pd.DataFrame(consolidated_data)
