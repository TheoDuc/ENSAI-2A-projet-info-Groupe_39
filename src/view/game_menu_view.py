import logging
import os

import requests
from InquirerPy import inquirer

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

        # Rafraîchir la table depuis l’API --- LA LIGNE QUI MANQUAIT !!!
        id_table = Session().joueur.id_table
        req = requests.get(f"{host}{END_POINT}{id_table}")
        req_j = requests.get(f"{host}{END_POINT}{id_table}/joueurs")
        joueurs = req_j.json()
        for j in joueurs:
            print(f"- {j['pseudo']} : {j['credit']} crédits")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Lancer manche",
                "Quitter table",
            ],
        ).execute()

        match choix:
            case "Lancer manche":
                logger.debug(f"{Session().joueur.table}")
                # numero_table = Session().joueur.table.numero_table
                numero_table = 1
                req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")

                return GameMenu("")

                """
                TableService().lancer_manche(table.numero_table)
                return GameMenu("")
                """

            case "Quitter table":  # fonctionne pas
                pseudo = Session().joueur.pseudo
                req = requests.put(f"{host}{END_POINT}quiter/{pseudo}")

                if req.status_code == 200:
                    print("vous avez quité la table")

                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue(Session().afficher())
