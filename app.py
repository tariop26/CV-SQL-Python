import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from streamlit_folium import st_folium
import folium
import altair as alt
from auth import authenticate
from matplotlib_venn import venn3
from collections import defaultdict

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

def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

def skill_distribution():
    data = fetch_data("""
        SELECT es.skill_name, COUNT(*) as count
        FROM experience_skills es
        GROUP BY es.skill_name
    """)
    fig = alt.Chart(data).mark_bar().encode(
        x=alt.X('count:Q', axis=alt.Axis(title=None, labels=True, tickMinStep=1, tickCount=5, format='d')),
        y=alt.Y('skill_name:N', axis=alt.Axis(title=None, labels=True, ticks=True, domain=True))
    ).properties(
        title=''
    )
    st.altair_chart(fig, use_container_width=True)

def interactive_timeline():
    timeline_data = fetch_data("""
        SELECT job_title AS label, start_date, end_date, 'Expérience' AS type FROM experience
        UNION ALL
        SELECT degree AS label, start_date, end_date, 'Formation' AS type FROM education
    """)
    timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
    timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
    fig = go.Figure()
    colors = {'Expérience': 'green', 'Formation': 'blue'}

    for _, row in timeline_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['start_date'], row['end_date']],
            y=[row['type'], row['type']],
            mode='lines+markers',
            line=dict(color=colors[row['type']], width=2),
            marker=dict(size=10),
            text=row['label'],
            hoverinfo='text'
        ))

    fig.update_layout(
        title='',
        xaxis=dict(title='Date'),
        yaxis=dict(title='', tickvals=['Expérience', 'Formation']),
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        height=400
    )
    st.plotly_chart(fig)

def radar_chart():
    skills = ['SQL', 'Power BI', 'Wordpress', 'Python', 'Excel', 'Autonomie', 'Travail en équipe', 'Management', 'Organisation de voyages']
    proficiency = [70, 75, 80, 65, 90, 95, 90, 90, 95]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=proficiency,
        theta=skills,
        fill='toself',
        name='Proficiency',
        fillcolor='rgba(0, 191, 255, 0.2)',
        line=dict(color='rgba(0, 191, 255, 1)')
    ))

    fig.update_layout(
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
        title=""
    )

    st.plotly_chart(fig)

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
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        text=text,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Les relations inter-compétences',  # Mettre à jour le titre ici
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2))
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        height=800,  # Augmenter la hauteur ici
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    st.plotly_chart(fig)
    st.markdown(
            """
            **Explication du Réseau de Compétences :**

            Ce graphique montre un réseau de compétences basé sur les expériences professionnelles. Chaque nœud représente soit un poste occupé, soit une compétence acquise. Les lignes entre les nœuds indiquent quelles compétences ont été utilisées dans quels postes. 

            Cela permet de visualiser les relations et les connexions entre les différentes compétences et les postes. Vous pouvez voir quelles compétences sont partagées entre plusieurs postes et identifier les compétences centrales qui jouent un rôle crucial dans plusieurs expériences professionnelles.
            """
        )


def skill_progression():
    progression_data = fetch_data("""
        SELECT skill_name, date, proficiency
        FROM skill_progression
        ORDER BY date
    """)
    fig = go.Figure()

    for skill in progression_data['skill_name'].unique():
        skill_data = progression_data[progression_data['skill_name'] == skill]
        fig.add_trace(go.Scatter(
            x=skill_data['date'],
            y=skill_data['proficiency'],
            mode='lines+markers',
            name=skill
        ))

    fig.update_layout(
        title='Progression des compétences',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Proficiency'),
        height=400
    )

