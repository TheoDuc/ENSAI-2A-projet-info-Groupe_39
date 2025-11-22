import logging
import os
import requests
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)
host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"


class InfoTableMenu(VueAbstraite):
    """Menu de gestion d'une table ."""

    def choisir_menu(self, numero_table: int):
        """Boucle principale du menu de la table."""
        while True:
            print(f"\nBienvenue sur la table {numero_table}\n")
            choix = inquirer.select(
                message="Faites votre choix :",
                choices=["Voir joueurs", "Lancer manche", "Quitter table"],
            ).execute()

            if choix == "Voir joueurs":
                self.afficher_infos_table(numero_table)

            elif choix == "Lancer manche":
                menu_manche = self.lancer_manche(numero_table)
                if menu_manche:
                    return menu_manche  

            elif choix == "Quitter table":
                return self.quitter_table(numero_table)

    def afficher_infos_table(self, numero_table: int):
        joueurs_ids = self.get_joueurs_table(numero_table)

        print(f"\nTable n°{numero_table} ({len(joueurs_ids)} joueurs présents)")
        for jid in joueurs_ids:
            print(f" - Joueur ID : {jid}")
        print()

    def get_joueurs_table(self, numero_table: int):
        try:
            resp = requests.get(f"{host}{END_POINT}joueurs/{numero_table}")
            if resp.status_code == 200:
                return resp.json()
            else:
                print("Impossible de récupérer les joueurs de la table")
                return []
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la récupération des joueurs : {e}")
            print("Erreur serveur lors de la récupération des joueurs de la table")
            return []

    def lancer_manche(self, numero_table: int):
        joueurs_ids = self.get_joueurs_table(numero_table)
        if not joueurs_ids:
            print("Impossible de lancer la manche : aucun joueur présent")
            return None

        try:
            resp = requests.put(f"{host}/manche/lancer/{numero_table}")
            if resp.status_code == 200:
                print("Manche lancée !")
                id_joueur = joueurs_ids[0]
                pseudo = f"Joueur{id_joueur}"

                from view.menu_manche import MenuManche
                return MenuManche().choisir_menu(numero_table, id_joueur, pseudo)
            else:
                print("Erreur lors du lancement de la manche")
                return None
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors du lancement de la manche : {e}")
            print("Erreur serveur lors du lancement de la manche")
            return None

    def quitter_table(self, numero_table: int):
        try:
            resp = requests.delete(f"{host}{END_POINT}{numero_table}")
            if resp.status_code == 200:
                print(f"Vous avez quitté la table {numero_table}")
            else:
                print("Erreur lors de la déconnexion de la table")
        except requests.RequestException as e:
            logger.error(f"Erreur serveur lors de la déconnexion de la table : {e}")
            print("Erreur serveur lors de la déconnexion de la table")

        from view.menu_joueur_vue import MenuJoueurVue
        return MenuJoueurVue()
