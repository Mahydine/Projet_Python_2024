"""
Created on Fri Sep 27 13:57:47 2024

@author: ubuntu """

import smtplib
from email.mime.text import MIMEText
import re
 
def prepare_email_body(cves):
    """Prépare le corps de l'email à partir des CVEs filtrées."""
    email_body = "Bonjour,\n\nVoici les vulnérabilités détectées correspondant à vos préférences :\n\n"
    for cve in cves:
        email_body += (
            f"- CVE : {cve['Identifiant CVE']}\n"
            f"  Produit : {cve['Produit']}\n"
            f"  Gravité : {cve['Base Severity']}\n\n"
        )
    email_body += "Cordialement,\nVotre équipe de sécurité."
    return email_body

def send_email(to_email, subject, body):
    """Envoie un email avec le sujet et le corps fournis."""
    
    sender_email = "cvecyber@gmail.com"
    sender_password = "royf lmac zbfw mecn"
    
    # Préparer le message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        # Se connecter au serveur SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [to_email], msg.as_string())
        print(f"Email envoyé à {to_email} avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email à {to_email}: {e}")

def process_and_send_alerts(users_preferences, new_data):
    """
    Filtre les CVEs en fonction des préférences des utilisateurs
    et envoie des emails contenant les alertes correspondantes.
    """
    for user in users_preferences:
        # Filtrer les CVEs pour cet utilisateur
        user_cves = [
           cve for cve in new_data
           if cve.get("Base Severity", "").upper() in user["severity"]
           and any(re.search(rf"\b{prod}\b", cve.get("Produit", ""), re.IGNORECASE) for prod in user["products"])
       ]
        if user_cves:
            # Préparer le contenu de l'email
            email_body = prepare_email_body(user_cves)
            send_email(user["email"], "Alerte Sécurité : CVE détectées", email_body)
