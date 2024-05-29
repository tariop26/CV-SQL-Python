-- Ajouter une table pour les compétences associées aux expériences
CREATE TABLE IF NOT EXISTS experience_skills (
    experience_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY (experience_id) REFERENCES experience(id),
    FOREIGN KEY (skill_name) REFERENCES skills(skill_name)
);

-- Ajouter une table pour les compétences associées aux formations
CREATE TABLE IF NOT EXISTS education_skills (
    education_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY (education_id) REFERENCES education(id),
    FOREIGN KEY (skill_name) REFERENCES skills(skill_name)
);