import logging
import os

import requests
from InquirerPy import inquirer

from view.menu_joueur_vue import MenuJoueurVue
from view.menu_manche import MenuManche
from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Vue du menu de jeu du joueur"""

    def __init__(self, numero_table=None):
        self.numero_table = numero_table  # numéro de table courant

    def afficher_infos_table(self):
        """Affiche les informations complètes de la table"""
        id_joueur = Session().id

        # On récupère la table à partir du serveur
        res_table = requests.get(f"{host}{END_POINT}joueur/{id_joueur}")
        if res_table.status_code != 200:
            print("Impossible de récupérer la table ou vous n'êtes connecté à aucune table.")
            return

        table_info = res_table.json()
        nb_joueurs = len(table_info.get("joueurs", []))
        nb_max = table_info.get("joueur_max", 0)
        pseudos = [j["pseudo"] for j in table_info.get("joueurs", [])]

        print(f"\nTable n°{table_info['numero_table']} : {nb_joueurs}/{nb_max} joueurs présents")
        if pseudos:
            print("Joueurs présents : " + ", ".join(pseudos))
        else:
            print("Aucun joueur présent pour le moment.")

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        print("\n" + "-" * 50 + "\nMenu de jeu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Info de session",
                "Lancer manche",
                "Quitter table",
            ],
        ).execute()

        match choix:
            case "Info de session":
                self.afficher_infos_table()
                return self  # reste dans le menu de la table

            case "Lancer manche":
                # récupérer le numéro de table via l'API
                id_joueur = Session().id
                res_table = requests.get(f"{host}{END_POINT}joueur/{id_joueur}")
                if res_table.status_code != 200:
                    print("Impossible de lancer la manche : vous n'êtes connecté à aucune table.")
                    return MenuJoueurVue("Vous n'êtes connecté à aucune table")

                table_info = res_table.json()
                numero_table = table_info["numero_table"]

                req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")
                if req.status_code == 200:
                    print("Manche lancée !")
                    return MenuManche("")
                else:
                    print("Erreur lors du lancement de la manche")
                    return MenuJoueurVue("Erreur lors du lancement de la manche")

            case "Quitter table":
                id_joueur = Session().id
                url = f"{host}{END_POINT}retirer/{id_joueur}"
                req = requests.put(url)

                if req.status_code == 200:
                    message = "Vous avez quitté la table"
                else:
                    message = "Vous n'avez pas pu quitter la table"

                return MenuJoueurVue(message)
