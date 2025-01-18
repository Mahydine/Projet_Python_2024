# Application de gestion des alertes RSS en cybersécurité

Ce projet permet de récupérer et de traiter des flux RSS du CERT-FR pour des alertes et avis en cybersécurité. Les données consolidées sont enrichies avec des informations supplémentaires, telles que les détails CVE, puis des notifications sont envoyées par email selon les préférences des utilisateurs.

---

## **Prérequis**

1. **Version de Python** : 3.8 ou supérieur
2. **Bibliothèques requises** :
   - `feedparser`
   - `pandas`
   - `requests`
   - `smtplib`
   - `email`
   - `re`

   Installez les dépendances avec la commande :
   ```bash
   pip install -r requirements.txt
   ```
---

## **Lancer l'application**

1. **Configuration initiale** :
   - Vérifiez que le fichier `final_data.csv` est présent à la racine (sinon, il sera créé automatiquement).

2. **Exécutez la commande** :
   python main.py

/!\ Le code à un délai de 30 minutes entre chaques tentatives de détections de nouveaux bulletins, 
se référer à la démo vidéo ou bien changer la variable "sleep_time" tout en haut du main.py /!\

3. L’application surveillera en continu les flux RSS et enverra des notifications par email selon les préférences utilisateurs.

---

## **Structure du code**

- **`main.py`** :
  Point d’entrée de l’application. Gère la surveillance des flux RSS, la récupération des données et l’envoi des notifications.

- **`rss_fetch.py`** :
  Contient les fonctions pour récupérer et analyser les flux RSS.

- **`services.py`** :
  Fonctions utilitaires pour formater les dates et rechercher des valeurs dans des données imbriquées.

- **`step4.py`** :
  Consolidation et enrichissement des données avec des détails CVE.

- **`email_services.py`** :
  Préparation et envoi des emails d’alerte.

- **`enrichissement_fetch.py`** :
  Récupère des détails supplémentaires sur les vulnérabilités, comme les scores CVSS et EPSS.

---

## **Points de vigilance**

1. **Identifiants email** :
   les informations pour l'émail qui est utiliser pour envoyer, sont à modifier si nécéssaire.

2. **Requêtes réseau** :
   - Les URLs des flux RSS et des API sont interrogées régulièrement, nos délais ont été choisi arbitrairement.

4. **Gestion des données** :
   - Le script ajoute de nouvelles données au fichier CSV, il faut donc prendre en compte sa taille au fil du temps.
