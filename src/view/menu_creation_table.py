from InquirerPy import inquirer

from service.table_service import TableService
from view.vue_abstraite import VueAbstraite


class MenuCreationTable(VueAbstraite):
    """Vue de Creation de table"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir les paramètres de la table
        joueur_max = inquirer.number(message="Saisissez le nombre de joueurs maximum dans la table", min_allowed=2, max_allowed=10).execute()
        grosse_blind = inquirer.number(message="Saisissez la valeur de la grosse blind", min_allowed=2).execute()

        # Appel du service pour créer la table
        table = TableService().creer_table(joueur_max, grosse_blind)

        # Si le joueur a été créé
        if table:
            message = (
                f"Votre table a été créé (n°{table.numero_table}). Vous pouvez maintenant la rejoindre"
            )
        else:
            message = "Erreur de création de la table (les paramètres de la table sont incorrects)"




        from view.menu_table import MenuTable

        return MenuTable()

class InfosTable(VueAbstraite):

    def infos_table(self):
        