from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService


class MenuJoueurVue(VueAbstraite):
    """Vue du menu du joueur

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Afficher les joueurs de la base de données",
                "Lire les regles",
                "Infos de session",
                "Se déconnecter",
                "Changer ses informations",
                "tables",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Infos de session":
                return MenuJoueurVue(Session().afficher())

            case "Afficher les joueurs de la base de données":
                joueurs_str = JoueurService().lister_tous()
                return MenuJoueurVue(joueurs_str)

            case "Lire les regles":
                texte = "les regles"
                return MenuJoueurVue(texte)

            case "Changer ses informations":
                pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
                joueur = JoueurService().trouver_par_pseudo(pseudo)
                
                nouveau_pseudo = inquirer.text(message="Entrez votre  nouveau pseudo : ").execute()
                nouveau_pays = inquirer.text(message="Entrez votre nouveau pays : ").execute()

                joueur_new = Joueur(joueur.id_joueur, nouveau_pseudo, credits, nouveau_pays)
                joueur_n = JoueurService().modifier(joueur_new)
                return MenuJoueurVue(joueur_n)

            case "tables":
                from view.menu_table import MenuTable
                return MenuTable()
                
