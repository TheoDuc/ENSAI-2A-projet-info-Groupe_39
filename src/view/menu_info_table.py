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
                from view.menu_joueur_vue import MenuJoueurVue

                session = Session()

                if not session.id:
                    print("Aucun joueur connecté")
                    return MenuJoueurVue()

                # Récupérer les infos du joueur connecté via l'API
                joueur_req = requests.get(f"{host}/joueur/id/{session.id}")
                if joueur_req.status_code != 200:
                    print("Impossible de récupérer les infos du joueur")
                    return MenuJoueurVue()

                joueur_info = joueur_req.json()
                table_numero = joueur_info.get("table")
                if not table_numero:
                    print("Vous n'êtes connecté à aucune table")
                    return MenuJoueurVue()

                # Récupérer la table et tous les joueurs via l'API
                table_req = requests.get(f"{host}/table/{table_numero}")
                if table_req.status_code != 200:
                    print("Impossible de récupérer les joueurs de la table")
                    return MenuJoueurVue()

                table_info = table_req.json()
                nb_joueurs = len(table_info.get("joueurs", []))
                nb_max = table_info.get("joueur_max", 0)
                pseudos = [
                    f"{j['pseudo']} : {j['credit']} crédits" for j in table_info.get("joueurs", [])
                ]

                print(f"\nTable n°{table_numero} : {nb_joueurs}/{nb_max} joueurs présents")
                print("-" * 40)
                if pseudos:
                    print("\n".join(pseudos))
                else:
                    print("Aucun joueur présent pour le moment")

                return MenuJoueurVue()

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
