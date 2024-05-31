# CV-SQL-Python
Le CV codé de Manuel Poirat
Junior certes mais débrouillard et passionné par les l'analyse de chiffres et la data-visualisation. 
Ce projet est une application web développée avec Streamlit pour afficher un CV interactif. Il utilise une base de données SQLite pour stocker les données et propose diverses visualisations pour présenter les compétences et les expériences professionnelles.

## Composants du projet
- Base de données SQL : Informations détaillées sur les tables, les données et les requêtes SQL utilisées. 
- Scripts Python : Comment Python est utilisé pour interagir avec la base de données SQL et créer des visualisations. 
- Application Web : Instructions sur la façon d'accéder à l'application Web et les fonctionnalités qu'elle inclut.

## Structure de mon projet
- - `app.py` : Le script principal de l'application Streamlit. Il contient le code qui génère l'interface utilisateur et les visualisations.
- `requirements.txt` : Le fichier listant toutes les dépendances nécessaires pour exécuter votre application. Il permet d'installer toutes les bibliothèques requises avec `pip install -r requirements.txt`.
- `cv_database.db` : La base de données SQLite contenant les informations utilisées par votre application.
- `initialize_db.py` : Le script pour initialiser la base de données.
- `insert_data.py` : Le script pour insérer les données dans la base de données.
- `queries.py` : Le script contenant des fonctions de requêtes SQL.
- `queries.sql` : Le fichier contenant les requêtes SQL utilisées pour interroger la base de données.
- `.gitignore` : Utilisé pour exclure certains fichiers du contrôle de version. Gardez-le si vous avez des fichiers à exclure.
- `.streamlit` : Dossier pour la configuration de Streamlit (ex : configuration de la mise en page, des thèmes, etc.).
- `README.md` : Ce fichier explicatif.

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
