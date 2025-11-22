import logging
import os
import requests
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"

class InfoTableMenu(VueAbstraite):
    """Menu de table multi-joueurs"""

    def choisir_menu(self, numero_table: int):
        logger.info(f"Début InfoTableMenu pour la table {numero_table}")

        print(f"\nBienvenue sur la table {numero_table}\n")
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=["Info de session", "Lancer manche", "Quitter table"],
        ).execute()

        match choix:
            case "Info de session":
                self.afficher_infos_table(numero_table)
                return self  # On reste dans le menu infos table

            case "Lancer manche":
                return self.lancer_manche(numero_table)

            case "Quitter table":
                return self.quitter_table(numero_table)

    def afficher_infos_table(self, numero_table: int):
        # Récupération des joueurs dans la table
        try:
            resp_table = requests.get(f"{host}{END_POINT}{numero_table}")
            table_joueurs_ids = resp_table.json() if resp_table.status_code == 200 else []
        except requests.RequestException:
            table_joueurs_ids = []

        # Récupération des joueurs connectés
        try:
            resp_connectes = requests.get(f"{host}/joueur/connectes/")
            joueurs_connectes_ids = resp_connectes.json() if resp_connectes.status_code == 200 else []
        except requests.RequestException:
            joueurs_connectes_ids = []

        # Filtrage : joueurs connectés sur cette table
        joueurs_en_ligne = [jid for jid in table_joueurs_ids if jid in joueurs_connectes_ids]

        print(f"Table n°{numero_table} ({len(joueurs_en_ligne)}/{len(table_joueurs_ids)}) joueurs connectés")
        for jid in joueurs_en_ligne:
            print(f"Joueur ID : {jid}")
        print()

    def lancer_manche(self, numero_table: int):
        # Vérification qu'au moins 2 joueurs connectés
        try:
            resp_connectes = requests.get(f"{host}/joueur/connectes/")
            joueurs_connectes_ids = resp_connectes.json() if resp_connectes.status_code == 200 else []
        except requests.RequestException:
            joueurs_connectes_ids = []

        try:
            resp_table = requests.get(f"{host}{END_POINT}{numero_table}")
            table_joueurs_ids = resp_table.json() if resp_table.status_code == 200 else []
        except requests.RequestException:
            table_joueurs_ids = []

        joueurs_table_connectes = [jid for jid in table_joueurs_ids if jid in joueurs_connectes_ids]

        if len(joueurs_table_connectes) < 2:
            print("Impossible de lancer la manche : au moins 2 joueurs connectés nécessaires")
            from view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue()

        # Lancement de la manche via API
        try:
            req = requests.get(f"{host}{END_POINT}lancer/{numero_table}")
            if req.status_code == 200:
                print("Manche lancée !")
                from view.menu_manche_vue import MenuManche
                return MenuManche()
            else:
                print("Erreur lors du lancement de la manche")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur : {e}")
            print("Erreur serveur lors du lancement de la manche")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()

    def quitter_table(self, numero_table: int):
        # On suppose que l'API gère le retrait du joueur de la table
        try:
            req = requests.delete(f"{host}{END_POINT}{numero_table}")
            if req.status_code == 200:
                print(f"Vous avez quitté la table {numero_table}")
            else:
                print("Erreur lors de la déconnexion de la table")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur : {e}")
            print("Erreur serveur lors de la déconnexion de la table")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()
