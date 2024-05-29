# auth.py
import streamlit as st

# Liste des utilisateurs et leurs rôles
users = {
    "admin": {"password": "admin_pass", "role": "admin"},
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
