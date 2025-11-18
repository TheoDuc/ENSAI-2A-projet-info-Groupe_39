# 🎲 ENSAI 2A — Projet Serveur Poker (Groupe 39)

Ce projet a pour objectif de créer un **serveur de poker fonctionnel**, capable de gérer des tables et de faire jouer des parties de **Texas Hold’em**.  
Les joueurs peuvent interagir avec le serveur via des requêtes **HTTP**, tandis que toutes les données importantes sont sauvegardées dans une base de données **PostgreSQL**.

L’application a été conçue pour être **modulaire et professionnelle**, grâce à une **architecture en couches** qui sépare clairement la logique métier, l’accès aux données et les interfaces utilisateur.  
Cette organisation facilite non seulement la maintenance et l’évolution du serveur, mais permet également d’intégrer facilement des fonctionnalités supplémentaires, comme un CLI interactif et  un webservice accessible à distance. Le projet propose :

- **Architecture en couches** : DAO, Service, Objet Métier, Vue
- Connexion à une base de données **PostgreSQL**
- Interface CLI avec InquirerPy
- Création et consommation de webservice utilisant **FastAPI**
- Journalisation (logging) avec décorateur et fichier de configuration
- Tests unitaires et couverture de code

## :arrow_forward: Logiciels et outils

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [InquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
- [pytest](https://docs.pytest.org/)
- [Coverage](https://coverage.readthedocs.io/)

## :arrow_forward: Cloner le dépôt

- [ ] Ouvrir VSCode
- [ ] Ouvrir **Git Bash**
- [ ] Cloner le dépôt
  - `git clone https://github.com/TheoDuc/ENSAI-2A-projet-info-Groupe_39`

### Ouvrir le dossier du projet

- [ ] Lancer **Visual Studio Code**
- [ ] Aller dans `Fichier > Ouvrir un dossier`
- [ ] Sélectionner le dossier `ENSAI-2A-projet-info-Groupe_39`
  - Ce dossier devrait être la **racine** de l'Explorateur VSCode.
  - :warning: Si ce n'est pas le cas, l'application risque de ne pas démarrer. Dans ce cas, essayez de rouvrir le dossier.

## Aperçu des fichiers du dépôt

| Fichier / Élément          | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| `README.md`                | Contient toutes les informations nécessaires pour comprendre, installer et utiliser le projet |
| `LICENSE`                  | Définit les droits d'usage et les termes de licence pour ce dépôt           |

### Fichiers de configuration

Ce projet inclut plusieurs fichiers de configuration utilisés pour configurer les outils, workflows et paramètres du projet.

Dans la plupart des cas, **vous n'avez pas besoin de modifier ces fichiers**, sauf :

- `.env` → pour configurer les variables d'environnement comme la connexion à la base de données et l'hôte du webservice
- `requirements.txt` → pour gérer les dépendances Python

| Fichier                   | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| `.github/workflows/ci.yml`   | Workflow GitHub Actions pour les tâches automatisées comme les tests, le linting et le déploiement |
| `.vscode/settings.json`      | Paramètres spécifiques au projet pour Visual Studio Code                    |
| `.coveragerc`                | Configuration pour le rapport de couverture de tests                        |
| `.gitignore`                 | Liste les fichiers et dossiers à exclure du contrôle de version             |
| `logging_config.yml`         | Configuration pour la journalisation, incluant les niveaux de log et le formatage |
| `requirements.txt`           | Liste des packages Python requis par le projet                              |
| `.env`                       | Variables d'environnement pour la base de données, le webservice et autres paramètres |

> :information_source: Assurez-vous de créer et configurer le fichier `.env` comme décrit ci-dessous avant d'exécuter le projet.

### Dossiers du projet

| Dossier | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `data/`       | Scripts SQL pour initialiser et peupler la base de données                  |
| `doc/`        | Diagrammes UML, documents de conception et documentation liée au projet    |
| `logs/`       | Fichiers de log générés pendant l'exécution de l'application ou du webservice |
| `src/`        | Code source Python organisé en architecture en couches (DAO, Service, BO, View) |

### Fichiers de paramètres

Ce projet inclut plusieurs fichiers de configuration utilisés pour configurer les outils, workflows et paramètres du projet.

Dans la plupart des cas, **vous n'avez pas besoin de modifier ces fichiers**, sauf :

- `.env` → pour configurer les variables d'environnement comme la connexion à la base de données et l'hôte du webservice
- `requirements.txt` → pour gérer les dépendances Python

## :arrow_forward: Installer les packages requis

Pour que le projet fonctionne correctement, vous devez installer toutes les dépendances Python nécessaires.

### Étapes

1. Ouvrez votre terminal (Git Bash, PowerShell, ou autre).
2. Installez les packages listés dans `requirements.txt` :

```bash
pip install -r requirements.txt
```
3. Vérifiez que les packages ont bien été installés
```bash
pip list

```
## :arrow_forward: Variables d'environnement

Pour que votre application Python fonctionne correctement, vous devez définir certaines **variables d’environnement** afin de configurer la connexion à la base de données et au webservice.

### Étapes

1. À la racine du projet, créez un fichier nommé `.env`.
2. Copiez-y les variables suivantes et complétez-les avec vos informations :

```env
# Adresse du webservice
WEBSERVICE_HOST=https://user-cheikna-966547-user.user.lab.sspcloud.fr/docs#/

# Configuration de la base de données PostgreSQL
POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
HOST_WEBSERVICE=https://xxx.fr
```
## :arrow_forward: Unit Tests

- [ ] Open Git Bash (or your terminal) and run the unit tests:

```bash
# Standard command
pytest -v

# If pytest is not in your PATH
python -m pytest -v
```


### DAO Unit Tests

To ensure that tests are **repeatable, safe, and do not affect the real database**, we use a dedicated schema for unit testing.

- The DAO tests use sample data from `data/pop_db_test.sql`.
- This data is loaded into a separate schema named `projet_test_dao` to prevent any impact on the main database.



### Test Coverage

You can generate test coverage reports using Coverage

- [ ] Run tests with coverage:

```bash
coverage run -m pytest
```
- [ ] Display a coverage report in the terminal:

```bash
coverage report -m
```
- [ ] Generate an HTML coverage report:

```bash
coverage html
```
- [ ] Open `coverage_report/index.html` in your browser to view the results.


## :arrow_forward: Launch the CLI Application

The CLI provides a simple interactive interface to navigate through the different menus of the poker application.

- [ ] Open Git Bash (or your terminal) and run:

```bash
python src/main.py
```
- [ ] On the first launch, select **Reset database**:
  - This will run the script `src/utils/reset_database.py`.
  - The script will execute the SQL files in the `data/` folder to initialize the database.




## :arrow_forward: Launch the webservice


### Endpoints

Examples of endpoints (to be tested, for example, with *Insomnia* or a browser):



## :arrow_forward: Logs

Logging is initialized in the `src/utils/log_init.py` module:

- This setup runs whenever the CLI application or webservice is started.
- It uses the `logging_config.yml` file for configuration.
  - To change the log level, modify the `level` tag in the configuration file.

A decorator is available in `src/utils/log_decorator.py`.

- When applied to a method, it automatically logs:
  - The input parameters
  - The output of the method

All logs are saved in the `logs/` folder for review.

Example of logs :





## :arrow_forward: Continuous Integration (CI)

This repository includes a CI workflow defined in `.github/workflows/main.yml`.

Whenever you *push* changes to GitHub, it triggers a pipeline that performs the following steps:

- Creates a container based on an Ubuntu (Linux) image
  - Essentially, this sets up a virtual machine with only the Linux kernel.
- Installs Python
- Installs the required packages
- Runs the unit tests (only service tests, as DAO tests are more complex to run)
- Analyzes the code using *pylint*
  - If the pylint score is below 7.5, the step will fail

You can monitor the pipeline's progress on your repository's GitHub page under the *Actions* tab.
