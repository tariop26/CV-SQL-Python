import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from auth import authenticate
import random

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour ajouter une compétence
def add_skill(skill_name, proficiency):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO skills (skill_name, proficiency)
        VALUES (?, ?)
    """, (skill_name, proficiency))
    conn.commit()
    conn.close()
    st.success(f"Skill '{skill_name}' added successfully.")

# Fonction pour ajouter une expérience
def add_experience(company, job_title, start_date, end_date, description):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO experience (company, job_title, start_date, end_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (company, job_title, start_date, end_date, description))
    conn.commit()
    conn.close()
    st.success(f"Experience '{job_title} at {company}' added successfully.")

# Fonction pour ajouter une formation
def add_education(institution, degree, start_date, end_date, description):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO education (institution, degree, start_date, end_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (institution, degree, start_date, end_date, description))
    conn.commit()
    conn.close()
    st.success(f"Education '{degree} at {institution}' added successfully.")

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

# Fonction pour récupérer les compétences associées
def fetch_skills_for_item(item_id, item_type):
    conn = sqlite3.connect('cv_database.db')
    query = f"""
        SELECT skill_name
        FROM {item_type}_skills
        WHERE {item_type}_id = ?
    """
    data = pd.read_sql_query(query, conn, params=(item_id,))
    conn.close()
    return data['skill_name'].tolist()

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

        st.header('Expériences')
        experience_data = fetch_data("SELECT id, job_title, company, start_date, end_date FROM experience")
        experience_data['skills'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
        experience_data = experience_data.drop(columns=['id'])  # Supprimer la colonne id
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT id, degree AS job_title, institution AS company, start_date, end_date FROM education")
        education_data['skills'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
        education_data = education_data.drop(columns=['id'])  # Supprimer la colonne id
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")
        st.write(skills_data)

        st.subheader('Ajouter une Formation ou une Expérience')
        add_type = st.selectbox('Type à ajouter', ['Formation', 'Expérience'])

        if add_type == 'Expérience':
            company = st.text_input('Entreprise')
            job_title = st.text_input('Titre du poste')
            start_date = st.date_input('Date de début')
            end_date = st.date_input('Date de fin')
            description = st.text_area('Description')
            if st.button('Ajouter Expérience'):
                add_experience(company, job_title, str(start_date), str(end_date), description)
        elif add_type == 'Formation':
            institution = st.text_input('Institution')
            degree = st.text_input('Diplôme')
            start_date = st.date_input('Date de début')
            end_date = st.date_input('Date de fin')
            description = st.text_area('Description')
            if st.button('Ajouter Formation'):
                add_education(institution, degree, str(start_date), str(end_date), description)

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

        st.subheader('Ajouter une Compétence')
        new_skill_name = st.text_input('Nom de la nouvelle compétence')
        new_proficiency = st.number_input('Niveau de maîtrise', min_value=1, max_value=5, step=1)
        if st.button('Ajouter Compétence'):
            add_skill(new_skill_name, new_proficiency)

    # Frise chronologique pour les utilisateurs
    if role == "user":
        st.markdown("[Télécharger mon CV au format PDF](https://tariop26.github.io/)")
        st.header('Frise Chronologique des Expériences et Formations')

        # Récupérer les expériences
        experiences = fetch_data("SELECT job_title, company, start_date, end_date FROM experience")
        experiences['type'] = 'Experience'
        experiences['y'] = 'Expériences'
        experiences['color'] = 'green'

        # Récupérer les formations
        educations = fetch_data("SELECT degree AS job_title, institution AS company, start_date, end_date FROM education")
        educations['type'] = 'Education'
        educations['y'] = 'Formations'
        educations['color'] = 'blue'

        # Combiner les deux DataFrames
        timeline_data = pd.concat([experiences, educations], ignore_index=True)
        timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
        timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
        timeline_data['label'] = timeline_data.apply(lambda row: f"{row['job_title']} at {row['company']}", axis=1)
        timeline_data['opacity'] = [random.uniform(0.2, 0.6) for _ in range(len(timeline_data))]

        # Créer la frise chronologique avec Plotly
        fig = go.Figure()

        for _, row in timeline_data.iterrows():
            fig.add_trace(go.Bar(
                x=[row['start_date'], row['end_date']],
                y=[row['y'], row['y']],
                orientation='h',
                width=0.4,
                marker=dict(
                    color=row['color'],
                    opacity=row['opacity']
                ),
                text=row['label'],
                hoverinfo='text',
                name=row['label']
            ))

        fig.update_layout(
            barmode='stack',
            xaxis=dict(type='date', range=['2000-01-01', pd.to_datetime('today')]),
            yaxis=dict(title="", showticklabels=True, ticktext=['Formations', 'Expériences'], tickvals=['Formations', 'Expériences']),
            showlegend=False,
            title="Frise Chronologique des Expériences et Formations",
            height=600
        )

        st.plotly_chart(fig)

        st.header('Expériences')
        experience_data = fetch_data("SELECT id, job_title, company, start_date, end_date FROM experience")
        experience_data['skills'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
        experience_data = experience_data.drop(columns=['id'])  # Supprimer la colonne id
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT id, degree AS job_title, institution AS company, start_date, end_date FROM education")
        education_data['skills'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
        education_data = education_data.drop(columns=['id'])  # Supprimer la colonne id
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")
        st.write(skills_data)

else:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
