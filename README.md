# ENSAI 2A - Poker Server Project (Group 39)

This project is a **Python-based poker server** organized with a **layered architecture**. It includes both a **command-line interface (CLI)** for interactive play and a **webservice** for programmatic access.

It was developed as part of a **2nd-year ENSAI project** and demonstrates all the key elements of a professional application, including:


- **Layered architecture**: DAO, Service, Business Object, View
- **PostgreSQL database** connection
- CLI interface with InquirerPy
- Webservice creation and consumption using **FastAPI**
- Logging with decorator and configuration file
- Unit tests and test coverage
- **CI/CD pipeline** via GitHub Actions


## :arrow_forward: Software and tools

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [InquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
- [pytest](https://docs.pytest.org/)
- [Coverage](https://coverage.readthedocs.io/)


## :arrow_forward: Clone the repository

- [ ] Open VSCode
- [ ] Open **Git Bash**
- [ ] Clone the repo
  - `git clone https://github.com/TheoDuc/ENSAI-2A-projet-info-Groupe_39`


### Open the Project Folder

- [ ] Launch **Visual Studio Code**
- [ ] Go to `File > Open Folder`
- [ ] Select the folder `ENSAI-2A-projet-info-Groupe_39`
  - This folder should be the **root** of your VSCode Explorer.
  - :warning: If it is not, the application may not start. In that case, try opening the folder again.


## Repository Files Overview

| File / Item                | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| `README.md`                | Contains all the information needed to understand, install, and use the project |
| `LICENSE`                  | Defines the usage rights and licensing terms for this repository             |

### Configuration Files

This project includes several configuration files used to set up tools, workflows, and project parameters.  

In most cases, **you do not need to modify these files**, except for:

- `.env` → to configure environment variables like database connection and webservice host  
- `requirements.txt` → to manage Python dependencies

| File / Item                  | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| `.github/workflows/ci.yml`   | GitHub Actions workflow for automated tasks such as testing, linting, and deployment |
| `.vscode/settings.json`      | Project-specific Visual Studio Code settings                                 |
| `.coveragerc`                | Configuration for test coverage reporting                                    |
| `.gitignore`                 | Lists files and folders to exclude from version control                     |
| `logging_config.yml`         | Configuration for logging, including log levels and formatting              |
| `requirements.txt`           | List of Python packages required by the project                             |
| `.env`                       | Environment variables for database, webservice, and other settings          |

> :information_source: Make sure to create and configure the `.env` file as described below before running the project.

### Project Folders

| Folder  | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `data/`       | SQL scripts to initialize and populate the database                         |
| `doc/`        | UML diagrams, design documents, and project-related documentation          |
| `logs/`       | Log files generated during application or webservice execution             |
| `src/`        | Python source code organized in a layered architecture (DAO, Service, BO, View) |



### Settings Files

This project includes several configuration files used to set up tools, workflows, and project parameters.  

In most cases, **you do not need to modify these files**, except for:

- `.env` → to configure environment variables such as database connection and webservice host  
- `requirements.txt` → to manage Python dependencies



## :arrow_forward: Install Required Packages

- [ ] Open Git Bash (or your terminal) and run the following commands to install all necessary packages and check the installed packages:

```bash
# Install packages from requirements.txt
pip install -r requirements.txt

# List installed packages
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


### TU DAO

To ensure tests are repeatable, safe, and **do not interfere with the real database**, we use a dedicated schema for unit testing.

The DAO unit tests use data from the `data/pop_db_test.sql` file.

This data is loaded into a separate schema (projet_test_dao) so as not to pollute the other data.


### Test coverage

It is also possible to generate test coverage using [Coverage](https://coverage.readthedocs.io/en/7.4.0/index.html)

:bulb: The `.coveragerc` file can be used to modify the settings

- [ ] `coverage run -m pytest`
- [ ] `coverage report -m`
- [ ] `coverage html`
  - Download and open coverage_report/index.html



## :arrow_forward: Launch the CLI application

This application provides a very basic graphical interface for navigating between different menus.

- [ ] In Git Bash: `python src/main.py`
- [ ] On first launch, choose **Reset database**
  - this calls the `src/utils/reset_database.py` program
  - which will itself execute the SQL scripts in the `data` folder



## :arrow_forward: Launch the webservice

This application can also be used to create a webservice.

- [ ] `python src/app.py`

Documentation :

- /docs
- /redoc

### Endpoints

Examples of endpoints (to be tested, for example, with *Insomnia* or a browser):


- `GET http://localhost/joueur`
- `GET http://localhost/joueur/3`
- ```
  POST http://localhost/joueur/
  JSON body :
    {
      "pseudo": "patapouf",
      "mdp": "9999",
      "age": "95",
      "mail": "patapouf@mail.fr",
      "fan_pokemon": true
    }
  ```
- ```
  PUT http://localhost/joueur/3
  JSON body :
    {
       "pseudo": "maurice_new",
       "mdp": null,
       "age": 20,
       "mail": "maurice@ensai.fr",
       "fan_pokemon": true
    }
  ```
- `DELETE http://localhost/joueur/5`



## :arrow_forward: Logs

It is initialised in the `src/utils/log_init.py` module:

- This is called when the application or webservice is started.
- It uses the `logging_config.yml` file for configuration.
  - to change the log level :arrow_right: *level* tag

A decorator has been created in `src/utils/log_decorator.py`.

When applied to a method, it will display in the logs :

- input parameters
- the output

The logs can be viewed in the `logs` folder.

Example of logs :

```
07/08/2024 09:07:07 - INFO     - ConnexionVue
07/08/2024 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - DEBUT
07/08/2024 09:07:08 - INFO     -         JoueurDao.se_connecter('a', '*****') - DEBUT
07/08/2024 09:07:08 - INFO     -         JoueurDao.se_connecter('a', '*****') - FIN
07/08/2024 09:07:08 - INFO     -            └─> Sortie : Joueur(a, 20 ans)
07/08/2024 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - FIN
07/08/2024 09:07:08 - INFO     -        └─> Sortie : Joueur(a, 20 ans)
07/08/2024 09:07:08 - INFO     - MenuJoueurVue
```



## :arrow_forward: Continuous integration (CI)

The repository contains a `.github/workflow/main.yml' file.

When you *push* on GitHub, it triggers a pipeline that will perform the following steps:

- Creating a container from an Ubuntu (Linux) image
  - In other words, it creates a virtual machine with just a Linux kernel.
- Install Python
- Install the required packages
- Run the unit tests (only the service tests, as it's more complicated to run the dao tests)
- Analyse the code with *pylint*
  - If the score is less than 7.5, the step will fail

You can check how this pipeline is progressing on your repository's GitHub page, *Actions* tab.