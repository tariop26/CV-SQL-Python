import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour mettre à jour l'expérience professionnelle
def update_experience(job_title, end_date, description, id):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE experience
        SET job_title = ?, end_date = ?, description = ?
        WHERE id = ?
    """, (job_title, end_date, description, id))
    conn.commit()
    conn.close()
    st.success(f"Experience with id {id} updated successfully.")

# Fonction pour mettre à jour une compétence
def update_skill(proficiency, skill_name):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE skills
        SET proficiency = ?
        WHERE skill_name = ?
    """, (proficiency, skill_name))
    conn.commit()
    conn.close()
    st.success(f"Skill {skill_name} updated successfully.")

st.title('CV de Manuel Poirat - Visualisations et Requêtes SQL')

st.header('Expériences par Entreprise')
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

st.header('Mettre à jour une expérience professionnelle')
exp_id = st.number_input('ID de l\'expérience', min_value=1, step=1)
job_title = st.text_input('Titre du poste')
end_date = st.date_input('Date de fin')
description = st.text_area('Description')
if st.button('Mettre à jour l\'expérience'):
    update_experience(job_title, str(end_date), description, exp_id)

st.header('Compétences triées par Niveau de Maîtrise')
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

st.header('Mettre à jour une compétence')
skill_name = st.text_input('Nom de la compétence')
proficiency = st.number_input('Niveau de maîtrise', min_value=1, max_value=5, step=1)
if st.button('Mettre à jour la compétence'):
    update_skill(proficiency, skill_name)

st.header('Nombre de Projets par Compétence')
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
