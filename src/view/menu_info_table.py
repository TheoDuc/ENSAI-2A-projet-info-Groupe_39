import logging
import os

import requests
from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite

logger = logging.getLogger(__name__)

host = os.environ.get("HOST_WEBSERVICE")
END_POINT = "/table/"


from view.session import Session


class InfoTableMenu(VueAbstraite):
    """Menu de jeu du joueur avec gestion multi-joueurs."""

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nMenu de jeu Joueur\n" + "-" * 50 + "\n")

        # Rafraîchir les joueurs connectés
        self.refresh_joueurs_connectes()

        session = Session()
        if not session.id:
            print("Aucun joueur connecté")
            return MenuJoueurVue()

        # Récupérer le joueur connecté
        joueur_connecte = next(
            (j for j in Session.joueurs_connectes if j.id_joueur == session.id), None
        )
        if not joueur_connecte:
            print("Erreur : joueur non trouvé dans la session")
            return MenuJoueurVue()

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
                self.afficher_infos_table(joueur_connecte)
                return MenuJoueurVue()

            case "Lancer manche":
                return self.lancer_manche(joueur_connecte)

            case "Quitter table":
                return self.quitter_table(joueur_connecte)

    # -----------------------------
    # Méthodes internes
    # -----------------------------
    def refresh_joueurs_connectes(self):
        """Rafraîchit la liste des joueurs connectés depuis l'API"""
        try:
            res = requests.get(f"{host}/joueur/")
            res.raise_for_status()
            all_joueurs = res.json()
            Session.joueurs_connectes = [
                Joueur.from_json(j) for j in all_joueurs if j.get("est_connecte", False)
            ]
        except Exception:
            logger.warning("Impossible de rafraîchir la liste des joueurs connectés")

    def get_table_api(self, numero_table):
        """Récupère la table depuis l'API et met à jour Session.tables_globales"""
        try:
            res = requests.get(f"{host}{END_POINT}{numero_table}")
            res.raise_for_status()
            table_data = res.json()
            table = Table.from_json(table_data)
            Session.tables_globales[numero_table] = table
            return table
        except Exception:
            print(f"Impossible de récupérer la table {numero_table} depuis le serveur")
            return None

    def afficher_infos_table(self, joueur):
        """Affiche les informations de la table où le joueur est connecté"""
        if not joueur.numero_table:
            print("Vous n'êtes connecté à aucune table")
            return

        table = self.get_table_api(joueur.numero_table)
        if not table:
            return

        nb_joueurs = len(table.joueurs)
        nb_max = table.joueur_max

        print(f"\nTable n°{table.numero_table} : {nb_joueurs}/{nb_max} joueurs présents")
        print("-" * 40)
        for j in table.joueurs:
            debut = getattr(j, "debut_connexion", "Non connecté")
            print(f"{j.pseudo} : {j.credit} crédits (connexion : {debut})")

    def lancer_manche(self, joueur):
        """Lance la manche si la table est prête"""
        if not joueur.numero_table:
            print("Vous n'êtes connecté à aucune table")
            return MenuJoueurVue()

        table = self.get_table_api(joueur.numero_table)
        if not table or len(table.joueurs) < 2:
            print("Impossible de lancer la manche : au moins 2 joueurs nécessaires")
            return MenuJoueurVue()

        try:
            req = requests.get(f"{host}{END_POINT}lancer/{joueur.numero_table}")
            if req.status_code == 200:
                print("Manche lancée !")
                from view.menu_manche_vue import MenuManche

                return MenuManche()
            else:
                print("Erreur lors du lancement de la manche")
                return MenuJoueurVue()
        except requests.RequestException:
            print("Erreur : impossible de contacter le serveur")
            return MenuJoueurVue()

    def quitter_table(self, joueur):
        """Permet à un joueur de quitter sa table"""
        if not joueur.table:
            print("Vous n'êtes actuellement à aucune table")
            return MenuJoueurVue()

        table = self.get_table_api(joueur.numero_table)
        if not table:
            return MenuJoueurVue()

        try:
            index = table.joueurs.index(joueur)
            table.retirer_joueur(index)
            logger.info(f"Vous avez quitté la table {table.numero_table}")
        except ValueError:
            logger.info("Erreur : impossible de vous retirer de la table")

        # Mise à jour de la table globale
        Session.tables_globales[table.numero_table] = table
        joueur.numero_table = None

        return MenuJoueurVue()
