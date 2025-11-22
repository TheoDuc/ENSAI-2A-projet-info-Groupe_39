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
    """Menu du joueur pendant une manche"""

    def __init__(
        self,
        numero_table: int,
        pseudo: str = "?",
        message="",
        temps_attente=0,
        input_attente=False,
    ):
        self.numero_table = numero_table
        self.pseudo = pseudo
        super().__init__(message, temps_attente, input_attente)

    def choisir_menu(self):
        """Boucle principale du menu pendant la manche."""
        print("\n" + "-" * 50)
        print(f"Menu Manche - Table {self.numero_table} - Joueur {self.pseudo}")
        print("-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=[
                "Voir infos manche",
                "Voir main",
                "Checker",
                "Suivre",
                "All in",
                "Se coucher",
                "Quitter manche",
            ],
        ).execute()

        if choix == "Voir infos manche":
            self.voir_infos_manche(self.numero_table)

        elif choix == "Voir main":
            self.voir_main(self.numero_table, Session.id_joueur)

        elif choix in ["Checker", "Suivre", "All in", "Se coucher"]:
            mapping = {
                "Checker": "checker",
                "Suivre": "suivre",
                "All in": "all_in",
                "Se coucher": "se_coucher",
            }
            self.effectuer_action(mapping[choix], Session.id_joueur)

        elif choix == "Quitter manche":
            self.quitter_manche(self.numero_table)
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

    # -------------------------
    # Actions et affichages
    # -------------------------
    def voir_infos_manche(self, numero_table: int):
        try:
            resp = requests.get(f"{host}/manche/affichage/{numero_table}")
            if resp.status_code == 200:
                print(resp.text)
            else:
                print("Impossible de récupérer les infos de la manche")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'affichage de la manche : {e}")
            print("Erreur serveur lors de l'affichage de la manche")

    def voir_main(self, numero_table: int, id_joueur: int):
        try:
            resp = requests.get(f"{host}/manche/main/{numero_table}/{id_joueur}")
            if resp.status_code == 200:
                print(resp.text)
            else:
                print("Impossible de récupérer votre main")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'affichage de la main : {e}")
            print("Erreur serveur lors de l'affichage de la main")

    def effectuer_action(self, action: str, id_joueur: int):
        try:
            resp = requests.put(f"{host}{END_POINT}{action}/{id_joueur}")
            if resp.status_code == 200:
                print(f"Action '{action}' effectuée !")
            else:
                print(f"Impossible de faire '{action}'")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de l'action '{action}' : {e}")
            print(f"Erreur serveur lors de l'action '{action}'")

    def quitter_manche(self, numero_table: int):
        try:
            resp = requests.get(f"{host}/manche/terminer/{numero_table}")
            if resp.status_code == 200:
                print("Vous avez quitté la manche")
            else:
                print("Impossible de quitter la manche")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la fermeture de la manche : {e}")
            print("Erreur serveur lors de la fermeture de la manche")
