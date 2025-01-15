import smtplib

from email.mime.text import MIMEText

 
"""
Created on Fri Sep 27 13:57:47 2024

@author: ubuntu """


msg = MIMEText("Hello, tout le monde")  # Corps du courriel

msg['Subject'] = 'Message de test'  # Objet

msg['From'] = 'gledoigt40@gmail.com'

'cvecyber@gmail.com'  # Votre adresse Gmail

msg['To'] = 'cvecyber@gmail.com'  # Adresse Gmail du destinataire

 

# Se connecter au serveur SMTP de Gmail

s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()

#bureau12&1

# Connexion à votre compte Gmail

s.login('gledoigt40@gmail.com', 'password')

 

# Envoyer le courriel

s.sendmail('gledoigt40@gmail.com', ['cvecyber@gmail.com'], msg.as_string())

 

# Quitter le serveur SMTP

s.quit()

 

print("Message envoyé !")
