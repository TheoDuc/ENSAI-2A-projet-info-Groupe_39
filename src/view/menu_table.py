"""Menu des tables"""

import logging
import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"

logger = logging.getLogger(__name__)


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def choisir_menu(self):
        action_table = ["Retour au Menu Joueur", "Créer une Table"]

        # Récupération des tables existantes
        try:
            reponse = requests.get(f"{host}{END_POINT}")
            boutons_tables = reponse.json()  # Doit être une liste ["Table 1", "Table 2", ...]
        except ValueError:
            boutons_tables = []

        # Ajout des tables
        action_table += boutons_tables

        # Sélection du choix
        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        # --- CAS FIXES ---

        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if choix == "Créer une Table":
            from view.menu_creation_table import MenuCreationTable

            return MenuCreationTable()

        # --- CAS DES TABLES DYNAMIQUES ---

        if choix in boutons_tables:
            session = Session()

            if not getattr(session, "id", None):
                print("Aucun joueur connecté")
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

            # Extraction du numéro de table
            numero_table = int(choix.split()[1].replace(",", ""))
            id_joueur = session.id

            # Appel API pour rejoindre la table
            req = requests.put(f"{host}{END_POINT}ajouter/{numero_table}/{id_joueur}")

            if req.status_code == 200:
                # Met à jour la session globale
                joueur = next(
                    (j for j in Session.joueurs_connectes if j.id_joueur == id_joueur),
                    None,
                )
                if joueur:
                    joueur.numero_table = numero_table

                print(f"Vous êtes connecté sur la table {numero_table}")
                from view.menu_info_table import InfoTableMenu

                return InfoTableMenu()

            else:
                print("Erreur lors de la connexion à la table")
                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue()

        # Sécurité : retour menu joueur si choix invalide (rare)
        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue()
