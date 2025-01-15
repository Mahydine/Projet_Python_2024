# contient la fonction de fetch des données rss
import step4
import rss_fetch
import time

# URL des RSS feed
avis_url = "https://www.cert.ssi.gouv.fr/avis/feed"
alerte_url = "https://www.cert.ssi.gouv.fr/alerte/feed/"

# Exemple d'appel initial : consolidation de données
final_df = step4.consolidate_data(avis_url)

# On stocke la date « build » et la liste des liens à l’instant T
old_date = rss_fetch.fetch_get_build_date(avis_url)
old_links = rss_fetch.fetch_bulletin_links(avis_url)

print("Liens initiaux :", old_links)
compteur = 0

while True:
    try:
        compteur += 1
        print(f"Itération n°{compteur}")

        # Récupère la date de mise à jour actuelle du flux
        lastBuildDate = rss_fetch.fetch_get_build_date(avis_url)

        # Compare la nouvelle date avec l'ancienne
        if lastBuildDate != old_date:
            print(f"Nouveau bulletin détecté ! (ancienne date : {old_date}, nouvelle date : {lastBuildDate})")

            # Récupère la nouvelle liste de liens
            new_links = rss_fetch.fetch_bulletin_links(avis_url)

            # Compare l’ancienne liste de liens (old_links) avec la nouvelle (new_links)
            # pour trouver uniquement ceux qui viennent d’apparaître
            added_links = set(new_links) - set(old_links)
            
            if added_links:
                print("Nouveaux liens détectés :")
                for link in added_links:
                    print(link)
            else:
                # Il se peut que la date ait changé, mais que les liens soient restés identiques
                print("Aucun nouveau lien détecté, malgré une date de build modifiée.")

            # Met à jour la date et la liste de liens
            old_date = lastBuildDate
            old_links = new_links

        # Attendre 3 secondes avant la prochaine vérification (à adapter selon vos besoins)
        time.sleep(3)

    except KeyboardInterrupt:
        print("Arrêt demandé par l’utilisateur.")
        break
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        # Ici, on continue la boucle malgré l'erreur
        pass
