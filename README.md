# TrelloProjetUEWeb

## Présentation

Trello est un outil de gestion de projet en ligne inspiré par la méthode Kanban de Toyota. 
Il repose sur une organisation des projets en planches listant des cartes, chacune représentant des tâches.

Dans le cadre de l'UE WEB de la TAF DCL à IMT Atlantique,
notre mission est de créer un site similaire à Trello avec des fonctionnalités équivalentes. 

## Avancement

|  Status   | Objet                  | Info                                               | 
|:---------:|------------------------|----------------------------------------------------|
|    ✔️     | Flask-Login            | -                                                  |
|    ✔️     | Flask-SqlAlchemy       | -                                                  |
|    ✔️     | Login / Register pages | -                                                  |
|     ❌     | Account features       | Récupération MDP, changement MDP, changement ID... | 
|    ✔️     | Rôles                  | Developer / Manager                                |
|    ✔️     | Gestion projets        | Création, modification                             |
|    ✔️     | Gestion tâches         | Création, modification                             |
|     ⌛     | Suivi de progression   | Projet et tâches                                   |
|     ⌛     | Vue tâches             |                                                    |
|     ⌛     | Commentaires tâches    |                                                    |
|     ⌛     | Tableau de bord        | Avec ordre de priorité                             |
|    ✔️     | Notifications          | En temps réel                                      |
|    ✔️     | README                 |                                                    |


## Installer

*Note : Il est fortement conseillé d'utiliser un environnement d'exécution CONDA*

Pour récupérer le projet, suivre les instructions suivantes :

```bash
$ # Clone the sources
$ git clone https://github.com/Loyceman/TrelloProjetUEWeb.git
$ cd TrelloProjetUEWeb
$
$ # Install requirements
$ pip3 install -r requirements.txt
```

## Exécuter

- Choisir un environnement d'éxécution CONDA
- Lancer app.py
- Ouvrir son navigateur et se rendre à l'URL : http://127.0.0.1:5000

# Structure

```
< PROJECT ROOT >
   |
   |-- database/
   |    |
   |    |-- database.py                 # Gestion de la base de données
   |    |-- mock_data.yaml              # Pour remplir la db à l'init
   |    |-- models.py                      
   |
   |-- static/                     # Fichiers CSS, JS, et médias
   |   
   |   |-- css/
   |   |   |
   |   |   |-- header.css
   |   |   |-- home.css
   |   |   |-- login.css
   |   |   |-- sidebar.css
   |   |   |-- styles.css
   |   |
   |   |-- img/                    # All the images and icons
   |   |
   |   |
   |   |-- js/
   |   |   |
   |   |   |-- header.js
   |   |   |-- home_page.js
   |   |   |-- project_pages.js
   |
   |-- templates/                  # Mises en page
   |    |
   |    |-- base.html.jinja2                    
   |    |-- database.html.jinja2 
   |    |-- header.html.jinja2 
   |    |-- home_page.html.jinja2 
   |    |-- index.html.jinja2 
   |    |-- login.html.jinja2 
   |    |-- logout.html.jinja2 
   |    |-- project_header.html.jinja2 
   |    |-- project_standard_view.html.jinja2 
   |    |-- register.html.jinja2 
   |
   |-- app.py                      # Coeur de l'application
   |-- helpers.py
   |-- requirements.txt
   |
   |-- ************************************************************************
```
