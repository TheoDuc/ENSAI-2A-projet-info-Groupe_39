import os

import requests
from InquirerPy import inquirer

from business_object.table import Table
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/table/"


class MenuCreationTable(VueAbstraite):
    """Vue de Creation de table"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir les paramètres de la table
        joueur_max = inquirer.number(
            message="Saisissez le nombre de joueurs maximum dans la table",
            min_allowed=2,
            max_allowed=10,
            default=5,
        ).execute()
        joueur_max = int(joueur_max)
        grosse_blind = inquirer.number(
            message="Saisissez la valeur de la grosse blind", min_allowed=2, default=40
        ).execute()
        grosse_blind = int(grosse_blind)

        table = {
            "numero_table": 0,
            "joueur_max": joueur_max,
            "grosse_blind": grosse_blind,
            "mode_jeu": 0,
        }
        req = requests.post(f"{host}{END_POINT}", json=table)

        # Si le joueur a été créé
        if req.status_code == 200:
            message = "Votre table a été créé. Vous pouvez maintenant la rejoindre"
        else:
            message = "Erreur de création de la table (les paramètres de la table sont incorrects)"

        from view.menu_table import MenuTable

        return MenuTable(message, temps_attente=3)


class InfosTable(VueAbstraite):
    """
    Vue permettant d'afficher les informations d'une table :
    - Numéro de la table
    - Nombre de joueurs présents / nombre max
    - Liste des joueurs présents
    """

    def infos_table(self, table: Table) -> None:
        """
        Affiche le statut complet de la table :
        - Numéro de la table
        - Nombre de joueurs présents / nombre max
        - Liste des joueurs présents
        """
        nb_joueurs_present = len(table.joueurs)
        nb_max = table.joueur_max
        pseudos = [joueur.pseudo for joueur in table.joueurs]

        print(f"Table n°{table.numero_table} : {nb_joueurs_present}/{nb_max} joueurs présents")
        if pseudos:
            print("Joueurs présents : " + ", ".join(pseudos))
        else:
            print("Aucun joueur présent pour le moment.")
