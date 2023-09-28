# Projet12: Développez une architecture back-end sécurisée en utilisant Django ORM

[![Generic badge](https://img.shields.io/badge/MADE_WITH-PYTHON-orange.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/MADE_WITH-Django_REST_Framework-blue.svg)](https://www.django-rest-framework.org/)   

[![Generic badge](https://img.shields.io/badge/APPROVED_BY-AURELIE_BERNICHE-blueviolet.svg)](https://github.com/BernicheAurelie/)
[![Generic badge](https://img.shields.io/badge/FOR-Epic-Events-green.svg)](https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png)

## Introduction

Ce projet a été réalisé pour la société Epic Events qui souhaitait développer un logiciel de gestion de la relation client (CRM) en interne, suite à une fuite de données chez le précédent fournisseur. Cette société reputée pour l'organisation de fêtes et événements hors du commun avait besoin d'un logiciel sécurisé pour garantir l'intégrité des données.

Les utilisateurs sont regroupés en trois groupes limitant l'accessibilité à la base de données en fonction des besoins de chaque groupe.

L'équipe de gestion:
    - ajoute et gère les utilisateurs.
    - a accès en lecture et modification a toutes les données du CRM.

L'équipe de vente:
    - ajoute des clients.
    - ajoute des contrats et des événements aux clients dont ils sont responsables.
    - a accès en lecture seule aux clients, contrats et événements.
    - ne peut modifier que les clients dont ils sont responsables.
    - ne peut modifier que les contrats des clients dont ils sont responsables.
    - ne peut pas modifier les événements.

L'équipe support
    - a accès en lecture seule aux clients, contrats et événements.
    - ne peut pas modifier que les événements dont ils sont responsables.

L'application est sécurisée:
  - Tout utilisateur doit être authentifié
  - Les permissions CRUD sont définies en fonction des utilisateurs pour limiter l'accès à la base de données.
  - L'accès aux utilisateurs est limitée à l'administration et à l'équipe de gestion.

### Pré-requis

- Editeur de texte [Download VS Code](https://code.visualstudio.com/) 
- Langage de programmation [Download Python](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com/) - Framework Python

### Installation
- Avec pipenv:   
Installation: ```pip install pipenv```   
Installation des dépendances: ```pipenv install```    
Activation de l'environnement virtuel: ```pipenv shell```   

- Avec pip, sans pipenv:   
Création de l'environnement virtuel: ``` python -m venv env ```   
Activation: ```venv\Scripts\activate```   
Installation des packages nécessaires: ```pip install -r requirements.txt```   


## Démarrage
Lancement de l'application: ```python manage.py runserver```   
Lancement direct avec pipenv: ```pipenv run python manage.py runserver```    
Suivre la documentation Postman pour utiliser au mieux les points de terminaison de l'API.
[Documentation PostMan](https://documenter.getpostman.com/view/18483073/2s9Xy5LVaQ)


## Réalisé avec 
- [Visual Studio Code](https://code.visualstudio.com/) - Editeur de textes
- [Django](https://www.djangoproject.com/) - Web Framework de Python
- [Django REST framework](https://www.django-rest-framework.org/) - Outil de développement d'API de Django
