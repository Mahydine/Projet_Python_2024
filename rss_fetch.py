import feedparser
import pandas as pd
import requests

#------- temporaire
import warnings
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
#----------------------

import requests
import feedparser

def fetch_get_build_date(url):
    # Télécharger le contenu RSS
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si erreur HTTP
    rss_feed = feedparser.parse(response.text)

    # Vérifier que le flux a bien un titre, et qu’il s’agit de "CERT-FR"
    if rss_feed.feed.title == "CERT-FR":
        # Récupérer la date de mise à jour (si présente)
        # Selon le flux, c'est parfois "updated", parfois "published"
        build_date = rss_feed.feed.get("updated", None)
        
        print("Titre du flux :", rss_feed.feed.title)
        print("Date de mise à jour du flux :", build_date)
        
        return build_date  # On la retourne ou on la traite selon vos besoins

    return None


def fetch_bulletin_links(url):
    # Télécharger le flux RSS
    response = requests.get(url)
    response.raise_for_status()
    
    # Parser avec feedparser
    rss_feed = feedparser.parse(response.text)
    
    # Récupérer tous les titres des bulletins (entries)
    links = [entry.link for entry in rss_feed.entries]
    
    return links

def fetch_bulletins_to_df(url):
    # Télécharger le contenu RSS avec requests
    response = requests.get(url)
    response.raise_for_status()  # Vérifier les erreurs HTTP
    
    # Parser le contenu avec feedparser
    rss_feed = feedparser.parse(response.text)

    # Create lists to store the data
    titles = []
    descriptions = []
    links = []
    dates = []

    # Iterate through the feed entries and store data in lists
    for entry in rss_feed.entries:
        titles.append(entry.title)
        descriptions.append(entry.description)
        links.append(entry.link + 'json')
        dates.append(entry.published)

    # Create and return a DataFrame
    df = pd.DataFrame({
        'title': titles,
        'description': descriptions,
        'link': links,
        'date': dates
    })
    return df


def fetch_cert_json_to_dict(url):
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code} {url}")
        return []
    
    data = response.json()
    
    full_data = {
        'title': data.get('title', ''),
        'content': data.get('content', ''),
        'cves': [cve.get('name') for cve in data.get('cves', []) if 'name' in cve],
        'reference': data.get('reference', ''),
        'affected_systems': data.get('affected_systems', [])
    }
    
    # Retourner un tableau avec les données nécessaires
    return full_data
