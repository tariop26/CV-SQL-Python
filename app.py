import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from auth import authenticate

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

    st.header('Visualisations')
    st.subheader('Expériences par Entreprise')
    query_experience = """
        SELECT 
            company, 
            COUNT(*) as num_experiences
        FROM experience
        GROUP BY company;
    """
    experience_data = fetch_data(query_experience)
    st.write(experience_data)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='num_experiences', y='company', data=experience_data)
    plt.title('Nombre d\'Expériences par Entreprise')
    plt.xlabel('Nombre d\'Expériences')
    plt.ylabel('Entreprise')
    st.pyplot(plt)

    st.subheader('Compétences triées par Niveau de Maîtrise')
    query_skills = """
        SELECT 
            skill_name, 
            proficiency
        FROM skills
        ORDER BY proficiency DESC;
    """
    skills_data = fetch_data(query_skills)
    st.write(skills_data)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='proficiency', y='skill_name', data=skills_data)
    plt.title('Compétences triées par Niveau de Maîtrise')
    plt.xlabel('Niveau de Maîtrise')
    plt.ylabel('Compétence')
    st.pyplot(plt)

    st.subheader('Nombre de Projets par Compétence')
    query_projects = """
        WITH project_counts AS (
            SELECT 
                skill_name, 
                COUNT(*) as num_projects
            FROM projects
            JOIN skills ON projects.technologies_used LIKE '%' || skills.skill_name || '%'
            GROUP BY skill_name
        )
        SELECT 
            skill_name, 
            num_projects
        FROM project_counts
        ORDER BY num_projects DESC;
    """
    projects_data = fetch_data(query_projects)
    st.write(projects_data)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='num_projects', y='skill_name', data=projects_data)
    plt.title('Nombre de Projets par Compétence')
    plt.xlabel('Nombre de Projets')
    plt.ylabel('Compétence')
    st.pyplot(plt)

    # Afficher les expériences, les formations et les compétences pour les utilisateurs
    if role == "user":
        st.header('Expériences')
        experience_data = fetch_data("SELECT * FROM experience")
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT * FROM education")
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")
        st.write(skills_data)

        st.header('Ajouter une Compétence à une Expérience ou une Formation')
        item_id = st.number_input('ID de l\'expérience ou de la formation', min_value=1, step=1)
        skill_name = st.text_input('Nom de la compétence à ajouter')
        item_type = st.selectbox('Type d\'élément', ('experience', 'education'))
        if st.button('Ajouter Compétence'):
            add_skill_to_item(item_id, skill_name, item_type)
else:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
