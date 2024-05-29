-- Selection de toutes les entrées de la table education
SELECT * FROM education;

-- Utilisation de CASE WHEN pour créer une colonne indiquant si la formation est terminée
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

-- Group by pour compter le nombre d'expériences par entreprise
SELECT 
    company, 
    COUNT(*) as num_experiences
FROM experience
GROUP BY company;

-- Order by pour trier les compétences par niveau de maîtrise
SELECT 
    skill_name, 
    proficiency
FROM skills
ORDER BY proficiency DESC;

-- Utilisation de WITH pour créer une sous-requête
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

-- Utilisation de LIMIT pour limiter les résultats aux 5 compétences les plus maîtrisées
SELECT 
    skill_name, 
    proficiency
FROM skills
ORDER BY proficiency DESC
LIMIT 5;
