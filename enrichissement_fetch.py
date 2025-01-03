# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:41:13 2025

@author: MahydineLAZZOULI
"""
import requests
import time
import logging
import pandas as pd
import services

def get_epss_score(cve_ids):
    """
    Récupère le score EPSS pour un ou plusieurs identifiants CVE.
    
    Paramètres:
        cve_ids (str | list): Un identifiant CVE unique ou une liste d'identifiants CVE.
    
    Retourne:
        dict | None: Un dictionnaire avec les identifiants CVE et leurs scores EPSS ou None.
        
    Commentaire : 
        Nous avons découvert que nous pouvions fetch plusieurs cve en UNE requette en
        les listant avec le séparateur "," entre chacun, ce qui optimise énormément la fonction.
    """
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    batch_size = 100  # Taille maximale autorisée par requête
    
    try:
        for i in range(0, len(cve_ids), batch_size):
            cve_ids_batched = cve_ids[i:i + batch_size]
        
            # Le convertir en liste si un seul ID est fourni
            if isinstance(cve_ids_batched, str):
                cve_ids_batched = [cve_ids_batched]
            elif not isinstance(cve_ids_batched, list):
                raise ValueError("Le paramètre 'cve_ids_batched' doit être une chaîne de caractères ou une liste.")
    
            # Créer l'URL avec les CVE ID séparés par des virgules
            cve_param = ",".join(cve_ids_batched)
    
            url = f"https://api.first.org/data/v1/epss?cve={cve_param}"
            response = requests.get(url)
            response.raise_for_status()
            
            time.sleep(1)  # Réduction de la pause pour optimisation
    
            data = response.json()
            epss_data = data.get("data", [])
    
            results = []
            for cve_score in epss_data:
                results.append({
                    "Identifiant CVE": cve_score['cve'],
                    "Score EPSS": cve_score['epss']
                })
                
        return pd.DataFrame(results)
    
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du/des score EPSS pour {cve_ids}: {e}")
        return "Erreur"
    
def get_cvss_cwe(cve_id): 
    url = f"https://cveawg.mitre.org/api/cve/{cve_id}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Extraire la description
        description = (
            data.get("containers", {})
            .get("cna", {})
            .get("descriptions", [{}])[0]
            .get("value", "Description non disponible")
        )

        # Extraire le score CVSS
        cvss_score = services.find_value_recursively(data, 'baseScore')
        cvss_severity = services.find_value_recursively(data, 'baseSeverity')
        
        # Initialiser les variables CWE avec des valeurs par défaut
        cwe_type = "N/A"
        cwe_desc = "N/A"
       
        # Extraire le CWE
        problemtype = services.find_value_recursively(data, 'problemTypes')[0]
        if problemtype and "descriptions" in problemtype:
            cwe_type = problemtype["descriptions"][0].get("cweId", "N/A")
            cwe_desc = problemtype['descriptions'][0].get("description", "N/A")

        # Extraire les produits affectés
        affected = data.get("containers", {}).get("cna", {}).get("affected", [])
        for product in affected:
            vendor = product.get("vendor", "Non disponible")
            product_name = product.get("product", "Non disponible")
            versions = [
                v.get("version", "Non disponible")
                for v in product.get("versions", [])
                if v.get("status") == "affected"
            ]

        results = []
        results.append({
            "Identifiant CVE": cve_id,
            "Description": description,
            "Score CVSS" : cvss_score,
            "Score Severity": cvss_severity,
            "CWE" : cwe_type,
            "Description CWE" : cwe_desc,
            "Éditeur" : vendor,
            "Produit" : product_name,
            "Versions" : ', '.join(versions)
        })
        
        return pd.DataFrame(results)

    else:
        return None
        print(f"Échec de la récupération des données pour {cve_id}. Code statut : {response.status_code}")
        
        

