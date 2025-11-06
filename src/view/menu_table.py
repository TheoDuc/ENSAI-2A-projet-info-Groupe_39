from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite


class MenuTable(VueAbstraite):
    """Vue qui affiche les tables"""

    def choisir_menu(self):
        action_table = ("Retour au Menu Joueur", "Créer une Table", "Les tables")

        choix = inquirer.select(
            message="Choisissez votre action : ",
            choices=action_table,
        ).execute()

        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()
        
        if choix == "Créer une Table":
            from view.menu_creation_table import MenuCreationTable

            return MenuCreationTable()
        
        if choix == "Les tables":
            from view.menu_creation_table import MenuCreationTable
            return 


        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue(pokemons_str)
