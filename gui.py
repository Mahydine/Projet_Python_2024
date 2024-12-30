import tkinter as tk
from tkinter import messagebox

# Fonction pour afficher les détails d'un bulletin
def show_details(bulletin):
    """
    Affiche les détails d'un bulletin dans une fenêtre Toplevel.
    """
    # Extraire les informations du bulletin
    title = bulletin.get('title', 'No title')
    content = bulletin.get('content', 'No content')
    reference = bulletin.get('reference', 'No reference')
    affected_systems = bulletin.get('affected_systems', [])
    cves = bulletin.get('cves', [])
    
    # Créer une nouvelle fenêtre pour afficher les détails
    details_window = tk.Toplevel()
    details_window.title(f"Détails de l'alerte : {title}")
    
    # Afficher les détails du bulletin
    tk.Label(details_window, text=f"Title: {title}", font=("Arial", 14)).pack(pady=10)
    tk.Label(details_window, text=f"Content: {content}", wraplength=400).pack(pady=10)
    tk.Label(details_window, text=f"Reference: {reference}", font=("Arial", 10)).pack(pady=5)
    
    # Liste des systèmes affectés
    if affected_systems:
        tk.Label(details_window, text="Affected Systems:", font=("Arial", 12, "bold")).pack(pady=10)
        for system in affected_systems:
            # On utilise get pour éviter une erreur si "description" n'existe pas
            desc = system.get("description", "No description")
            tk.Label(details_window, text=desc).pack(pady=3)
    
    # Ajouter un bouton pour afficher les CVEs
    tk.Button(
        details_window, 
        text="Voir les CVEs", 
        command=lambda: show_cves(cves, details_window)
    ).pack(pady=20)


# Fonction pour afficher les CVEs d'un bulletin
def show_cves(cves, parent_window):
    """
    Crée une nouvelle fenêtre qui affiche la liste des CVEs.
    """
    if not cves:
        messagebox.showinfo("No CVEs", "Aucune CVE trouvée pour ce bulletin.")
        return
    
    # Créer une nouvelle fenêtre pour afficher les CVEs
    cve_window = tk.Toplevel(parent_window)
    cve_window.title("Liste des CVEs")
    
    # Afficher la liste des CVEs
    for cve in cves:
        cve_name = cve.get("name", "Unknown CVE")
        cve_url = cve.get("url", "No URL")
        cve_text = f"CVE Name: {cve_name}\nURL: {cve_url}"
        tk.Label(cve_window, text=cve_text, justify="left", font=("Arial", 10)).pack(pady=5)


# Fonction principale pour afficher les bulletins
def display_bulletins(bulletins_list):
    """
    Affiche tous les bulletins contenus dans bulletins_list
    dans une fenêtre Tkinter. Chaque bulletin est un dictionnaire
    avec au minimum les clés 'title', 'content', 'reference',
    'affected_systems', 'cves'.
    """
    # Créer la fenêtre principale
    window = tk.Tk()
    window.title("Exploration des Bulletins ANSSI")
        
    tk.Label(window, text="Liste des Bulletins", font=("Arial", 16)).pack(pady=20)
    
    # Créer un bouton pour chaque bulletin
    for bulletin in bulletins_list:
        title = bulletin.get('title', 'Bulletin sans titre')
        bulletin_button = tk.Button(
            window, 
            text=title, 
            width=50, 
            command=lambda b=bulletin: show_details(b)
        )
        bulletin_button.pack(pady=5)
    
    # Boucle principale de la fenêtre
    window.mainloop()
