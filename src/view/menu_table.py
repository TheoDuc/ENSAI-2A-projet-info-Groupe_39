"""Menu des tables"""

import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def choisir_menu(self):
        action_table = ["Retour au Menu Joueur", "Créer une Table"]

        # Récupère la liste des tables depuis l'API
        try:
            reponse = requests.get(f"{host}{END_POINT}")
            reponse.raise_for_status()
            tables = reponse.json()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des tables : {e}")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        # Crée les boutons pour chaque table
        boutons_tables = [f"Table {t['numero_table']}" for t in tables]
        action_table += boutons_tables

        # Menu interactif
        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if choix == "Créer une Table":
            from view.menu_creation_table import MenuCreationTable

            return MenuCreationTable()

        if choix in boutons_tables:
            index = boutons_tables.index(choix)
            table = tables[index]
            numero_table = table["numero_table"]
            pseudo = getattr(Session().joueur, "pseudo", None)

            if not pseudo:
                print("Aucun joueur connecté.")
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

            # Requête pour rejoindre la table
            try:
                req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{pseudo}")
                req.raise_for_status()
            except requests.RequestException:
                print("La connexion à la table n'a pas fonctionné")
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

            print(f"Vous êtes connecté sur la table {numero_table}")
            from view.game_menu_view import GameMenu

            return GameMenu()