def employment_duration_histogram(width=6, height=4):
    data = fetch_data("""
        SELECT job_title, start_date, end_date
        FROM experience
    """)
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])
    data['duration'] = (data['end_date'] - data['start_date']).dt.days / 30  # Durée en mois

        # Calcul des statistiques
    median_duration = data['duration'].median()
    mean_duration = data['duration'].mean()
    min_duration = data['duration'].min()
    max_duration = data['duration'].max()
    
    fig, ax = plt.subplots(figsize=(width / 100, height / 100))  # Ajuster la taille (6 pouces en largeur, 4 en hauteur)
    sns.histplot(data['duration'], bins=10, kde=False, ax=ax)
    ax.set_title("")
    ax.set_xlabel("Nbre de mois")
    ax.set_ylabel("Nombre d'emplois")

    # Encapsuler le graphique dans un conteneur avec des dimensions spécifiées
    placeholder = st.empty()
    with placeholder.container():
        st.pyplot(fig)
        st.markdown("Cet histogramme montre la durée de chaque emploi en mois. On y constate que je suis resté majoritairement entre 20 et 40 mois pour chaque emploi.")
        st.markdown(
            f"""
            **Statistiques des Durées d'Emploi :**
            - Durée médiane : {median_duration:.2f} mois
            - Durée moyenne : {mean_duration:.2f} mois
            - Durée minimale : {min_duration:.2f} mois
            - Durée maximale : {max_duration:.2f} mois
            """
        )

def fetch_locations():
    data = {
        "Lieu": ["Voiron, France", "Denver, Colorado, USA", "Drôme, France", "Font-Romeu, France", "Divonne-les-Bains, France", "Lyon, France", "Tanzanie", "Afrique du Sud", "Mâcon, France", "Courchevel, France"],
        "Latitude": [45.367, 39.7392, 44.7631, 42.5037, 46.356, 45.764, -6.369, -30.5595, 46.306, 45.414],
        "Longitude": [5.5788, -104.9903, 5.424, 1.982, 6.139, 4.835, 34.8888, 22.9375, 4.830, 6.631]
    }
    return pd.DataFrame(data)

def create_map(data):
    m = folium.Map(location=[45.764, 4.8357], zoom_start=2.5)  # Centré sur la France par défaut
    for _, row in data.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Lieu']).add_to(m)
    return m

st.set_page_config(layout="wide")
st.title('CV de Manuel Poirat')
st.markdown("[Voir mon CV \"classique\"](https://tariop26.github.io/)")
# Suppression de la barre de navigation
st.markdown(
    """
    <style>
    .css-18e3th9 { visibility: hidden; }
    .css-1d391kg { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["Mes expériences", "Mes compétences", "Itinéraire d'un baroudeur"])

with tab1:
    st.header('Mes expériences et formations au fil du temps')
    interactive_timeline()
    
    st.header("L'école, c'est bien...")
    education_data = fetch_data("SELECT id, degree AS 'Diplôme', institution AS 'Institution', start_date AS 'Date de début', end_date AS 'Date de fin' FROM education")
    education_data['Compétences'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
    st.write(education_data, use_container_width=True)
    
    st.header("Le travail, c'est mieux !")
    experience_data = fetch_data("SELECT id, job_title AS 'Titre du poste', company AS 'Entreprise', start_date AS 'Date de début', end_date AS 'Date de fin' FROM experience")
    experience_data['Compétences'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
    st.write(experience_data, use_container_width=True)

    st.header('Combien de temps suis-je resté à chaque poste ?')
    employment_duration_histogram(width=600, height=400)
    

with tab2:
    st.header('Un professionnel aux multiples talents')
    col1, col2, col3 = st.columns([1, 0.1, 1])
    
    with col1:
        st.subheader('Répartition des compétences à travers les expériences')
        skill_distribution()
    
    with col3:
        st.subheader('Niveau de compétence par domaine')
        radar_chart()
        
    st.header('Réseau de Compétences')
    skill_network()

with tab3:
    st.header('Carte des Lieux où j\'ai Travaillé')
    location_data = fetch_locations()
    map_ = create_map(location_data)
    st_folium(map_, width=1200, height=800)
    st.markdown(
            """
            Quelques mois en Afrique, quelques années aux Etats-Unis et une bonne partie en Rhône-Alpes !
            """
        )
