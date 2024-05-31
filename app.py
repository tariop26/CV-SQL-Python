import streamlit as st

# Appeler st.set_page_config au tout début
st.set_page_config(layout="wide")

import sqlite3
import pandas as pd
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
import networkx as nx
from streamlit_folium import st_folium
import folium
import altair as alt
from auth import authenticate

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

def fetch_skills_data():
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query("""
        SELECT es.skill_name, e.job_title, COUNT(*) as count
        FROM experience_skills es
        JOIN experience e ON es.experience_id = e.id
        GROUP BY es.skill_name, e.job_title
    """, conn)
    conn.close()
    return data

def skill_distribution():
    data = fetch_data("""
        SELECT es.skill_name, COUNT(*) as count
        FROM experience_skills es
        GROUP BY es.skill_name
    """)
    fig = alt.Chart(data).mark_bar().encode(
        x='count:Q',
        y=alt.Y('skill_name:N', sort='-x')
    ).properties(
        title='Distribution des Compétences'
    )
    st.altair_chart(fig, use_container_width=True)

def skill_heatmap():
    data = fetch_skills_data()
    heatmap_data = data.pivot("skill_name", "job_title", "count").fillna(0)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
    plt.title('Heatmap des Compétences par Poste')
    st.pyplot(fig)

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
        title='Chronologie Interactive des Expériences et Formations',
        xaxis=dict(title='Date'),
        yaxis=dict(title=''),
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        height=400
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
                title='Connexions de Nœuds',  # Mettre à jour le titre ici
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2))
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Réseau de Compétences',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        height=800,  # Augmenter la hauteur ici
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    st.plotly_chart(fig)

def fetch_locations():
    data = {
        "Lieu": ["Voiron, France", "Denver, Colorado, USA", "Drôme, France", "Font-Romeu, France", "Divonne-les-Bains, France", "Lyon, France", "Tanzanie", "Afrique du Sud", "Mâcon, France", "Courchevel, France"],
        "Latitude": [45.367, 39.7392, 44.7631, 42.5037, 46.356, 45.764, -6.369, -30.5595, 46.306, 45.414],
        "Longitude": [5.5788, -104.9903, 5.424, 1.982, 6.139, 4.835, 34.8888, 22.9375, 4.830, 6.631]
    }
    return pd.DataFrame(data)

def create_map(data):
    m = folium.Map(location=[20, 0], zoom_start=2)
    for _, row in data.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Lieu']).add_to(m)
    return m

def radar_chart():
    skills_data = {
        'Competence': ['SQL', 'Power BI', 'Wordpress', 'Python', 'Excel', 'Autonomie', 'Travail en équipe', 'Management', 'Organisation de voyages'],
        'Proficiency': [70, 75, 80, 65, 90, 95, 90, 90, 95]
    }
    df_skills = pd.DataFrame(skills_data)

    radar_fig = go.Figure()

    radar_fig.add_trace(go.Scatterpolar(
        r=df_skills['Proficiency'],
        theta=df_skills['Competence'],
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

st.title('CV de Manuel Poirat - Formations et expériences professionnelles')

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

tab1, tab2, tab3, tab4 = st.tabs(["Accueil", "Compétences", "Analyses", "Carte"])

with tab1:
    st.header('Frise Chronologique des Expériences et Formations')
    interactive_timeline()
    
    st.header('Expériences')
    experience_data = fetch_data("SELECT id, job_title AS 'Titre du poste', company AS 'Entreprise', start_date AS 'Date de début', end_date AS 'Date de fin' FROM experience")
    experience_data['Compétences'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
    st.write(experience_data, use_container_width=True)

    st.header('Formations')
    education_data = fetch_data("SELECT id, degree AS 'Diplôme', institution AS 'Institution', start_date AS 'Date de début', end_date AS 'Date de fin' FROM education")
    education_data['Compétences'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
    st.write(education_data, use_container_width=True)

with tab2:
    col1, col2, col3 = st.columns([2, 0.1, 2])  # Ajuster les largeurs des colonnes ici

    with col1:
        st.header('Distribution des Compétences')
        skill_distribution()
    
    with col2:
        st.write("")  # Colonne intermédiaire vide et étroite
        
    with col3:
        st.header('Radar des Compétences')
        radar_chart()

    st.header('Réseau de Compétences')
    skill_network()

with tab3:
    st.header('Heatmap des Compétences par Poste')
    skill_heatmap()

with tab4:
    st.header('Carte des Lieux où j\'ai Travaillé')
    
    location_data = fetch_locations()
    map_ = create_map(location_data)
    st_folium(map_, width=700, height=500)
