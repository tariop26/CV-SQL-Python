import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import folium
from streamlit_folium import st_folium

# Fonction pour obtenir les données d'une requête SQL
def fetch_data(query):
    conn = sqlite3.connect('cv_database.db')
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Fonction pour obtenir les compétences
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

# Configuration de la page
st.set_page_config(layout="wide")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["Accueil", "Compétences", "Descriptions", "Carte"])

# Page d'accueil
if page == "Accueil":
    st.title('CV de Manuel Poirat - Formations et expériences professionnelles')

    st.header('Frise Chronologique des Expériences et Formations')
    
    # Récupérer les expériences
    experiences = fetch_data("SELECT job_title, company, start_date, end_date FROM experience")
    experiences['type'] = 'Expérience'
    experiences['y'] = 'Expérience'
    experiences['color'] = 'blue'

    # Récupérer les formations
    educations = fetch_data("SELECT degree AS job_title, institution AS company, start_date, end_date FROM education")
    educations['type'] = 'Formation'
    educations['y'] = 'Formation'
    educations['color'] = 'red'

    # Combiner les deux DataFrames
    timeline_data = pd.concat([experiences, educations], ignore_index=True)
    timeline_data['start_date'] = pd.to_datetime(timeline_data['start_date'])
    timeline_data['end_date'] = pd.to_datetime(timeline_data['end_date'])
    timeline_data['label'] = timeline_data.apply(lambda row: f"{row['job_title']} at {row['company']}", axis=1)

    fig = px.timeline(timeline_data, x_start="start_date", x_end="end_date", y="y", color="type", text="label",
                      color_discrete_map={'Formation': 'red', 'Expérience': 'blue'})
    
    fig.update_layout(
        yaxis_title="",
        xaxis_title="",
        yaxis=dict(ticktext=['Formation', 'Expérience'], tickvals=['Formation', 'Expérience']),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header('Expériences')
    experience_data = fetch_data("SELECT id, job_title, company, start_date, end_date FROM experience")
    experience_data['Compétences'] = experience_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'experience')))
    st.write(experience_data.rename(columns={
        'job_title': 'Titre du poste',
        'company': 'Entreprise',
        'start_date': 'Date de début',
        'end_date': 'Date de fin'
    }))

    st.header('Formations')
    education_data = fetch_data("SELECT id, degree AS job_title, institution AS company, start_date, end_date FROM education")
    education_data['Compétences'] = education_data['id'].apply(lambda x: ', '.join(fetch_skills_for_item(x, 'education')))
    st.write(education_data.rename(columns={
        'job_title': 'Diplôme',
        'company': 'Institution',
        'start_date': 'Date de début',
        'end_date': 'Date de fin'
    }))

# Page des compétences
elif page == "Compétences":
    st.header('Distribution des Compétences')
    skills_data = fetch_data("SELECT skill_name AS Compétence, proficiency AS Maîtrise FROM skills")
    st.bar_chart(skills_data.set_index('Compétence'))

    st.header('Réseau de Compétences')
    def skill_network():
        skills = fetch_data("SELECT skill_name FROM skills")
        skill_list = skills['skill_name'].tolist()
        G = nx.Graph()
        
        for skill in skill_list:
            G.add_node(skill)
        
        for exp_id in fetch_data("SELECT id FROM experience")['id']:
            exp_skills = fetch_skills_for_item(exp_id, 'experience')
            for i in range(len(exp_skills)):
                for j in range(i + 1, len(exp_skills)):
                    G.add_edge(exp_skills[i], exp_skills[j])
        
        pos = nx.spring_layout(G, k=0.5, iterations=50)
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
        node_text = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                color=[],
                line_width=2
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Réseau de Compétences',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            height=800,
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))
        
        st.plotly_chart(fig, use_container_width=True)
    
    skill_network()

# Page des descriptions
elif page == "Descriptions":
    st.header('Nuage de Mots des Descriptions de Postes')
    experiences = fetch_data("SELECT description FROM experience")
    text = ' '.join(experiences['description'].tolist())
    wordcloud = WordCloud(background_color='white').generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

    st.header('Heatmap des Compétences')
    skills_data = fetch_data("SELECT skill_name, proficiency FROM skills")
    skills_data = skills_data.pivot("skill_name", "proficiency", "proficiency")
    st.heatmap(skills_data, cmap='coolwarm', annot=True)

# Page de la carte
elif page == "Carte":
    st.header('Carte des Lieux où j\'ai Travaillé')
    
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
    
    location_data = fetch_locations()
    map_ = create_map(location_data)
    st_folium(map_, width=700, height=500)
