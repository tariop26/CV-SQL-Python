# auth.py
import os
import streamlit as st
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Obtenir le mot de passe admin depuis la variable d'environnement
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Liste des utilisateurs et leurs rôles
users = {
    "admin": {"password": ADMIN_PASSWORD, "role": "admin"},
    "user": {"role": "user"}
}

def authenticate(username, password=None):
    user = users.get(username)
    if user:
        if user["role"] == "user":
            return user["role"]
        elif user["role"] == "admin" and user["password"] == password:
            return user["role"]
    return None
