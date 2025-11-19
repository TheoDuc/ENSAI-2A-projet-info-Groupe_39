from InquirerPy import inquirer

from service.table_service import TableService
from view.session import Session
from view.vue_abstraite import VueAbstraite


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

                TableService().lancer_manche(table.numero_table)
                return GameMenu("")

            case "Quitter table":
                TableService().retirer_joueur(Session().joueur.id_joueur)

                from view.menu_joueur_vue import MenuJoueurVue

                return MenuJoueurVue(Session().afficher())
