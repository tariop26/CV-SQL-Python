import streamlit as st
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
                title='Node Connections',
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
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    st.plotly_chart(fig)

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

st.set_page_config(layout="wide")
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

tab1, tab2, tab3, tab4 = st.tabs(["Accueil", "Compétences", "Descriptions", "Carte"])

with tab1:
    st.header('Frise Chronologique des Expériences et Formations')
    interactive_timeline()
    
    st.header('Expériences')
    experience_data = fetch_data("SELECT id, job_title AS 'Titre du poste', company AS 'Entreprise', start_date AS 'Date de début', end_date AS 'Date de fin' FROM experience")
    experience_data['Compétences'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
    st.write(experience_data)

    st.header('Formations')
    education_data = fetch_data("SELECT id, degree AS 'Diplôme', institution AS 'Institution', start_date AS 'Date de début', end_date AS 'Date de fin' FROM education")
    education_data['Compétences'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
    st.write(education_data)

with tab2:
    st.header('Distribution des Compétences')
    skill_distribution()
    st.header('Réseau de Compétences')
    skill_network()

with tab3:
    st.header('Nuage de Mots des Descriptions de Poste')
    generate_wordcloud()

with tab4:
    location_map()
