import streamlit as st

# Liste des utilisateurs et leurs rôles
users = {
    "admin": {"password": "admin_pass", "role": "admin"},
    "visiteur": {"role": "user"}
}

def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None
