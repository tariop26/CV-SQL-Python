-- Création de la table education
CREATE TABLE education (
    id INTEGER PRIMARY KEY,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field_of_study TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    description TEXT
);

-- Création de la table experience
CREATE TABLE experience (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    description TEXT
);

-- Création de la table skills
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    proficiency INTEGER NOT NULL
);

-- Création de la table projects
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    description TEXT,
    technologies_used TEXT
);

-- Insertion des données dans la table education
INSERT INTO education (institution, degree, field_of_study, start_date, end_date, description)
VALUES
    ('Lycée Condorcet', 'Bac S', 'Options maths', '2002-09-01', '2002-06-30', 'Description of degree program'),
    ('Databird', 'Formation Data Analyst', 'Analyse de données', '2024-02-01', '2024-07-30', 'Description of degree program');

-- Insertion des données dans la table experience
INSERT INTO experience (company, job_title, start_date, end_date, description)
VALUES
    ('Company A', 'Software Developer', '2009-07-01', '2013-08-01', 'Description of job responsibilities'),
    ('Company B', 'Data Analyst', '2013-09-01', '2018-12-01', 'Description of job responsibilities');

-- Insertion des données dans la table skills
INSERT INTO skills (skill_name, proficiency)
VALUES
    ('Python', 5),
    ('SQL', 4),
    ('Data Analysis', 5);

-- Insertion des données dans la table projects
INSERT INTO projects (project_name, description, technologies_used)
VALUES
    ('Project A', 'Description of Project A', 'Python, SQL, Pandas'),
    ('Project B', 'Description of Project B', 'Python, Flask, SQLAlchemy');

-- Mise à jour d'une expérience professionnelle
UPDATE experience
SET job_title = 'Senior Data Analyst', end_date = '2022-12-01', description = 'Updated description of job responsibilities'
WHERE id = 2;

-- Mise à jour d'une compétence
UPDATE skills
SET proficiency = 5
WHERE skill_name = 'SQL';


