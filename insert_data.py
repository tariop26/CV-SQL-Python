import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('cv_database.db')
cursor = conn.cursor()

# Supprimer toutes les données des tables
cursor.execute("DELETE FROM education_skills")
cursor.execute("DELETE FROM experience_skills")
cursor.execute("DELETE FROM education")
cursor.execute("DELETE FROM experience")
cursor.execute("DELETE FROM skills")
conn.commit()

# Dictionnaire des compétences avec les valeurs de pourcentage
skills_proficiency = {
    "SQL": 70,
    "Power BI": 75,
    "Wordpress": 80,
    "Python": 65,
    "Jupyter": 70,
    "Excel": 90,
    "Autonomie": 95,
    "Travail en équipe": 90,
    "Management": 90,
    "Commerce": 85,
    "Organisation de voyages": 95
}

# Fonction pour insérer ou mettre à jour les compétences
def upsert_skill(skill_name):
    proficiency = skills_proficiency.get(skill_name, 0)
    cursor.execute("SELECT proficiency FROM skills WHERE skill_name = ?", (skill_name,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO skills (skill_name, proficiency) VALUES (?, ?)", (skill_name, proficiency))
    else:
        current_proficiency = row[0]
        if proficiency > current_proficiency:
            cursor.execute("UPDATE skills SET proficiency = ? WHERE skill_name = ?", (proficiency, skill_name))

# Liste des expériences à insérer
experiences = [
    {
        "company": "COMMUNAUTÉ AGGLOMÉRATION PAYS VOIRONNAIS - SERVICE TOURISME",
        "job_title": "Conception et mise en place d'un observatoire du tourisme pour le territoire",
        "start_date": "2024-03-01",
        "end_date": "2024-09-01",
        "description": "Récolte, analyse et visualisation des données pour fournir aux décideurs des informations fiables, facilitant ainsi la planification du développement futur du tourisme. Voiron",
        "skills": ["Excel","SQL", "Power BI", "Autonomie"]
    },
    {
        "company": "DÉVELOPPEUR WORDPRESS INDÉPENDANT",
        "job_title": "Création et maintenance de sites internet Wordpress",
        "start_date": "2022-01-01",
        "end_date": None,
        "description": "Création et maintenance de sites internet Wordpress.",
        "skills": ["Autonomie","Wordpress"]
    },
    {
        "company": "CONGÉ SABBATIQUE PERSONNEL - SUIVI DE CONJOINT",
        "job_title": "Expérience de vie aux États-Unis (Denver, Colorado) en famille pendant 2 années",
        "start_date": "2021-07-01",
        "end_date": "2023-08-01",
        "description": "Expérience de vie aux États-Unis (Denver, Colorado) en famille pendant 2 années.",
        "skills": ["Organisation de voyages"]
    },
    {
        "company": "ADJOINT DE DIRECTION ROC FRANCE (AREAS)",
        "job_title": "Manager (20 employés) et assistant administratif 3 magasins Franprix et station-service Esso d'autoroute",
        "start_date": "2018-05-01",
        "end_date": "2021-06-01",
        "description": "Manager (20 employés) et assistant administratif 3 magasins Franprix et station-service Esso d'autoroute. Drôme",
        "skills": ["Travail en équipe","Management","Excel", "Commerce"]
    },
    {
        "company": "DIRECTEUR DE SITE HUTTOPIA",
        "job_title": "Directeur de villages-vacances",
        "start_date": "2013-01-01",
        "end_date": "2018-02-01",
        "description": "Manager de 20 personnes. Font-Romeu & Divonne-les-Bains",
        "skills": ["Travail en équipe","Management","Commerce"]
    },
    {
        "company": "CHARGÉ DE PROJETS ÉVÉNEMENTS ET VOYAGES",
        "job_title": "Agent de voyages multitâches",
        "start_date": "2010-09-01",
        "end_date": "2013-01-01",
        "description": "Agent de voyages multitâches. Lyon",
        "skills": ["Organisation de voyages","Commerce"]
    },
    {
        "company": "COMMERCIAL PETIT FUTÉ",
        "job_title": "Création d'un portefeuille de 40 clients (hôtels et agences de voyages principalement) en Tanzanie et 60 en Afrique du Sud",
        "start_date": "2009-01-01",
        "end_date": "2010-12-01",
        "description": "Création d'un portefeuille de 40 clients (hôtels et agences de voyages principalement) en Tanzanie et 60 en Afrique du Sud. Auto-entrepreneur",
        "skills": ["Autonomie","Organisation de voyages","Commerce"]
    },
    {
        "company": "DIRECTEUR DE SITE AMERICAN VILLAGE",
        "job_title": "Manager d'une équipe d'animateurs anglophones et responsable de 50 enfants par quinzaine",
        "start_date": "2007-06-01",
        "end_date": "2010-09-01",
        "description": "Manager d'une équipe d'animateurs anglophones et responsable de 50 enfants par quinzaine. Mâcon",
        "skills": ["Travail en équipe","Management"]
    },
    {
        "company": "RESPONSABLE JARDIN D'ENFANTS MAGIC IN MOTION",
        "job_title": "Responsable du jardin d'enfants, aide-moniteur, création d'événements",
        "start_date": "2006-12-01",
        "end_date": "2007-03-01",
        "description": "Responsable du jardin d'enfants, aide-moniteur, création d'événements.Courchevel",
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
        upsert_skill(skill)

# Liste des formations à insérer
formations = [
    {
        "institution": "Databird",
        "degree": "Formation Data Analyst",
        "start_date": "2024-02-01",
        "end_date": "2024-07-01",
        "description": "Base de données, Analyse et traitement de données, Data visualisation, Analyse statistique, Python, Jupyter, SQL, Power BI",
        "field_of_study": "Data Analysis",
        "skills": ["Python", "Jupyter", "SQL", "Power BI","Travail en équipe", "Autonomie"]
    },
    {
        "institution": "WPChef",
        "degree": "Certification pro. développeur Wordpress (RS5170)",
        "start_date": "2021-09-01",
        "end_date": "2021-12-01",
        "description": "Certification pro. développeur Wordpress.",
        "field_of_study": "Développement Web",
        "skills": ["Wordpress","Autonomie"]
    },
    {
        "institution": "UJF Grenoble",
        "degree": "Master 1 Sport & Tourisme",
        "start_date": "2003-09-01",
        "end_date": "2006-09-01",
        "description": "Master 1 Sport & Tourisme.",
        "field_of_study": "Sport & Tourisme",
        "skills": ["Travail en équipe","Organisation de voyages"]
    },
    {
        "institution": "UFR Staps - Besançon",
        "degree": "Licence 1 Sport",
        "start_date": "2002-09-01",
        "end_date": "2003-06-30",
        "description": "1ère année de fac de sport, option handball",
        "field_of_study": "Sport",
        "skills": ["Autonomie"]
    },
    {
        "institution": "Lycée Condorcet - Belfort",
        "degree": "Baccalauréat scientifique",
        "start_date": "2000-09-01",
        "end_date": "2002-06-30",
        "description": "Lycée général. Option maths en terminal.",
        "field_of_study": "Sciences, Maths",
        "skills": ["Autonomie"]
    }
]

# Insérer les formations dans la base de données
for edu in formations:
    cursor.execute("""
        INSERT INTO education (institution, degree, field_of_study, start_date, end_date, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (edu['institution'], edu['degree'], edu['field_of_study'], edu['start_date'], edu['end_date'], edu['description']))
    edu_id = cursor.lastrowid
    for skill in edu['skills']:
        cursor.execute("""
            INSERT INTO education_skills (education_id, skill_name)
            VALUES (?, ?)
        """, (edu_id, skill))
        upsert_skill(skill)

# Commit des modifications et fermer la connexion
conn.commit()
conn.close()
