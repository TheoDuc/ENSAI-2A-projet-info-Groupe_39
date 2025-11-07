from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.table_service import TableService
from business_object.table import Table
from business_object.joueur import Joueur


class GameMenu(VueAbstraite):
    """Vue du menu de jeu du joueur"""

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu de jeu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Lancer manche",
                "Quitter table",
            ],
        ).execute()

        match choix:
            case "Lancer manche":
                table = Session().joueur.table
               
                TableService().jouer(table)
                return GameMenu("")

            case "Quitter table":
                TableService().retirer_joueur(Session().joueur.table, Session().joueur)
                return MenuJoueurVue(Session().afficher())