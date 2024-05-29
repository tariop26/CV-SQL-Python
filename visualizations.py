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

# Visualisation 1: Nombre d'expériences par entreprise
query_experience = """
    SELECT 
        company, 
        COUNT(*) as num_experiences
    FROM experience
    GROUP BY company;
"""
experience_data = fetch_data(query_experience)
plt.figure(figsize=(10, 6))
sns.barplot(x='num_experiences', y='company', data=experience_data)
plt.title('Number of Experiences by Company')
plt.xlabel('Number of Experiences')
plt.ylabel('Company')
plt.savefig('visualizations/experience_by_company.png')
plt.show()

# Visualisation 2: Compétences triées par niveau de maîtrise
query_skills = """
    SELECT 
        skill_name, 
        proficiency
    FROM skills
    ORDER BY proficiency DESC;
"""
skills_data = fetch_data(query_skills)
plt.figure(figsize=(10, 6))
sns.barplot(x='proficiency', y='skill_name', data=skills_data)
plt.title('Skills Ordered by Proficiency')
plt.xlabel('Proficiency Level')
plt.ylabel('Skill')
plt.savefig('visualizations/skills_by_proficiency.png')
plt.show()

# Visualisation 3: Nombre de projets utilisant chaque compétence
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
plt.figure(figsize=(10, 6))
sns.barplot(x='num_projects', y='skill_name', data=projects_data)
plt.title('Number of Projects by Skill')
plt.xlabel('Number of Projects')
plt.ylabel('Skill')
plt.savefig('visualizations/projects_by_skill.png')
plt.show()
