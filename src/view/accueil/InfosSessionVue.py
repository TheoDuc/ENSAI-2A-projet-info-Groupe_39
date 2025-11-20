from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite


class InfosSessionVue(VueAbstraite):
    """Vue pour afficher les informations de la session"""

    def choisir_menu(self):
        """Affiche les infos de session et retourne au menu après un temps d'attente ou input"""

        session = Session()
        texte = session.afficher()

        if session.joueur is None:
            texte += "\n⚠ Aucun joueur n'est actuellement connecté."

        print("\n" + "-" * 50)
        print("Infos de session")
        print("-" * 50 + "\n")
        print(texte)

        inquirer.text(message="Appuyez sur Entrée pour revenir au menu...").execute()

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue()
