#contient la fonction de fetch des données rss
import rss_fetch, enrichissement_fetch, gui
import time

# URL des RSS feed
avis_url = "https://www.cert.ssi.gouv.fr/avis/feed"
alerte_url = "https://www.cert.ssi.gouv.fr/alerte/feed/"

#extraction de tout les avis & alertes
df_bulletins_avis = rss_fetch.fetch_bulletins_to_df(avis_url)
df_bulletins_alertes = rss_fetch.fetch_bulletins_to_df(alerte_url)

# Liste pour stocker les tableaux détaillés de chaque avis & alerte
df_bulletins_avis_detailed = []

# limite de fetch pour la boucle for
max_fetch = 4

# Fonction pour récupérer les détails de chaque bulletin (avec un délai)
for link in df_bulletins_avis.link[:max_fetch]:
    print(f"Fetching data for link: {link}")
    
    # Appel de la fonction pour récupérer les données de chaque lien
    result = rss_fetch.fetch_cert_json_to_dict(link)
    df_bulletins_avis_detailed.append(result)
    
    # Délai de 1 secondes entre chaque requête pour ne pas surcharger le site
    time.sleep(1)

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

scores_cvss = enrichissement_fetch.get_epss_score(cve_ids)
cvss_cwe = enrichissement_fetch.get_cvss_cwe("CVE-2023-4966")


# Utiliser la fonction `display_bulletins` du fichier gui.py pour afficher l'interface graphique
#gui.display_bulletins(df_bulletins_avis_detailed)
