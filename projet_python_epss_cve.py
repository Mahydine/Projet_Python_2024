#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:42:47 2024

@author: ubuntu
"""

import requests
import time                 # librairie 
import pandas as pd
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_epss_score(cve_id):
    """
    Récupère le score EPSS pour un identifiant CVE donné.
    """
    try:
        url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
        response = requests.get(url)
        response.raise_for_status()
        time.sleep(1)  # Réduction de la pause pour optimisation

        data = response.json()
        epss_data = data.get("data", [])
        return epss_data[0]["epss"] if epss_data else "Aucun score EPSS trouvé"
    except Exception as e:
        logging.error(f"Erreur lors de la récupération du score EPSS pour {cve_id}: {e}")
        return "Erreur"

# Dictionnaire des CVE de l'annsi à traiter
cve_ids = [
    "CVE-2023-3519", "CVE-2023-3466", "CVE-2023-3467", "CVE-2023-46805", 
    "CVE-2023-4966", "CVE-2023-4967", "CVE-2023-27997", "CVE-2024-3400", 
    "CVE-2024-21887", "CVE-2024-22024", "CVE-2024-21893", "CVE-2024-21888", 
    "CVE-2024-21762", "CVE-2021-31207", "CVE-2021-34473", "CVE-2021-34523", 
    "CVE-2021-36958", "CVE-2021-34527", "CVE-2021-34481", "CVE-2021-1675", 
    "CVE-2021-27078", "CVE-2021-27065", "CVE-2021-26858", "CVE-2021-26857", 
    "CVE-2021-26855", "CVE-2021-26854", "CVE-2021-26412", "CVE-2022-35947", 
    "CVE-2022-41082", "CVE-2022-41040"
]

# Liste pour stocker les résultats
results = []

# Traitement de chaque CVE
for cv_id in cve_ids:
    try:
        epss_score = get_epss_score(cv_id)
        results.append({
            "Identifiant CVE": cv_id,
            "Score EPSS": epss_score
        })
    except Exception as e:
        logging.error(f"Erreur lors du traitement du CVE {cv_id}: {e}")

# Création de la DataFrame avec les résultats
df = pd.DataFrame(results)

# Affichage de la DataFrame
print(df.head())
