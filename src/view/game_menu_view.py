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
        """Choix du menu suivant de l'utilisateur"""
        print("\n" + "-" * 50 + "\nMenu de jeu Joueur\n" + "-" * 50 + "\n")

        # Vérifie que le joueur est connecté à une table
        id_table = getattr(Session().joueur, "id_table", None)
        if not id_table:
            print("Vous n'êtes connecté à aucune table.")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        # Récupère la table et les joueurs via l'API
        req_table = requests.get(f"{host}{END_POINT}{id_table}")
        if req_table.status_code != 200:
            print("Impossible de récupérer la table.")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        req_joueurs = requests.get(f"{host}{END_POINT}{id_table}/joueurs")
        joueurs = req_joueurs.json() if req_joueurs.status_code == 200 else []

        print(f"Joueurs présents à la table {id_table}:")
        if joueurs:
            for j in joueurs:
                print(f"- {j['pseudo']} : {j['credit']} crédits")
        else:
            print("Aucun joueur trouvé pour le moment.")

        # Menu principal du jeu
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Lancer manche",
                "Quitter table",
            ],
        ).execute()

        match choix:
            case "Lancer manche":
                resp = requests.get(f"{host}{END_POINT}lancer/{id_table}")
                if resp.status_code != 200:
                    print("Impossible de lancer la manche.")
                    from view.menu_joueur_vue import MenuJoueurVue

                    return MenuJoueurVue()
                else:
                    print("Manche lancée avec succès.")

                from view.menu_manche import MenuManche

                return MenuManche(id_table)

            case "Quitter table":
                pseudo = Session().joueur.pseudo
                req = requests.put(f"{host}{END_POINT}quiter/{pseudo}")
                if req.status_code == 200:
                    print("Vous avez quitté la table.")
                    # Mettre à jour la session pour refléter le départ
                    Session().joueur.id_table = None
                else:
                    print("Erreur lors de la déconnexion de la table.")

                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()
