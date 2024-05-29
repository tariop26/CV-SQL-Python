import os
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir le mot de passe admin depuis la variable d'environnement
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Liste des utilisateurs et leurs rôles
users = {
    "admin": {"password": ADMIN_PASSWORD, "role": "admin"}
}

def authenticate(username, password=None):
    if username == "admin":
        if password == ADMIN_PASSWORD:
            return "admin"
    else:
        return "user"
    return None
