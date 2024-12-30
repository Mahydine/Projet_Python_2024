#contient la fonction de fetch des données rss
import rss_fetch, gui
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
    
    # Délai de 2 secondes entre chaque requête pour ne pas surcharger le site
    time.sleep(1)

# Utiliser la fonction `display_bulletins` du fichier gui.py pour afficher l'interface graphique
gui.display_bulletins(df_bulletins_avis_detailed)
