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
        logger.info("Session rafraîchie")

        # On récupère le joueur connecté
        joueur = next((j for j in Session.joueurs_connectes if j.id_joueur == session.id), None)
        if not joueur:
            logger.error("Erreur : joueur non trouvé dans la session")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        logger.info(f"Menu de jeu pour le joueur {joueur.pseudo} (id={joueur.id_joueur})")
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
            logger.warning("Vous n'êtes connecté à aucune table")
            return
        logger.info(
            f"Table n°{table.numero_table} ({len(table.joueurs)}/{table.joueur_max}) joueurs présents"
        )
        for j in table.joueurs:
            logger.info(f"{j.pseudo} : {j.credit} crédits")

    def lancer_manche(self, joueur):
        table = Session.tables_globales.get(joueur.numero_table)
        if not joueur.numero_table:
            logger.warning("Vous n'êtes connecté à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if len(table.joueurs) < 2:
            logger.warning(
                f"Impossible de lancer la manche : {len(table.joueurs)} joueur(s) présent(s), minimum 2 requis"
            )
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        try:
            req = requests.get(f"{host}{END_POINT}lancer/{joueur.numero_table}")
            logger.info(f"Appel API /table/lancer/{joueur.numero_table} status={req.status_code}")
            if req.status_code == 200:
                logger.info("Manche lancée avec succès !")
                from view.menu_manche_vue import MenuManche

                return MenuManche()
            else:
                logger.error(f"Erreur lors du lancement de la manche : {req.text}")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors du lancement de la manche : {e}")

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()

    def quitter_table(self, joueur):
        table = getattr(joueur, "table", None)
        if not table:
            logger.warning("Vous n'êtes actuellement à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        try:
            index = table.joueurs.index(joueur)
            table.retirer_joueur(index)
            logger.info(f"Vous avez quitté la table {table.numero_table}")
        except ValueError:
            logger.error("Erreur : impossible de vous retirer de la table")

        Session.tables_globales[table.numero_table] = table
        joueur.numero_table = None

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()
