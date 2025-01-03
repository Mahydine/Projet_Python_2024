# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:56:12 2025

@author: MahydineLAZZOULI
"""

batch_size = 10  # Taille maximale autorisée par requête
cve_list = [
    "CVE-2023-1234", "CVE-2023-1235", "CVE-2023-1236", "CVE-2023-1237",
    "CVE-2023-1238", "CVE-2023-1239", "CVE-2023-1240", "CVE-2023-1241",
    "CVE-2023-1242", "CVE-2023-1243", "CVE-2023-1244", "CVE-2023-1245",
    "CVE-2023-1246", "CVE-2023-1247", "CVE-2023-1248", "CVE-2023-1249",
    "CVE-2023-1250", "CVE-2023-1251", "CVE-2023-1252", "CVE-2023-1253",
    "CVE-2023-1254", "CVE-2023-1255", "CVE-2023-1256", "CVE-2023-1257",
    "CVE-2023-1258", "CVE-2023-1259"
]

# Découpage en sous-listes
batches = [cve_list[i:i + batch_size] for i in range(0, len(cve_list), batch_size)]

# Affichage des sous-listes
for idx, batch in enumerate(batches):
    print(f"Batch {idx + 1}: {batch}")