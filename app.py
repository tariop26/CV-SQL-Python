import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from auth import authenticate
import random

# Configurer Streamlit pour utiliser toute la largeur de l'écran
st.set_page_config(layout="wide")

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# (Le reste de votre code...)

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
        experience_data = fetch_data("SELECT id, job_title, company, start_date, end_date, description FROM experience")
        experience_data['skills'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
        experience_data = experience_data.loc[:, experience_data.columns != experience_data.columns[0]]  # Supprimer la première colonne sans en-tête
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT id, degree AS job_title, institution AS company, start_date, end_date, description FROM education")
        education_data['skills'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
        education_data = education_data.loc[:, education_data.columns != education_data.columns[0]]  # Supprimer la première colonne sans en-tête
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")
        st.write(skills_data)

        st.subheader('Ajouter une Formation ou une Expérience')
        add_type = st.selectbox('Type à ajouter', ['Formation', 'Expérience'])
        skills_options = fetch_data("SELECT skill_name FROM skills")['skill_name'].tolist()

        if add_type == 'Expérience':
            company = st.text_input('Entreprise')
            job_title = st.text_input('Titre du poste')
            start_date = st.date_input('Date de début')
            end_date = st.date_input('Date de fin')
            description = st.text_area('Description')
            selected_skills = st.multiselect('Compétences', skills_options)
            if st.button('Ajouter Expérience'):
                add_experience(company, job_title, str(start_date), str(end_date), description, selected_skills)
        elif add_type == 'Formation':
            institution = st.text_input('Institution')
            degree = st.text_input('Diplôme')
            start_date = st.date_input('Date de début')
            end_date = st.date_input('Date de fin')
            description = st.text_area('Description')
            selected_skills = st.multiselect('Compétences', skills_options)
            if st.button('Ajouter Formation'):
                add_education(institution, degree, str(start_date), str(end_date), description, selected_skills)

        st.subheader('Mettre à Jour une Formation ou une Expérience')
        update_type = st.selectbox('Type à mettre à jour', ['Formation', 'Expérience'])
        update_id = st.number_input('ID', min_value=1, step=1)
        if update_type == 'Expérience':
            job_title = st.text_input('Titre du poste', key='update_job_title')
            end_date = st.date_input('Date de fin', key='update_end_date')
            description = st.text_area('Description', key='update_description')
            selected_skills = st.multiselect('Compétences', skills_options, key='update_skills')
            if st.button('Mettre à Jour Expérience'):
                update_experience(job_title, str(end_date), description, selected_skills, update_id)
        elif update_type == 'Formation':
            degree = st.text_input('Diplôme', key='update_degree')
            end_date = st.date_input('Date de fin', key='update_edu_end_date')
            description = st.text_area('Description', key='update_edu_description')
            selected_skills = st.multiselect('Compétences', skills_options, key='update_edu_skills')
            if st.button('Mettre à Jour Formation'):
                update_education(degree, str(end_date), description, selected_skills, update_id)

        st.subheader('Supprimer une Formation ou une Expérience')
        delete_type = st.selectbox('Type à supprimer', ['Formation', 'Expérience'])
        delete_id = st.number_input('ID à supprimer', min_value=1, step=1)
        if delete_type == 'Expérience':
            if st.button('Supprimer Expérience'):
                delete_experience(delete_id)
        elif delete_type == 'Formation':
            if st.button('Supprimer Formation'):
                delete_education(delete_id)

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
        experiences['Type'] = 'Expérience'

        # Récupérer les formations
        educations = fetch_data("SELECT degree AS job_title, institution AS company, start_date, end_date FROM education")
        educations['Type'] = 'Formation'

        # Combiner les deux DataFrames
        timeline_data = pd.concat([experiences, educations], ignore_index=True)
        timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
        timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
        timeline_data['label'] = timeline_data.apply(lambda row: f"{row['job_title']} at {row['company']}", axis=1)

        # Créer le diagramme de Gantt avec Plotly
        fig = px.timeline(timeline_data, x_start="start_date", x_end="end_date", y="Type", color="Type", hover_name="label",
                          title="Frise Chronologique des Expériences et Formations")

        fig.update_yaxes(categoryorder="category ascending", showticklabels=False)
        fig.update_traces(textposition='outside', insidetextanchor='start', marker=dict(line=dict(width=0.5, color='Black')))
        fig.update_layout(showlegend=True)

        # Configuration de la légende pour une meilleure lisibilité
        fig.update_layout(
            legend=dict(
                title="Type d'activité",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Configuration des labels de survol pour une meilleure lisibilité
        fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><extra></extra>",
            textfont_size=10,  # Ajuster la taille de la police des labels
            insidetextanchor='middle'
        )

        st.plotly_chart(fig)

        st.header('Expériences')
        experience_data = fetch_data("SELECT id, job_title, company, start_date, end_date FROM experience")
        experience_data['skills'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
        st.write(experience_data)

        st.header('Formations')
        education_data = fetch_data("SELECT id, degree AS job_title, institution AS company, start_date, end_date FROM education")
        education_data['skills'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
        st.write(education_data)

        st.header('Compétences')
        skills_data = fetch_data("SELECT * FROM skills")

        # Créer un graphique en radar pour les compétences
        categories = skills_data['skill_name'].tolist()
        values = skills_data['proficiency'].tolist()

        radar_fig = go.Figure()

        radar_fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))

        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,  # Masquer les étiquettes de graduation
                    showline=False,  # Masquer la ligne de l'axe radial
                    ticks=''  # Masquer les graduations sur l'axe radial
                ),
                angularaxis=dict(
                    linewidth=1,
                    showline=True,
                    showticklabels=True,
                    color='grey'
                ),
                bgcolor='rgba(0,0,0,0)'  # Rendre le fond du radar transparent
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Rendre le fond de la zone de traçage transparent
            paper_bgcolor='rgba(0,0,0,0)',  # Rendre le fond du papier transparent
            showlegend=False,
            title="Compétences et leur Niveau de Maîtrise (%)"
        )

        st.plotly_chart(radar_fig)

else:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
