import os

import requests
from InquirerPy import inquirer

from service.joueur_service import JoueurService
from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ.get("HOST_WEBSERVICE")


class MenuJoueurVue(VueAbstraite):
    """Menu du joueur avec rafraîchissement de la session multi-joueurs"""

    def __init__(self, message="", temps_attente=0, input_attente=False):
        super().__init__(message, temps_attente, input_attente)
        self.session = Session()
        self.session.refresh()

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Tables",
                "Se créditer",
                "Infos de session",
                "Afficher les joueurs de la base de données",
                "Changer ses informations",
                "Lire les regles",
                "Se déconnecter",
            ],
        ).execute()

        if not self.session.id:
            print("Aucun joueur connecté")
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue()

        match choix:
            case "Se déconnecter":
                requests.get(f"{host}/joueur/deconnection/{self.session.id}")
                self.session.deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Infos de session":
                print(self.session.afficher())
                return MenuJoueurVue(temps_attente=3)

            case "Afficher les joueurs de la base de données":
                try:
                    req = requests.get(f"{host}/joueur/liste/")
                    reponse = req.json() if req.status_code == 200 else None
                    print(reponse)
                except Exception:
                    print("Impossible de récupérer la liste des joueurs")
                return MenuJoueurVue(temps_attente=3)

            case "Tables":
                from view.menu_table import MenuTable

                return MenuTable()

            case "Se créditer":
                joueur = JoueurService().trouver_par_id(self.session.id)
                admin = inquirer.text(message="Etes vous un administrateur : (oui/non)").execute()
                if admin != "oui":
                    print("Vous n'êtes pas admin")
                    return MenuJoueurVue()
                credit = int(inquirer.text(message="Entrez votre montant à ajouter : ").execute())
                requests.put(f"{host}/admin/crediter/{joueur.pseudo}/{credit}")
                return MenuJoueurVue()

            case "Lire les regles":
                texte = "..."  # ton texte de règles
                return MenuJoueurVue(texte, input_attente=True)
