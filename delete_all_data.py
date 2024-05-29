import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('cv_database.db')
cursor = conn.cursor()

# Supprimer toutes les expériences existantes
cursor.execute("DELETE FROM experience")
cursor.execute("DELETE FROM experience_skills")

# Supprimer toutes les formations existantes
cursor.execute("DELETE FROM education")
cursor.execute("DELETE FROM education_skills")

# Valider les modifications
conn.commit()
conn.close()
