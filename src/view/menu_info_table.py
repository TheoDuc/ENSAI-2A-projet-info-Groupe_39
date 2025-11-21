import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Menu de table multi-joueurs"""

    def choisir_menu(self):
        logger.info("Début InfoTableMenu.choisir_menu()")
        session = Session()
        session.refresh()  # Rafraîchit les infos du joueur et des tables
        logger.info(f"ID session : {session.id}")
        logger.info(f"Joueurs connectés : {[j.id_joueur for j in Session.joueurs_connectes]}")

        joueur = next((j for j in Session.joueurs_connectes if j.id_joueur == session.id), None)
        if not joueur:
            logger.warning("Erreur : joueur non trouvé dans la session")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        logger.info(f"Joueur courant : {joueur.pseudo}, table : {joueur.numero_table}")

        print("\nMenu de jeu Joueur")
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=["Info de session", "Lancer manche", "Quitter table"],
        ).execute()

        match choix:
            case "Info de session":
                self.afficher_infos_table(joueur)
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

            case "Lancer manche":
                return self.lancer_manche(joueur)

            case "Quitter table":
                return self.quitter_table(joueur)

    def afficher_infos_table(self, joueur):
        logger.info(f"Affichage infos table pour {joueur.pseudo}")
        table = Session.tables_globales.get(joueur.numero_table)
        if not table:
            logger.warning("Aucune table trouvée pour ce joueur")
            print("Vous n'êtes connecté à aucune table")
            return

        print(
            f"Table n°{table.numero_table} ({len(table.joueurs)}/{table.joueur_max}) joueurs présents"
        )
        for j in table.joueurs:
            print(f"{j.pseudo} : {j.credit} crédits")

    def lancer_manche(self, joueur):
        logger.info(f"Tentative de lancer manche pour {joueur.pseudo}")
        table = Session.tables_globales.get(joueur.numero_table)

        if not joueur.numero_table:
            logger.warning("Le joueur n'est connecté à aucune table")

            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if len(table.joueurs) < 2:
            logger.warning("Impossible de lancer la manche : moins de 2 joueurs")
            print("Impossible de lancer la manche : au moins 2 joueurs nécessaires")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        try:
            req = requests.get(f"{host}{END_POINT}lancer/{joueur.numero_table}")
            if req.status_code == 200:
                logger.info("Manche lancée avec succès")
                print("Manche lancée !")
                from view.menu_manche_vue import MenuManche

                return MenuManche()
            else:
                logger.error(f"Erreur lors du lancement de la manche (status {req.status_code})")
                print("Erreur lors du lancement de la manche")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur : {e}")
            print("Erreur serveur lors du lancement de la manche")

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()

    def quitter_table(self, joueur):
        logger.info(f"Tentative de quitter table pour {joueur.pseudo}")
        table = Session.tables_globales.get(joueur.numero_table)

        if not table:
            logger.warning("Le joueur n'est connecté à aucune table")
            print("Vous n'êtes actuellement à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        try:
            index = table.joueurs.index(joueur)
            table.retirer_joueur(index)
            logger.info(f"Joueur {joueur.pseudo} retiré de la table {table.numero_table}")
        except ValueError:
            logger.error("Erreur : impossible de retirer le joueur de la table")

        Session.tables_globales[table.numero_table] = table
        joueur.numero_table = None

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()
