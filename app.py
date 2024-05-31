import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from auth import authenticate
import random
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import folium
from streamlit_folium import st_folium

# Configurer Streamlit pour utiliser toute la largeur de l'écran
st.set_page_config(layout="wide")

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour la distribution des compétences
def skill_distribution():
    data = fetch_data("""
        SELECT e.job_title, es.skill_name
        FROM experience_skills es
        JOIN experience e ON es.experience_id = e.id
    """)
    plt.figure(figsize=(10, 6))
    sns.countplot(y='skill_name', hue='job_title', data=data, palette='viridis')
    plt.title('Distribution des Compétences par Type d\'Expérience')
    st.pyplot(plt)

# Fonction pour créer une chronologie interactive
def interactive_timeline():
    timeline_data = fetch_data("""
        SELECT job_title AS label, start_date, end_date, 'Expérience' AS type FROM experience
        UNION ALL
        SELECT degree AS label, start_date, end_date, 'Formation' AS type FROM education
    """)
    timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
    timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
    fig = px.timeline(timeline_data, x_start="start_date", x_end="end_date", y="type", color="type", text="label",
                      title="Chronologie Interactive des Expériences et Formations")
    fig.update_yaxes(categoryorder="category ascending")
    st.plotly_chart(fig)

# Fonction pour créer un nuage de mots alternatif avec matplotlib
def generate_wordcloud():
    data = fetch_data("SELECT description FROM experience")
    text = ' '.join(data['description'].tolist())
    words = pd.Series(text.split()).value_counts().head(50)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    words.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('Top 50 Words in Job Descriptions')
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Words')
    st.pyplot(fig)

# Fonction pour créer un réseau de compétences
def skill_network():
    data = fetch_data("""
        SELECT e.job_title, es.skill_name
        FROM experience_skills es
        JOIN experience e ON es.experience_id = e.id
    """)
    G = nx.Graph()
    for _, row in data.iterrows():
        G.add_edge(row['job_title'], row['skill_name'])
    
    pos = nx.spring_layout(G)
    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
    
    node_trace = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += [x]
        node_trace['y'] += [y]
        node_trace['text'] += [node]
    
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Réseau de Compétences',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    st.plotly_chart(fig)

# Fonction pour créer une carte des lieux
def location_map():
    data = fetch_data("SELECT company, job_title, description FROM experience")
    locations = {
        'COMMUNAUTÉ AGGLOMÉRATION PAYS VOIRONNAIS - SERVICE TOURISME': [45.3674, 5.5939],
        'DÉVELOPPEUR WORDPRESS INDÉPENDANT': [39.7392, -104.9903],  # Exemple de localisation à Denver
        'ROC FRANCE (AREAS)': [44.8998, 5.7191],  # Drôme
        'HUTTOPIA': [42.5078, 2.0684],  # Font-Romeu
        'ÉVÉNEMENTS ET VOYAGES': [45.7640, 4.8357],  # Lyon
        'Petit Futé': [-6.369028, 34.888822],  # Tanzanie
        'American Village': [46.3064, 4.8286],  # Mâcon
        'Magic in Motion': [45.4153, 6.6314]  # Courchevel
    }
    
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    for idx, row in data.iterrows():
        if row['company'] in locations:
            folium.Marker(locations[row['company']], popup=row['description']).add_to(m)
    
    st.header('Carte des Lieux où J\'ai Travaillé')
    st_folium(m, width=700, height=450)

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

    # Tableau de bord interactif pour les utilisateurs
    else:
        st.header('CV de Manuel Poirat - Formations et expériences professionnelles')
        st.image("https://path_to_your_image.jpg", width=200)
        st.markdown("[Télécharger mon CV au format PDF](https://tariop26.github.io/)")

        # Ajouter des onglets de navigation
        tab1, tab2, tab3, tab4 = st.tabs(['Chronologie & Récapitulatif', 'Compétences', 'Analyses & Nuage de Mots', 'Carte des Lieux'])
        
        with tab1:
            st.header('Chronologie Interactive')
            interactive_timeline()
            
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

        with tab2:
            st.header('Distribution des Compétences')
            skill_distribution()
            
            st.header('Réseau de Compétences')
            skill_network()
        
        with tab3:
            st.header('Nuage de Mots des Descriptions de Postes')
            generate_wordcloud()

            st.header('Heatmap des Compétences')
            skill_heatmap()
        
        with tab4:
            st.header('Carte des Lieux où J\'ai Travaillé')
            location_map()

else:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
