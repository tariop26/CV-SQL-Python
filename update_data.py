import sqlite3

# Fonction pour mettre à jour l'expérience professionnelle
def update_experience(job_title, end_date, description, id):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE experience
        SET job_title = ?, end_date = ?, description = ?
        WHERE id = ?
    """, (job_title, end_date, description, id))
    conn.commit()
    conn.close()
    print(f"Experience with id {id} updated successfully.")

# Fonction pour mettre à jour une compétence
def update_skill(proficiency, skill_name):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE skills
        SET proficiency = ?
        WHERE skill_name = ?
    """, (proficiency, skill_name))
    conn.commit()
    conn.close()
    print(f"Skill {skill_name} updated successfully.")

# Mise à jour des données
update_experience('Senior Data Analyst', '2022-12-01', 'Updated description of job responsibilities', 2)
update_skill(5, 'SQL')

import sqlite3

# Fonction pour mettre à jour l'expérience professionnelle
def update_experience(job_title, end_date, description, id):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE experience
        SET job_title = ?, end_date = ?, description = ?
        WHERE id = ?
    """, (job_title, end_date, description, id))
    conn.commit()
    conn.close()
    print(f"Experience with id {id} updated successfully.")

# Fonction pour mettre à jour une compétence
def update_skill(proficiency, skill_name):
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE skills
        SET proficiency = ?
        WHERE skill_name = ?
    """, (proficiency, skill_name))
    conn.commit()
    conn.close()
    print(f"Skill {skill_name} updated successfully.")

# Fonction pour créer les tables pour associer les compétences aux expériences et aux formations
def create_tables():
    conn = sqlite3.connect('cv_database.db')
    cursor = conn.cursor()

    # Créer les tables pour associer les compétences aux expériences et aux formations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experience_skills (
        experience_id INTEGER,
        skill_name TEXT,
        FOREIGN KEY (experience_id) REFERENCES experience(id),
        FOREIGN KEY (skill_name) REFERENCES skills(skill_name)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS education_skills (
        education_id INTEGER,
        skill_name TEXT,
        FOREIGN KEY (education_id) REFERENCES education(id),
        FOREIGN KEY (skill_name) REFERENCES skills(skill_name)
    );
    """)

    # Fermer la connexion à la base de données
    conn.commit()
    conn.close()
    print("Tables created successfully.")

# Mise à jour des données
update_experience('Senior Data Analyst', '2022-12-01', 'Updated description of job responsibilities', 2)
update_skill(5, 'SQL')

# Créer les tables
create_tables()
