import logging
import os

from InquirerPy import inquirer

from view.menu_manche import MenuManche
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
                import os

                import requests

                from view.menu_joueur_vue import MenuJoueurVue
                from view.session import Session

                session = Session()
                host = os.environ["HOST_WEBSERVICE"]

                # Récupérer toutes les tables
                res_tables = requests.get(f"{host}/table/")
                if res_tables.status_code != 200:
                    print("Impossible de récupérer la liste des tables")
                    return MenuJoueurVue()

                tables = res_tables.json()

                # Trouver la table où le joueur connecté est présent
                table_info = None
                for t in tables:
                    for j in t.get("joueurs", []):
                        if j.get("id_joueur") == session.id:
                            table_info = t
                            break
                    if table_info:
                        break

                if not table_info:
                    print("Vous n'êtes connecté à aucune table")
                    return MenuJoueurVue()

                # Affichage des infos de la table
                numero_table = table_info.get("numero_table", "?")
                nb_joueurs = len(table_info.get("joueurs", []))
                nb_max = table_info.get("joueur_max", 0)

                print(f"\nTable n°{numero_table} : {nb_joueurs}/{nb_max} joueurs présents")
                print("-" * 40)
                for j in table_info.get("joueurs", []):
                    pseudo = j.get("pseudo", "Inconnu")
                    credit = j.get("credit", 0)
                    print(f"{pseudo} : {credit} crédits")

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
