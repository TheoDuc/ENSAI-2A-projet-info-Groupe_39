from InquirerPy import inquirer

from service.table_service import TableService
from view.session import Session
from view.vue_abstraite import VueAbstraite


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def choisir_menu(self):
        action_table = ["Retour au Menu Joueur", "Créer une Table"] 
        boutons_tables = TableService().affichages_tables()
        action_table += boutons_tables

        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        if choix == "Créer une Tables":
            from view.menu_creation_table import MenuCreationTable

            return MenuCreationTable()

        if choix in boutons_tables:
            indice_table = boutons_tables.index(choix)

            TableService().ajouter_joueur(TableService.tables[indice_table], Session().joueur)

            from view.game_menu_view import GameMenu

            return GameMenu()
