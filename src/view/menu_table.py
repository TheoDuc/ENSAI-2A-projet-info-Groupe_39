"""Menu des tables"""

import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"

logger = logging.getLogger(__name__)


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def __init__(self, table_info=None):
        self.table_info = table_info  # dictionnaire avec les infos de la table

    def afficher_infos_table(self):
        if not self.table_info:
            print("Impossible de récupérer les infos de la table.")
            return

        nb_joueurs = len(self.table_info.get("joueurs", []))
        nb_max = self.table_info.get("joueur_max", 0)
        pseudos = [j["pseudo"] for j in self.table_info.get("joueurs", [])]

        print(f"Table n°{self.table_info['numero_table']}: {nb_joueurs}/{nb_max} joueurs présents")
        if pseudos:
            print("Joueurs présents : " + ", ".join(pseudos))
        else:
            print("Aucun joueur présent pour le moment.")

    def choisir_menu(self):
        self.afficher_infos_table()
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
            numero_table = int(choix.split()[1].replace(",", ""))

            # L'identifiant provient de Session(), donc c'est TOUJOURS un ID numérique
            id_joueur = Session().id

            # On appelle ta route actuelle
            req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{id_joueur}")

            if req.status_code == 200:
                res_table = requests.get(f"{host}{END_POINT}{numero_table}")
                table_info = res_table.json() if res_table.status_code == 200 else None
                from view.menu_info_table import InfoTableMenu

                print(f"Vous êtes connecté sur la table {numero_table}")
                return InfoTableMenu(table_info)

            else:
                print("Erreur lors de la connexion à la table")
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()
