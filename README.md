# CV-SQL-Python
Le CV codé de Manuel Poirat
Junior certes mais débrouillard et passionné par les l'analyse de chiffres et la data-visualisation. 

## Voici la structure de mon projet

- `create_cv_database.sql`: Script pour créer une database avec mes infos personnelles et professionnelles. 
- `queries.sql`: SQL queries pour montrer un peu ce que je suis capable de faire en SQL.
- `queries.py`: Script Python pour intéragir avec la base SQL.
- `visualizations.py`: Script Python pour créer des visualisations.
- `app.py`: Web application.
- `README.md`: Ce fichier explicatif.

## Comment utiliser mon CV Codé ? 
1. Cloner le repository : 
   ```bash
   git clone https://github.com/tariop26/CV-SQL-Python
   cd CV-SQL-Python
2. Configurez l'environnement virtuel et installez les dépendances :
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
3. Exécutez le script SQL pour créer la base de données :
   sqlite3 cv_database.db < create_cv_database.sql
4. Exécutez le script Python :
   python queries.py
   python visualizations.py
5. Exécutez l'application web :
   python app.py

## Composants du projet
- Base de données SQL : Informations détaillées sur les tables, les données et les requêtes SQL utilisées. 
- Scripts Python : Comment Python est utilisé pour interagir avec la base de données SQL et créer des visualisations. 
- Application Web : Instructions sur la façon d'accéder à l'application Web et les fonctionnalités qu'elle inclut.