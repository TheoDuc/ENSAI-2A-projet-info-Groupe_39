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
        try:
            reponse = requests.get(f"{host}{END_POINT}")
            boutons_tables = reponse.json()
        except ValueError:
            boutons_tables = []

        action_table += boutons_tables

        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        match choix:
            case "Retour au Menu Joueur":
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

            case "Créer une Table":
                from view.menu_creation_table import MenuCreationTable

                return MenuCreationTable()

            case _ if choix in boutons_tables:
                numero_table = int(choix.split()[1].replace(",", ""))
                id_joueur = Session().id

                req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{id_joueur}")

                match req.status_code:
                    case 200:
                        # Met à jour la session globale
                        joueur = next(
                            (j for j in Session.joueurs_connectes if j.id_joueur == id_joueur), None
                        )
                        if joueur:
                            joueur.numero_table = numero_table
                        from view.menu_info_table import InfoTableMenu

                        print(f"Vous êtes connecté sur la table {numero_table}")
                        return InfoTableMenu()
                    case _:
                        print("Erreur lors de la connexion à la table")
                        from view.menu_joueur_vue import MenuJoueurVue

                        return MenuJoueurVue()
