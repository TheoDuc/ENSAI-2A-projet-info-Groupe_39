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
                import requests

                from view.menu_joueur_vue import MenuJoueurVue
                from view.session import Session

                session = Session()
                if not session.id:
                    print("Aucun joueur connecté")
                    return MenuJoueurVue()

                res_tables = requests.get(f"{host}/table/")
                if res_tables.status_code != 200:
                    print("Impossible de récupérer la liste des tables")
                    return MenuJoueurVue()

                try:
                    tables = res_tables.json()
                except Exception:
                    print("Erreur : impossible de décoder la réponse JSON")
                    return MenuJoueurVue()

                # Chercher la table où le joueur est présent
                table_info = None
                for t in tables:
                    if not isinstance(t, dict):
                        continue
                    joueurs = t.get("joueurs")
                    if not isinstance(joueurs, list):
                        continue
                    for j in joueurs:
                        if isinstance(j, dict) and j.get("id_joueur") == session.id:
                            table_info = t
                            break
                    if table_info:
                        break

                if not table_info:
                    print("Vous n'êtes connecté à aucune table")
                    return MenuJoueurVue()

                # Afficher les infos
                numero_table = table_info.get("numero_table", "?")
                nb_joueurs = len(table_info.get("joueurs", []))
                nb_max = table_info.get("joueur_max", 0)

                print(f"\nTable n°{numero_table} : {nb_joueurs}/{nb_max} joueurs présents")
                print("-" * 40)
                for j in table_info.get("joueurs", []):
                    pseudo = j.get("pseudo", "Inconnu") if isinstance(j, dict) else "Inconnu"
                    credit = j.get("credit", 0) if isinstance(j, dict) else 0
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
            case "Quitter table":
                import requests

                from view.menu_creation_table import MenuCreationTable
                from view.session import Session

                session = Session()
                id_joueur = session.id
                url = f"{host}/table/retirer/{id_joueur}"

                try:
                    req = requests.put(url)
                    if req.status_code == 200:
                        message = req.json().get("message", "Vous avez quitté la table")
                    else:
                        message = req.json().get("error", "Impossible de quitter la table")
                except Exception as e:
                    message = f"Erreur lors de la requête : {e}"

                return MenuCreationTable(message)
