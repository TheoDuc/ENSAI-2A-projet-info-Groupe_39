import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)
host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Menu de table multi-joueurs"""

    def choisir_menu(self):
        session = Session()
        session.refresh()
        joueur = next((j for j in Session.joueurs_connectes if j.id_joueur == session.id), None)
        if not joueur:
            from view.menu_joueur_vue import MenuJoueurVue

            print("Erreur : joueur non trouvé dans la session")
            return MenuJoueurVue()

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
        """Affiche les infos de la table"""
        table = Session.tables_globales.get(joueur.numero_table)
        if not table:
            print("Vous n'êtes connecté à aucune table")
            return
        print(
            f"Table n°{table.numero_table} ({len(table.joueurs)}/{table.joueur_max}) joueurs présents"
        )
        for j in table.joueurs:
            print(f"{j.pseudo} : {j.credit} crédits")

    def lancer_manche(self, joueur):
        if not joueur.numero_table:
            print("Vous n'êtes connecté à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()
        table = Session.tables_globales.get(joueur.numero_table)
        if len(table.joueurs) < 2:
            print("Impossible de lancer la manche : au moins 2 joueurs nécessaires")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        try:
            req = requests.get(f"{host}{END_POINT}lancer/{joueur.numero_table}")
            if req.status_code == 200:
                print("Manche lancée !")
                from view.menu_manche_vue import MenuManche

                return MenuManche()
        except requests.RequestException:
            print("Erreur serveur")
        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()

    def quitter_table(self, joueur):
        if not joueur.table:
            print("Vous n'êtes actuellement à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        table = joueur.table
        try:
            index = table.joueurs.index(joueur)
            table.retirer_joueur(index)
            logger.info(f"Vous avez quitté la table {table.numero_table}")
        except ValueError:
            logger.info("Erreur : impossible de vous retirer de la table")
        Session.tables_globales[table.numero_table] = table
        joueur.numero_table = None
        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()
