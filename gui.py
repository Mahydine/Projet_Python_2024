import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webbrowser

def display_bulletins(bulletins_list):
    """
    Affiche tous les bulletins contenus dans bulletins_list
    dans une fenêtre Tkinter. Chaque bulletin est un dictionnaire
    avec au minimum les clés 'title', 'content', 'reference',
    'affected_systems', 'cves'.
    
    - Liste des bulletins à gauche (Listbox + scrollbar).
    - Zone de détails à droite avec scrollbars pour 'content', 'affected_systems' et 'cves'.
    - Pas de popup (navigation dans la même fenêtre).
    """

    # -------------------------
    # Configuration de la fenêtre principale
    # -------------------------
    root = tk.Tk()
    root.title("Exploration des Bulletins ANSSI")
    root.geometry("1000x600")  # Taille par défaut

    # Utiliser ttk pour un look plus moderne
    style = ttk.Style(root)
    style.theme_use("clam")  # Possible : "clam", "alt", "default", "vista"…

    # Configuration d'un style général
    style.configure("TFrame", background="#F4F4F4")
    style.configure("TLabel", background="#F4F4F4", foreground="#333333")
    style.configure("TButton", background="#E0E0E0", foreground="#000")

    # -------------------------
    # Cadre principal
    # -------------------------
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Label de titre (en haut)
    header_label = ttk.Label(main_frame, text="Liste des Bulletins", font=("Helvetica", 16, "bold"))
    header_label.pack(pady=10)

    # -------------------------
    # Cadre du contenu (gauche : liste / droite : détails)
    # -------------------------
    content_frame = ttk.Frame(main_frame)
    content_frame.pack(fill="both", expand=True)

    # =========================
    # Cadre de gauche (liste de bulletins)
    # =========================
    left_frame = ttk.Frame(content_frame)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    list_label = ttk.Label(left_frame, text="Sélectionnez un bulletin :")
    list_label.pack(anchor="w", padx=5, pady=5)

    # Frame pour Listbox + scrollbar
    listbox_frame = ttk.Frame(left_frame)
    listbox_frame.pack(fill="both", expand=True)

    # Scrollbar verticale pour la liste
    list_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
    list_scrollbar.pack(side="right", fill="y")

    # Listbox pour afficher les titres
    bulletin_listbox = tk.Listbox(listbox_frame, yscrollcommand=list_scrollbar.set, height=20)
    bulletin_listbox.pack(side="left", fill="both", expand=True)
    list_scrollbar.config(command=bulletin_listbox.yview)

    # =========================
    # Cadre de droite (détails)
    # =========================
    right_frame = ttk.Frame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Sous-cadre pour les détails (permet de rafraîchir facilement le contenu)
    detail_frame = ttk.Frame(right_frame)
    detail_frame.pack(fill="both", expand=True)

    # ------------------------------------------------------------
    # Fonction pour mettre à jour les détails selon le bulletin sélectionné
    # ------------------------------------------------------------
    def update_details(event=None):
        # Récupère l'index du bulletin sélectionné dans la Listbox
        selection = bulletin_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        bulletin = bulletins_list[index]

        # On vide le contenu précédent du detail_frame
        for widget in detail_frame.winfo_children():
            widget.destroy()

        # Extraire les infos du bulletin
        title = bulletin.get('title', 'No title')
        content = bulletin.get('content', 'No content')
        reference = bulletin.get('reference', 'No reference')
        affected_systems = bulletin.get('affected_systems', [])
        cves = bulletin.get('cves', [])

        # Titre du bulletin
        lbl_title = ttk.Label(detail_frame, text=title, font=("Helvetica", 14, "bold"))
        lbl_title.pack(pady=5, anchor="w")

        # Référence
        lbl_reference = ttk.Label(detail_frame, text=f"Référence : {reference}", font=("Helvetica", 9, "italic"))
        lbl_reference.pack(pady=5, anchor="w")

        # -------------------------
        # Zone de texte défilable pour la description (content)
        # -------------------------
        content_label = ttk.Label(detail_frame, text="Description :", font=("Helvetica", 10, "bold"))
        content_label.pack(pady=(10, 0), anchor="w")

        content_text = scrolledtext.ScrolledText(detail_frame, wrap="word", width=60, height=8)
        content_text.pack(pady=5, fill="both", expand=False)
        content_text.insert("end", content)
        content_text.config(state="disabled")  # Rendre la zone non-éditable

        # -------------------------
        # Systèmes affectés
        # -------------------------
        if affected_systems:
            affected_label = ttk.Label(detail_frame, text="Systèmes affectés :", font=("Helvetica", 10, "bold"))
            affected_label.pack(pady=(10, 0), anchor="w")

            aff_frame = ttk.Frame(detail_frame)
            aff_frame.pack(fill="both", expand=False, pady=5)

            aff_scroll = ttk.Scrollbar(aff_frame, orient="vertical")
            aff_scroll.pack(side="right", fill="y")

            aff_text = tk.Text(aff_frame, wrap="word", yscrollcommand=aff_scroll.set, height=5)
            aff_text.pack(side="left", fill="both", expand=True)
            aff_scroll.config(command=aff_text.yview)

            for system in affected_systems:
                desc = system.get("description", "No description")
                aff_text.insert("end", f"- {desc}\n")
            aff_text.config(state="disabled")

        # -------------------------
        # Liste des CVEs (scrollable)
        # -------------------------
        cve_label = ttk.Label(detail_frame, text="CVEs :", font=("Helvetica", 10, "bold"))
        cve_label.pack(pady=(10, 0), anchor="w")

        if cves:
            cve_frame = ttk.Frame(detail_frame)
            cve_frame.pack(fill="both", expand=False, pady=5)

            cve_scroll = ttk.Scrollbar(cve_frame, orient="vertical")
            cve_scroll.pack(side="right", fill="y")

            cve_text = tk.Text(cve_frame, wrap="word", yscrollcommand=cve_scroll.set, height=5)
            cve_text.pack(side="left", fill="both", expand=True)
            cve_scroll.config(command=cve_text.yview)

            for cve in cves:
                cve_name = cve.get("name", "Unknown CVE")
                cve_url = cve.get("url", "No URL")

                # Insérer chaque CVE sous forme de texte
                if cve_url != "No URL":
                    # On peut insérer un texte cliquable, mais c'est plus complexe à gérer
                    # Pour rester simple, on met juste l'URL en texte :
                    cve_text.insert("end", f"- {cve_name} : {cve_url}\n")
                else:
                    cve_text.insert("end", f"- {cve_name}\n")

            cve_text.config(state="disabled")

        else:
            no_cve_label = ttk.Label(detail_frame, text="Aucune CVE trouvée.")
            no_cve_label.pack(pady=5, anchor="w")

    # ------------------------------------------------------------
    # Peuplement de la Listbox avec les titres de bulletins
    # ------------------------------------------------------------
    for bulletin in bulletins_list:
        title = bulletin.get('title', 'Bulletin sans titre')
        bulletin_listbox.insert("end", title)

    # Lorsque l'utilisateur sélectionne un élément, on appelle 'update_details'
    bulletin_listbox.bind("<<ListboxSelect>>", update_details)

    # Lance la boucle principale de l'interface
    root.mainloop()
