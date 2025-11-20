import logging
import os

import requests
from InquirerPy import inquirer

from service.joueur_service import JoueurService
from view.menu_manche import MenuManche
from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class GameMenu(VueAbstraite):
    """Vue du menu de jeu du joueur"""

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

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
                return GameMenu(Session().afficher(), temps_attente=3)

            case "Lancer manche":
                joueur = JoueurService().trouver_par_id(Session().id)
                logger.debug(f"{joueur.table}")
                numero_table = joueur.table
                # numero_table = 1
                req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")

                return MenuManche("")

                """
                TableService().lancer_manche(table.numero_table)
                return GameMenu("")
                """

            case "Quitter table":  # fonctionne pas
                joueur = JoueurService().trouver_par_id(Session().id)
                pseudo = joueur.pseudo
                req = requests.put(f"{host}{END_POINT}quiter/{pseudo}")

                if req.status_code == 200:
                    print("vous avez quité la table")

                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue(Session().afficher())
