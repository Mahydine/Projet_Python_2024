# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 16:01:48 2025

@author: MahydineLAZZOULI
"""

def find_value_recursively(data, uniqueKey):
    """
    Recherche récursivement une valeur dans une structure de données imbriquée.
    
    Paramètres:
        data (dict | list): Les données JSON à analyser.
        uniqueKey (str): La clé à rechercher dans la structure.
    
    Retourne:
        Any: La valeur si elle est trouvée, sinon "N/A".
    """
    if isinstance(data, dict):
        # Vérifie si la clé est directement présente
        if uniqueKey in data and data[uniqueKey] is not None:
            return data[uniqueKey]
        # Parcours récursif dans les valeurs du dictionnaire
        for value in data.values():
            result = find_value_recursively(value, uniqueKey)
            if result != "N/A":
                return result

    elif isinstance(data, list):
        # Parcours récursif dans les éléments de la liste
        for item in data:
            result = find_value_recursively(item, uniqueKey)
            if result != "N/A":
                return result

    return "N/A"

def date_formatter(date_str):
    from datetime import datetime

    # Conversion en objet datetime
    date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    
    # Formatage au format "YYYY-MM-DD"
    formatted_date = date_obj.strftime("%Y-%m-%d")
    
    return(formatted_date)
