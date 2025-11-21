import logging
import os

import requests
from InquirerPy import inquirer

from view.menu_manche import MenuManche
from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
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
                from service.joueur_service import JoueurService
                from view.menu_info_table import InfoTableMenu
                from view.menu_joueur_vue import MenuJoueurVue

                joueur = JoueurService().trouver_par_id(Session().id)
                table = joueur.table
                if table:
                    nb_joueurs = len(table.joueurs)
                    nb_max = table.joueur_max
                    pseudos = [j.pseudo for j in table.joueurs]
                    print(f"Table n°{table.numero_table}: {nb_joueurs}/{nb_max} joueurs présents")
                    print("Joueurs présents : " + ", ".join(pseudos))
                else:
                    print("Vous n'êtes connecté à aucune table.")

                return InfoTableMenu(Session().afficher(), temps_attente=3)

            case "Lancer manche":
                joueur = JoueurService().trouver_par_id(Session().id)
                logger.debug(f"{joueur.table}")
                # numero_table = joueur.table
                numero_table = joueur.table.numero_table
                # numero_table = 1
                req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")

                # return MenuManche("")

                if req.status_code == 200:
                    print("Manche lancée !")
                    return MenuManche("")
                else:
                    print("Erreur lors du lancement de la manche")
                    from view.menu_joueur_vue import MenuJoueurVue

                    return MenuJoueurVue(Session().afficher())

                """
                TableService().lancer_manche(table.numero_table)
                return GameMenu("")
                """

            case "Quitter table":  # fonctionne pas
                id_joueur = Session().id
                url = f"{host}{END_POINT}retirer/{id_joueur}"
                req = requests.put(url)

                if req.status_code == 200:
                    message = "vous avez quitté la table"
                else:
                    message = "vous n'avez pas pu quitter la table"

                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue(message)
