#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 15:58:45 2024

@author: ubuntu
"""

import pandas as pd
import requests  
import time

# Données CVSS spécifiques fournies manuellement
manual_cvss_scores = {
    "CVE-2024-3400": 10.0,
    "CVE-2024-21762": 9.6,
    "CVE-2021-31207": 6.6,
    "CVE-2021-34473": 9.1,
    "CVE-2021-34523": 9.0,
    "CVE-2021-36958": 7.8,
    "CVE-2021-34527": 8.8,
    "CVE-2021-34481": 8.8,
    "CVE-2021-1675": 7.8,
    "CVE-2021-27078": 9.1,
    "CVE-2021-27065": 7.8,
    "CVE-2021-26858": 7.8,
    "CVE-2021-26857": 7.8,
    "CVE-2021-26855": 9.1,
    "CVE-2021-26854": 6.6,
    "CVE-2021-26412": 9.1,
    "CVE-2022-35947": 10.0,
    "CVE-2022-41082": 8.0,
    "CVE-2022-41040": 8.8
}

# Fonction pour récupérer les données CVE depuis l'API de MITRE ou les données manuelles
def get_cve_data(cve_id):
    if cve_id in manual_cvss_scores:
        # Utiliser les données manuelles si disponibles
        cvss_score = manual_cvss_scores[cve_id]
        description = "Données fournies manuellement"
        return cvss_score, description

    # Si pas de données manuelles, récupérer depuis l'API
    url = f"https://cveawg.mitre.org/api/cve/{cve_id}"
    try:
        time.sleep(1)  # Attente pour éviter de surcharger le serveur
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extraire le score CVSS
        cvss_score = (
            data.get("containers", {})
            .get("cna", {})
            .get("metrics", [{}])[0]
            .get("cvssV3_0", {})
            .get("baseScore", "Non disponible")
        )

        # Extraire la description
        description = data.get("containers", {}).get("cna", {}).get("descriptions", [{}])[0].get("value", "Non disponible")

        return cvss_score, description
    except Exception as e:
        print(f"Erreur lors de la récupération des données CVE {cve_id}: {e}")
        return "Erreur", "Erreur"

# Fonction pour récupérer le score EPSS depuis l'API First.org
def get_epss_score(cve_id):
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"
    try:
        time.sleep(1)  # Attente pour éviter de surcharger le serveur
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        epss_data = data.get("data", [])
        return epss_data[0]["epss"] if epss_data else "Non disponible"
    except Exception as e:
        print(f"Erreur lors de la récupération du score EPSS pour {cve_id}: {e}")
        return "Erreur"

# Liste des identifiants CVE à traiter
cve_ids = [
    "CVE-2024-3400", "CVE-2024-21762", "CVE-2021-31207", "CVE-2021-34473",
    "CVE-2021-34523", "CVE-2021-36958", "CVE-2021-34527", "CVE-2021-34481",
    "CVE-2021-1675", "CVE-2021-27078", "CVE-2021-27065", "CVE-2021-26858",
    "CVE-2021-26857", "CVE-2021-26855", "CVE-2021-26854", "CVE-2021-26412",
    "CVE-2022-35947", "CVE-2022-41082", "CVE-2022-41040"
]

# Liste pour stocker les résultats
results = []

# Traitement de chaque CVE
for cve_id in cve_ids:
    cvss_score, description = get_cve_data(cve_id)
    epss_score = get_epss_score(cve_id)

    # Ajouter les résultats dans la liste
    results.append({
        "Identifiant CVE": cve_id,
        "Score CVSS": cvss_score,
        "Score EPSS": epss_score,
       # "Description": description
    })

# Création d'une DataFrame avec les résultats
df = pd.DataFrame(results)

# Affichage de la DataFrame
print(df)
