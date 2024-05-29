-- Create the education table
CREATE TABLE education (
    id INTEGER PRIMARY KEY,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field_of_study TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    description TEXT
);

-- Create the experience table
CREATE TABLE experience (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL,
    job_title TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    description TEXT
);

-- Create the skills table
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    proficiency INTEGER NOT NULL
);

-- Create the projects table
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    description TEXT,
    technologies_used TEXT
);

-- Insert sample data into the education table
INSERT INTO education (institution, degree, field_of_study, start_date, end_date, description)
VALUES
    ('University A', 'Bachelor of Science', 'Computer Science', '2002-09-01', '2006-06-01', 'Description of degree program'),
    ('University B', 'Master of Science', 'Data Science', '2007-09-01', '2009-06-01', 'Description of degree program');

-- Insert sample data into the experience table
INSERT INTO experience (company, job_title, start_date, end_date, description)
VALUES
    ('Company A', 'Software Developer', '2009-07-01', '2013-08-01', 'Description of job responsibilities'),
    ('Company B', 'Data Analyst', '2013-09-01', '2018-12-01', 'Description of job responsibilities');

-- Insert sample data into the skills table
INSERT INTO skills (skill_name, proficiency)
VALUES
    ('Python', 5),
    ('SQL', 4),
    ('Data Analysis', 5);

-- Insert sample data into the projects table
INSERT INTO projects (project_name, description, technologies_used)
VALUES
    ('Project A', 'Description of Project A', 'Python, SQL, Pandas'),
    ('Project B', 'Description of Project B', 'Python, Flask, SQLAlchemy');
