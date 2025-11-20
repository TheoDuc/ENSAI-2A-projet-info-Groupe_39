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
            numero_table = int(choix.split()[1].replace(",", ""))
            id_joueur = Session().id
            url = f"{host}{END_POINT}ajouter/{numero_table}/{id_joueur}"
            req = requests.put(url)

            if req.status_code == 200:
                from view.menu_info_table import InfoTableMenu

                message = f"Vous êtes connecté sur la table {numero_table}"
                return InfoTableMenu(message, 2)

            else:
                from view.menu_joueur_vue import MenuJoueurVue

                message = f"Erreur lors de la connexion à la table {numero_table}"
                return MenuJoueurVue(message)
