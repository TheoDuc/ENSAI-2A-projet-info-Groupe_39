import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/action/"


class MenuManche(VueAbstraite):
    """Menu du joueur pendant une manche de poker multi-joueurs."""

    def choisir_menu(self):
        """Affiche le menu principal de la manche et gère les actions du joueur."""

        session = Session()
        if not session.id:
            print("Aucun joueur connecté")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        # Récupération du joueur courant
        joueur = next((j for j in session.joueurs_connectes if j.id_joueur == session.id), None)
        if not joueur or not joueur.numero_table:
            logger.info("Vous n'êtes connecté à aucune table")
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        numero_table = joueur.numero_table
        pseudo = joueur.pseudo

        print("\n" + "-" * 50 + "\nMenu de jeu - Manche\n" + "-" * 50 + "\n")

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

        match choix:
            case "Voir les infos de la manche":
                self.voir_infos_manche(numero_table)
                return MenuManche()

            case "Regarder main":
                self.voir_main(numero_table, joueur.id_joueur)
                return MenuManche()

            case "Checker":
                self.effectuer_action("checker", pseudo)
                return MenuManche()

            case "Suivre":
                self.effectuer_action("suivre", pseudo)
                return MenuManche()

            case "All in":
                self.effectuer_action("all_in", pseudo)
                return MenuManche()

            case "Se coucher":
                self.effectuer_action("se_coucher", pseudo)
                return MenuManche()

            case "Quitter manche":
                self.quitter_manche(numero_table, joueur)
                from view.game_menu_view import GameMenu

                return GameMenu(session.afficher())

    def voir_infos_manche(self, numero_table):
        """Affiche l’état complet de la manche (pot, joueurs, mises...)."""
        try:
            req = requests.get(f"{host}/table/affichage/{numero_table}")
            if req.status_code == 200:
                print(req.text)
            else:
                print("Impossible de récupérer les infos de la manche")
        except requests.RequestException:
            print("Erreur : impossible de contacter le serveur")

    def voir_main(self, numero_table, id_joueur):
        """Affiche la main du joueur courant."""
        try:
            req = requests.get(f"{host}/table/main/{numero_table}/{id_joueur}")
            if req.status_code == 200:
                print(req.text)
            else:
                print("Impossible de récupérer votre main")
        except requests.RequestException:
            print("Erreur : impossible de contacter le serveur")

    def effectuer_action(self, action, pseudo):
        """Exécute une action (checker, suivre, all_in, se_coucher) pour le joueur."""
        try:
            req = requests.put(f"{host}{END_POINT}{action}/{pseudo}")
            if req.status_code == 200:
                print(f"Action '{action}' effectuée avec succès")
            else:
                print(f"Impossible de '{action}', réessayez")
        except requests.RequestException:
            print(f"Erreur serveur lors de l'action '{action}'")

    def quitter_manche(self, numero_table, joueur):
        """Permet au joueur de quitter la manche."""
        try:
            req = requests.get(f"{host}/table/terminer/{numero_table}")
            if req.status_code == 200:
                print("Vous avez quitté la manche")
            else:
                print("Impossible de quitter la manche")
        except requests.RequestException:
            print("Erreur : impossible de contacter le serveur")

        # Mise à jour de la table globale et de la session
        table = Session.tables_globales.get(numero_table)
        if table and joueur in table.joueurs:
            try:
                index = table.joueurs.index(joueur)
                table.retirer_joueur(index)
                Session.tables_globales[numero_table] = table
                joueur.numero_table = None
            except ValueError:
                logger.warning("Erreur lors du retrait du joueur de la table")
