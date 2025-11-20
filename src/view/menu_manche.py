import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/action/"


class MenuManche(VueAbstraite):
    """Vue du menu d'une manche"""

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
                "Voir les infos de la manche",
                "Regarder main",
                "Checker",
                "Suivre",
                "All in",
                "Se coucher",
                "Quitter manche",
            ],
        ).execute()

        id_joueur = Session().id
        req_joueur = requests.get(f"{host}/joueur/id/{id_joueur}")
        if req_joueur.status_code != 200:
            print("Erreur : impossible de récupérer les infos du joueur.")
            return self
        joueur_data = req_joueur.json()
        numero_table = joueur_data["table"]["numero_table"]
        pseudo = joueur_data["pseudo"]

        match choix:
            case "Voir les infos de la manche":
                req = requests.get(f"{host}/table/affichage/{numero_table}")
                # numero_table = 1
                # joueur = JoueurService().trouver_par_id(Session().id)
                # numero_table = joueur.table.numero_table
                # req = requests.get(f"{host}/table/affichage/{numero_table}")
                if req.status_code == 200:
                    print(req.text)
                return MenuManche()

            case "Regarder main":
                # numero_table = 1
                # joueur = JoueurService().trouver_par_id(Session().id)
                # id_joueur =  Session().id
                # numero_table = joueur.table.numero_table
                req = requests.get(f"{host}/table/main/{numero_table}/{id_joueur}")
                if req.status_code == 200:
                    print(req.text)
                return MenuManche()

            case "Checker":
                # joueur = JoueurService().trouver_par_id(Session().id)
                # pseudo = joueur.pseudo
                req = requests.put(f"{host}{END_POINT}checker/{pseudo}")
                return MenuManche()

            case "Suivre":
                # joueur = JoueurService().trouver_par_id(Session().id)
                # pseudo = joueur.pseudo
                req = requests.put(f"{host}{END_POINT}suivre/{pseudo}")
                return MenuManche()

            case "All in":
                # joueur = JoueurService().trouver_par_id(Session().id)
                # pseudo = joueur.pseudo
                req = requests.put(f"{host}{END_POINT}all_in/{pseudo}")
                return MenuManche()

            case "Se coucher":
                # joueur = JoueurService().trouver_par_id(Session().id)
                # pseudo = joueur.pseudo
                req = requests.put(f"{host}{END_POINT}se_coucher/{pseudo}")
                return MenuManche()

            case "Quitter manche":
                # joueur = JoueurService().trouver_par_id(Session().id)
                # numero_table = joueur.table.numero_table
                # numero_table = 1
                req = requests.get(f"{host}/table/terminer/{numero_table}")

                if req.status_code == 200:
                    print("vous avez quité la manche")

                from view.game_menu_view import GameMenu

                return GameMenu(Session().afficher())
