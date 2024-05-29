import sqlite3
import pandas as pd

# Fonction pour exécuter une requête SQL et afficher les résultats
def execute_query(query):
    conn = sqlite3.connect('cv_database.db')
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

# Liste des requêtes SQL à exécuter
queries = {
    "All education entries": "SELECT * FROM education;",
    "Education status": """
        SELECT 
            institution, 
            degree, 
            field_of_study, 
            start_date, 
            end_date,
            CASE 
                WHEN end_date IS NOT NULL THEN 'Completed'
                ELSE 'In Progress'
            END AS status
        FROM education;
    """,
    "Experience count by company": """
        SELECT 
            company, 
            COUNT(*) as num_experiences
        FROM experience
        GROUP BY company;
    """,
    "Skills ordered by proficiency": """
        SELECT 
            skill_name, 
            proficiency
        FROM skills
        ORDER BY proficiency DESC;
    """,
    "Project counts by skill": """
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
    """,
    "Top 5 skills by proficiency": """
        SELECT 
            skill_name, 
            proficiency
        FROM skills
        ORDER BY proficiency DESC
        LIMIT 5;
    """
}

# Exécuter chaque requête et afficher les résultats
for query_name, query in queries.items():
    print(f"\n--- {query_name} ---")
    result = execute_query(query)
    print(result)

