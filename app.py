import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from auth import authenticate
import random

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour ajouter une compétence à une expérience ou une formation
def add_skill_to_item(item_id, skill_name, item_type):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {item_type}_skills ({item_type}_id, skill_name)
        VALUES (?, ?)
    """, (item_id, skill_name))
    conn.commit()
    conn.close()
    st.success(f"Skill '{skill_name}' added to {item_type} with id {item_id} successfully.")

# Interface de connexion
st.title('CV de Manuel Poirat - Visualisations et Requêtes SQL')
st.sidebar.title('Authentification')
username = st.sidebar.text_input('Quel est votre prénom ?')
password = None
if username == "admin":
    password = st.sidebar.text_input('Mot de passe', type='password')

role = authenticate(username, password)

if role:
    st.sidebar.success(f"Connecté en tant que {role}")

    if role == "admin":
        st.header('Admin Interface')

        st.subheader('Ajouter une Expérience')
        company = st.text_input('Entreprise')
        job_title = st.text_input('Titre du poste')
        start_date = st.date_input('Date de début')
        end_date = st.date_input('Date de fin')
        description = st.text_area('Description')
        if st.button('Ajouter Expérience'):
            add_experience(company, job_title, str(start_date), str(end_date), description)

        st.subheader('Mettre à Jour une Expérience')
        exp_id = st.number_input('ID de l\'expérience', min_value=1, step=1)
        job_title = st.text_input('Titre du poste', key='update_job_title')
        end_date = st.date_input('Date de fin', key='update_end_date')
        description = st.text_area('Description', key='update_description')
        if st.button('Mettre à Jour Expérience'):
            update_experience(job_title, str(end_date), description, exp_id)

        st.subheader('Supprimer une Expérience')
        exp_id_delete = st.number_input('ID de l\'expérience à supprimer', min_value=1, step=1, key='delete_exp_id')
        if st.button('Supprimer Expérience'):
            delete_experience(exp_id_delete)

        st.subheader('Mettre à Jour une Compétence')
        skill_name = st.text_input('Nom de la compétence', key='update_skill_name')
        proficiency = st.number_input('Niveau de maîtrise', min_value=1, max_value=5, step=1, key='update_proficiency')
        if st.button('Mettre à Jour Compétence'):
            update_skill(proficiency, skill_name)

    # Frise chronologique pour les utilisateurs
    if role == "user":
        st.header('Frise Chronologique des Expériences et Formations')

        # Récupérer les expériences
        experiences = fetch_data("SELECT job_title, company, start_date, end_date FROM experience")
        experiences['type'] = 'Experience'
        experiences['color'] = 'green'

        # Récupérer les formations
        educations = fetch_data("SELECT degree AS job_title, institution AS company, start_date, end_date FROM education")
        educations['type'] = 'Education'
        educations['color'] = 'blue'

        # Combiner les deux DataFrames
        timeline_data = pd.concat([experiences, educations], ignore_index=True)
        timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
        timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
        timeline_data['label'] = timeline_data.apply(lambda row: f"{row['job_title']} at {row['company']}", axis=1)
        timeline_data['opacity'] = [random.uniform(0.2, 0.6) for _ in range(len(timeline_data))]

        # Créer la frise chronologique avec Plotly
        fig = go.Figure()

        for i, row in timeline_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['start_date'], row['end_date']],
                y=[0, 0],
                base=[0, 0],
                width=[row['end_date'] - row['start_date'], row['end_date'] - row['start_date']],
                name=row['label'],
                marker_color=row['color'],
                opacity=row['opacity'],
                hoverinfo='text',
                text=row['label'],
                textposition='inside'
            ))

        fig.update_layout(
            barmode='stack',
            xaxis=dict(type='date', range=['2000-01-01', pd.to_datetime('today')]),
            yaxis=dict(title="", showticklabels=False),
            showlegend=False,
            title="Frise Chronologique des Expériences et Formations",
            height=600
        )

        st.plotly_chart(fig)

        st.header('Expériences')
        experience_data = fetch_data("SELECT * FROM experience")
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT * FROM education")
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")
        st.write(skills_data)
        
else:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
