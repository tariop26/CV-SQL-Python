import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('cv_database.db')
cursor = conn.cursor()

# Supprimer toutes les données existantes
cursor.execute("DELETE FROM education")
cursor.execute("DELETE FROM experience")
cursor.execute("DELETE FROM skills")
cursor.execute("DELETE FROM projects")

# Liste des expériences à insérer
experiences = [
    {
        "company": "COMMUNAUTÉ AGGLOMÉRATION PAYS VOIRONNAIS - SERVICE TOURISME",
        "job_title": "Conception et mise en place d'un observatoire du tourisme pour le territoire",
        "start_date": "2024-03-01",
        "end_date": "2024-09-01",
        "description": "Récolte, analyse et visualisation des données pour fournir aux décideurs des informations fiables, facilitant ainsi la planification du développement futur du tourisme. Voiron",
        "skills": ["Excel", "SQL", "Power BI", "Autonomie"]
    },
    {
        "company": "DÉVELOPPEUR WORDPRESS INDÉPENDANT",
        "job_title": "Création et maintenance de sites internet Wordpress",
        "start_date": "2022-01-01",
        "end_date": None,
        "description": "Création et maintenance de sites internet Wordpress.",
        "skills": ["Autonomie", "Wordpress"]
    },
    {
        "company": "CONGÉ SABBATIQUE PERSONNEL - SUIVI DE CONJOINT",
        "job_title": "Expérience de vie aux États-Unis (Denver, Colorado) en famille pendant 2 années",
        "start_date": "2021-07-01",
        "end_date": "2023-08-01",
        "description": "Expérience de vie aux États-Unis (Denver, Colorado) en famille pendant 2 années.",
        "skills": []
    },
    {
        "company": "ADJOINT DE DIRECTION ROC FRANCE (AREAS)",
        "job_title": "Manager (20 employés) et assistant administratif 3 magasins Franprix et station-service Esso d'autoroute",
        "start_date": "2018-05-01",
        "end_date": "2021-06-01",
        "description": "Manager (20 employés) et assistant administratif 3 magasins Franprix et station-service Esso d'autoroute. Drôme",
        "skills": ["Travail en équipe", "Management", "Excel"]
    },
    {
        "company": "DIRECTEUR DE SITE HUTTOPIA",
        "job_title": "Directeur de villages-vacances",
        "start_date": "2013-01-01",
        "end_date": "2018-02-01",
        "description": "Manager de 20 personnes. Font-Romeu & Divonne-les-Bains",
        "skills": ["Travail en équipe", "Management"]
    },
    {
        "company": "CHARGÉ DE PROJETS ÉVÉNEMENTS ET VOYAGES",
        "job_title": "Agent de voyages multitâches",
        "start_date": "2010-09-01",
        "end_date": "2013-01-01",
        "description": "Agent de voyages multitâches. Lyon",
        "skills": []
    },
    {
        "company": "COMMERCIAL PETIT FUTÉ",
        "job_title": "Création d'un portefeuille de 40 clients (hôtels et agences de voyages principalement) en Tanzanie et 60 en Afrique du Sud",
        "start_date": "2009-01-01",
        "end_date": "2010-12-01",
        "description": "Création d'un portefeuille de 40 clients (hôtels et agences de voyages principalement) en Tanzanie et 60 en Afrique du Sud. Auto-entrepreneur",
        "skills": ["Autonomie"]
    },
    {
        "company": "DIRECTEUR DE SITE AMERICAN VILLAGE",
        "job_title": "Manager d'une équipe d'animateurs anglophones et responsable de 50 enfants par quinzaine",
        "start_date": "2007-06-01",
        "end_date": "2010-09-01",
        "description": "Manager d'une équipe d'animateurs anglophones et responsable de 50 enfants par quinzaine. Mâcon",
        "skills": []
    },
    {
        "company": "RESPONSABLE JARDIN D'ENFANTS MAGIC IN MOTION",
        "job_title": "Responsable du jardin d'enfants, aide-moniteur, création d'événements",
        "start_date": "2006-12-01",
        "end_date": "2007-03-01",
        "description": "Responsable du jardin d'enfants, aide-moniteur, création d'événements. Courchevel",
        "skills": ["Travail en équipe"]
    }
]

# Insérer les expériences dans la base de données
for exp in experiences:
    cursor.execute("""
        INSERT INTO experience (company, job_title, start_date, end_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (exp['company'], exp['job_title'], exp['start_date'], exp['end_date'], exp['description']))
    exp_id = cursor.lastrowid
    for skill in exp['skills']:
        cursor.execute("""
            INSERT INTO experience_skills (experience_id, skill_name)
            VALUES (?, ?)
        """, (exp_id, skill))

# Liste des formations à insérer
formations = [
    {
        "institution": "Databird",
        "degree": "Formation Data Analyst",
        "start_date": "2024-02-01",
        "end_date": "2024-07-01",
        "description": "Base de données, Analyse et traitement de données, Data visualisation, Analyse statistique, Python, Jupyter, SQL, Power BI",
        "field_of_study": "Data Analysis",
        "skills": ["Python", "Jupyter", "SQL", "Power BI", "Travail en équipe", "Autonomie"]
    },
    {
        "institution": "WPChef",
        "degree": "Certification pro. développeur Wordpress (RS5170)",
        "start_date": "2021-09-01",
        "end_date": "2021-12-01",
        "description": "Certification pro. développeur Wordpress.",
        "field_of_study": "Développement Web",
        "skills": ["Wordpress", "Autonomie"]
    },
    {
        "institution": "UJF Grenoble",
        "degree": "Master 1 Sport & Tourisme",
        "start_date": "2003-09-01",
        "end_date": "2006-09-01",
        "description": "Master 1 Sport & Tourisme.",
        "field_of_study": "Sport & Tourisme",
        "skills": []
    }
]

# Insérer les formations dans la base de données
for edu in formations:
    cursor.execute("""
        INSERT INTO education (institution, degree, start_date, end_date, description, field_of_study)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (edu['institution'], edu['degree'], edu['start_date'], edu['end_date'], edu['description'], edu['field_of_study']))
    edu_id = cursor.lastrowid
    for skill in edu['skills']:
        cursor.execute("""
            INSERT INTO education_skills (education_id, skill_name)
            VALUES (?, ?)
        """, (edu_id, skill))

# Commit des modifications et fermer la connexion
conn.commit()
conn.close()
