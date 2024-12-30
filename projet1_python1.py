import pandas as pd
import numpy as np
import requests
import time  # Import de time pour gérer le délai si nécessaire

cve_id = "CVE-2024-21893"
url = f"https://cveawg.mitre.org/api/cve/{cve_id}"

# Optional delay if needed
time.sleep(5)

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
    try:
        cvss_score = (
            data.get("containers", {})
            .get("cna", {})
            .get("metrics", [{}])[0]
            .get("cvssV3_0", {})
            .get("baseScore", "Score CVSS non disponible")
        )
    except KeyError:
        cvss_score = "Score CVSS non disponible"

    # Extraire le CWE
    cwe = "Non disponible"
    cwe_desc = "Non disponible"
    problemtype = data.get("containers", {}).get("cna", {}).get("problemTypes", [])
    if problemtype and "descriptions" in problemtype[0]:
        cwe = problemtype[0]["descriptions"][0].get("cweId", "Non disponible")
        cwe_desc = problemtype[0]["descriptions"][0].get("description", "Non disponible")

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
        print(f"Éditeur : {vendor}, Produit : {product_name}, Versions : {', '.join(versions)}")

    # Afficher les résultats
    print(f"CVE : {cve_id}")
    print(f"Description : {description}")
    print(f"Score CVSS : {cvss_score}")
    print(f"CWE : {cwe}")
    print(f"Description CWE : {cwe_desc}")

else:
    print(f"Échec de la récupération des données pour {cve_id}. Code statut : {response.status_code}")
