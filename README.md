# Bot Discord pour la gestion de serveur

![Badge de version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Licence](https://img.shields.io/badge/licence-MIT-green.svg)

Une brève description de votre bot Discord et de ses fonctionnalités.

## Table des matières

- [Description](#description)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Dépendances](#dépendances)
- [Utilisation](#utilisation)
- [Licence](#licence)

## Description

Ce bot Discord est conçu pour faciliter la gestion de serveur en automatisant diverses tâches telles que la modération, l'accueil des nouveaux membres et la gestion des rôles. Il offre une interface conviviale et des commandes personnalisables pour s'adapter aux besoins spécifiques de votre communauté.

## Prérequis

Avant d'installer le bot, assurez-vous d'avoir les éléments suivants :

- [Python](https://www.python.org/) version 3.8 ou supérieure
- [Pip](https://pip.pypa.io/en/stable/) pour la gestion des packages Python
- Un compte Discord et un serveur où vous avez les droits d'administration

## Installation

1. **Clonez le repository :**

   ```bash
   git clone https://github.com/7Sonny/Bot-discord.git
   cd Bot-discord
   
Créez un environnement virtuel :
python3 -m venv env

Activez l'environnement virtuel :
Sur Windows :
env\Scripts\activate

Sur macOS/Linux :
source env/bin/activate

Installez les dépendances :
pip install -r requirements.txt

Configurez le bot :
Renommez le fichier config_example.py en config.py.
Ouvrez config.py et remplissez les champs requis, notamment votre token Discord et les paramètres de préfixe de commande.
Invitez le bot sur votre serveur :
Accédez au portail des développeurs Discord.
Sélectionnez votre application, puis générez une URL d'invitation avec les autorisations appropriées.
Utilisez cette URL pour inviter le bot sur votre serveur.

Dépendances : 

Le bot utilise les bibliothèques suivantes :

aiohappyeyeballs 2.4.4
aiohttp 3.11.11
aiosignal 1.3.2
anyio 4.8.0
async-timeout 5.0.1
attrs 25.1.0
beautifulsoup4 4.13.3
blinker 1.9.0
certifi 2025.1.31
charset-normalizer 3.4.1
click 8.1.8
deep-translator 1.11.4
discord.py 2.4.0
exceptiongroup 1.2.2
Flask 3.1.0
frozenlist 1.5.0
googletrans 4.0.2
h11 0.14.0
h2 4.2.0
hpack 4.1.0
httpcore 1.0.7
httpx 0.28.1
hyperframe 6.1.0
idna 3.10
importlib_metadata 8.6.1
itsdangerous 2.2.0
Jinja2 3.1.5
MarkupSafe 3.0.2
multidict 6.1.0
mysql-connector-python 9.2.0
pip 23.2.1
praw 7.8.1
prawcore 2.4.0
propcache 0.2.1
python-dotenv 1.0.1
requests 2.32.3
setuptools 68.2.0
sniffio 1.3.1
soupsieve 2.6
typing_extensions 4.12.2
update-checker 0.18.0
urllib3 2.3.0
websocket-client 1.8.0
Werkzeug 3.1.3
wheel 0.41.2
wikipedia 1.4.0
yarl 1.18.3
zipp 3.21.0
Utilisation

Une fois le bot installé et en ligne :

Utilisez le préfixe défini (par défaut !) suivi de la commande souhaitée. Par exemple :
!aide : Affiche la liste des commandes disponibles.
!accueil : Envoie un message de bienvenue aux nouveaux membres.
Pour plus de commandes et de fonctionnalités, consultez la documentation complète ou utilisez !aide dans Discord.

Licence :

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
