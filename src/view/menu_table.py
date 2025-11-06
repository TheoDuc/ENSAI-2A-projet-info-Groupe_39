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
            from view.menu_creation_table import InfosTable

            infos_vue = InfosTable()  # Instancie la vue
            service = TableService()  # Accède aux tables existantes

            if not service.tables:
                print("Aucune table créée pour le moment.")
            else:
                for table in service.tables:
                    infos_vue.infos_table(table)
            input("\nAppuyez sur Entrée pour revenir au menu principal...")
            return self

        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue(pokemons_str)
