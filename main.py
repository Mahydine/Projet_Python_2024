# contient la fonction de fetch des données rss
import step4
import rss_fetch
import time
import pandas as pd
import email_essai1

# URL des RSS feed
avis_url = "https://www.cert.ssi.gouv.fr/avis/feed"
alerte_url = "https://www.cert.ssi.gouv.fr/alerte/feed/"

# Exemple d'appel initial : consolidation de données
final_df = step4.consolidate_data(avis_url)

users_preferences = [
    {
        "email": "mahydinegame@gmail.com",
        "severity": ["HIGH", "CRITICAL"],
        "products": ["github", "Visual Studio"]
    },
    {
        "email": "mahydinegame@gmail.com",
        "severity": ["MEDIUM", "HIGH", "CRITICAL"],
        "products": ["linux", "ubuntu"]
    },
    {
        "email": "mahydinegame@gmail.com",
        "severity": ["CRITICAL"],
        "products": ["adobe", "oracle"]
    }
]


# On stocke la date « build » et la liste des liens à l’instant T
old_date = rss_fetch.fetch_get_build_date(avis_url)
old_bulletins_data = rss_fetch.fetch_bulletin_links(avis_url)

compteur = 0

while True:
    try:
        compteur += 1
        print(f">> Itération n°{compteur}")
        
        if(compteur == 3):
            old_date = 0
            old_bulletins_data = old_bulletins_data[:-4]
            
        # Récupère la date de mise à jour actuelle du flux
        lastBuildDate = rss_fetch.fetch_get_build_date(avis_url)

        # Compare la nouvelle date avec l'ancienne
        if lastBuildDate != old_date:
            print(f"---------------------\n[NEW] bulletin détecté ! (ancienne date : {old_date}, nouvelle date : {lastBuildDate})\n---------------------")

            # Récupère la nouvelle liste de liens
            new_bulletins_data = rss_fetch.fetch_bulletin_links(avis_url)
            new_links = [bulletin["link"] for bulletin in new_bulletins_data]
            
            # Compare l’ancienne liste de liens (old_links) avec la nouvelle (new_links)
            # pour trouver uniquement ceux qui viennent d’apparaître
            # Extraire uniquement les liens
            old_links = [bulletin["link"] for bulletin in old_bulletins_data]
            
            added_links = set(new_links) - set(old_links)
            
            # Met à jour la date et la liste de liens
            old_date = lastBuildDate
            old_links = new_links
            
            if added_links:
                print("Nouveaux liens détectés :")
                new_data = []
                
                for new_bulletin in new_bulletins_data:
                    if new_bulletin['link'] in added_links:  # Vérifier si le lien est nouveau
                        new_cve_data = step4.consolidate_bulletins_cves(new_bulletin['link'] + 'json')
                        if new_cve_data:
                            for data in new_cve_data:  # Parcourir chaque dictionnaire de la liste
                                data["Titre du bulletin (ANSSI)"] = new_bulletin['title']
                                data["Type de bulletin"] = new_bulletin['type']
                                data["Date de publication"] = new_bulletin['date']
                                new_data.append(data)  # Ajouter à une liste temporaire
           
                if new_data:
                    # Concaténer les nouvelles données dans testDF
                    final_df = pd.concat([final_df, pd.DataFrame(new_data)], ignore_index=True)
                    email_essai1.process_and_send_alerts(users_preferences, new_data)
                    
                else:
                    # Il se peut que la date ait changé, mais que les liens soient restés identiques
                    print("Aucun nouveau lien détecté, malgré une date de build modifiée.")

        # Attendre 3 secondes avant la prochaine vérification (à adapter selon vos besoins)
        time.sleep(2)

    except KeyboardInterrupt:
        print("\n--------- Arrêt demandé par l’utilisateur.\n")
        break
    except Exception as e:
        print(f"\n--------- Une erreur s'est produite : {e}\n")
        # Ici, on continue la boucle malgré l'erreur
        pass
