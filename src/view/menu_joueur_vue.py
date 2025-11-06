from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService
from service.credit_service import CreditService
from business_object.joueur import Joueur


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
                "tables",
                "Afficher les joueurs de la base de données",
                "Lire les regles",
                "Infos de session",
                "Changer ses informations",
                "Se créditer",
                "Se déconnecter",
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
                joueur = Session().joueur
                
                nouveau_pseudo = inquirer.text(message="Entrez votre  nouveau pseudo : ").execute()
                nouveau_pays = inquirer.text(message="Entrez votre nouveau pays : ").execute()

                nouveau_joueur = Joueur(joueur.id_joueur, nouveau_pseudo, joueur.credit, nouveau_pays)
                joueur_n = JoueurService().modifier(nouveau_joueur)
                return MenuJoueurVue(joueur_n)

            case "Tables":
                from view.menu_table import MenuTable
                return MenuTable()

            case "Se créditer":
                joueur = Session().joueur
                credit = inquirer.text(message="Entrez votre montant à ajouter : ").execute()
                nouveau_credit = CreditService().crediter(joueur, int(credit))
                return MenuJoueurVue(Session().joueur)
                
