#contient la fonction de fetch des données rss
import rss_fetch, enrichissement_fetch, gui, step4
import time

# URL des RSS feed
avis_url = "https://www.cert.ssi.gouv.fr/avis/feed"
alerte_url = "https://www.cert.ssi.gouv.fr/alerte/feed/"


final_df = step4.consolidate_data(avis_url)