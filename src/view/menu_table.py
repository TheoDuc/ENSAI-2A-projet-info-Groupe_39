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
        reponse = requests.get(f"{host}{END_POINT}")
        boutons_tables = reponse.json()
        action_table += boutons_tables

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
            numero_table = int(choix[6])
            pseudo = Session().joueur.pseudo

            req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{pseudo}")
            if req.status_code != 200:
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()
            table_req = requests.get(f"{host}{END_POINT}{numero_table}")
            table_data = table_req.json()
            if numero_table not in Session.tables_globales:
                from business_object.joueur import Joueur
                from business_object.table import Table

                Session.tables_globales[numero_table] = Table(
                    numero_table=table_data["numero_table"],
                    grosse_blind=table_data["grosse_blind"],
                    joueurs=[
                        Joueur(j["id_joueur"], j["pseudo"], j["credit"], j["pays"])
                        for j in table_data["joueurs"]
                    ],
                )
            Session().joueur.table = Session.tables_globales[numero_table]

            if req.status_code != 200:
                print("La connexion à la table n'a pas fonctionné")
                return MenuJoueurVue()
            from view.game_menu_view import GameMenu

            print(f"Vous etes connecté sur la table {numero_table}")
            return GameMenu()
