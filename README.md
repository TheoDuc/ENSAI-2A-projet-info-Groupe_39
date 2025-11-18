# ENSAI 2A - Projet Serveur Poker (Groupe 39)

Ce projet est un **serveur poker basé sur Python** organisé avec une **architecture en couches**. Il inclut à la fois une **interface en ligne de commande (CLI)** pour jouer interactivement et un **webservice** pour un accès programmatique.

Il a été développé dans le cadre d'un **projet de 2ème année à l'ENSAI** et démontre tous les éléments clés d'une application professionnelle, incluant :

- **Architecture en couches** : DAO, Service, Objet Métier, Vue
- Connexion à une base de données **PostgreSQL**
- Interface CLI avec InquirerPy
- Création et consommation de webservice utilisant **FastAPI**
- Journalisation (logging) avec décorateur et fichier de configuration
- Tests unitaires et couverture de code
- Pipeline **CI/CD** via GitHub Actions

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

- [ ] Ouvrir Git Bash (ou votre terminal) et exécuter les commandes suivantes pour installer tous les packages nécessaires et vérifier les packages installés :

```bash
# Installer les packages depuis requirements.txt
pip install -r requirements.txt

# Lister les packages installés
pip list

```
## :arrow_forward: Environment Variables

You need to define environment variables to configure the database and webservice that your Python application will connect to.

At the root of the project:

- [ ] Create a file named `.env`
- [ ] Copy and fill in the following variables:

```env
# Webservice host
WEBSERVICE_HOST= à completer

# PostgreSQL database configuration
POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet

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
