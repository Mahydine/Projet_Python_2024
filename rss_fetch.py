import feedparser
import pandas as pd
import requests
import re

def fetch_bulletins_to_df(url):
    # Parse the RSS feed
    rss_feed = feedparser.parse(url)

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
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
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
