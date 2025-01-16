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
            
            #.. appeler le truc ici
            cves_data = consolidate_bulletins_cves(bulletin_link)
            
            if(cves_data == None):
                continue
        
            for cve_data in cves_data:
                
                cve_data["Titre du bulletin (ANSSI)"] = title
                cve_data["Type de bulletin"] = bulletin_type
                cve_data["Date de publication"] = publication_date
                
                consolidated_data.append(cve_data)
                    
            print(f'[END] fin du traitement de la ligne : {index+1} \n')
                    
        except Exception as e:
            return pd.DataFrame(row)
            print(f"Erreur lors du traitement de l'entrée {index+1}: {e}")

    # Create final DataFrame
    pd.DataFrame(consolidated_data).to_csv("final_df.csv", index=False)
    return pd.DataFrame(consolidated_data)



def consolidate_bulletins_cves(bulletin_link):
    # Fetch additional data from bulletin link
    cert_data = rss_fetch.fetch_cert_json_to_dict(bulletin_link)

    consolidate_cves_data = []

    #passage au prochain bulletin si aucun CVE
    if(cert_data.get('cves')== []):
        print('Aucun CVE trouvé, passage au bulletin suivant.\n')
        return None

    # Si on dépasse 30 CVE, on passe directement à la CVE suivante
    if (len(cert_data.get('cves')) >= 30):
        print("Plus de 30 CVEs, on skip cette itération.\n")
        return None
        

    # Get EPSS score
    epss_df = enrichissement_fetch.get_epss_score(cert_data.get('cves'))

    compteur = 0
    
    for cve_id in cert_data.get('cves'):
        
        compteur += 1
        
        print(f'enrichissement du CVE : {cve_id} - {compteur}/{len(cert_data.get("cves"))}')

        
        epss_score = "N/A"
        
        if(epss_df is not None and epss_df is not epss_df.empty):
            epss_score = epss_df.loc[epss_df['Identifiant CVE'] == cve_id, 'Score EPSS'].iloc[0] if cve_id in epss_df['Identifiant CVE'].values else "N/A"
        
        # Get CVSS, CWE, and affected product details
        cve_details_df = enrichissement_fetch.get_cvss_cwe(cve_id)
        if cve_details_df is not None and not cve_details_df.empty:
            cve_details = cve_details_df.iloc[0]

        consolidate_cves_data.append({
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

    return consolidate_cves_data

# Exemple d'appel initial : consolidation de données
final_df = consolidate_bulletins_cves("https://www.cert.ssi.gouv.fr/avis/CERTFR-2025-AVI-0041/json")

import time
def testwait():
    time.sleep(3)