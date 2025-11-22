import os
import requests
from InquirerPy import inquirer
import json

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ.get("HOST_WEBSERVICE")


class MenuJoueurVue(VueAbstraite):
    """Menu du joueur avec session locale et récupération des infos via API"""

    def __init__(self, message="", temps_attente=0, input_attente=False):
        super().__init__(message, temps_attente, input_attente)
        self.session = Session()  

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
                "Lire les règles",
                "Se déconnecter",
            ],
        ).execute()

        if not self.session.id_joueur:
            print("Aucun joueur connecté")
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()

        match choix:
            case "Se déconnecter":
                requests.get(f"{host}/joueur/deconnexion/{self.session.id_joueur}")
                self.session.deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue()

            case "Infos de session":
                print(self.session.afficher())
                return MenuJoueurVue(temps_attente=2)

            case "Afficher les joueurs de la base de données":
                try:
                    req = requests.get(f"{host}/joueur/liste/")
                    if req.status_code == 200:
                        reponse = req.json()
                        print(json.dumps(reponse, indent=4, ensure_ascii=False))
                    else:
                        print("Impossible de récupérer la liste des joueurs")
                except Exception:
                    print("Erreur lors de la récupération des joueurs")
                return MenuJoueurVue(temps_attente=3)

            case "Changer ses informations":
                return self.changer_infos()

            case "Tables":
                from view.menu_table import MenuTable
                return MenuTable()

            case "Se créditer":
                return self.se_crediter()

            case "Lire les règles":
                texte = self._texte_regles()
                return MenuJoueurVue(texte, input_attente=True)

    def changer_infos(self):
        """Permet de modifier le pseudo et le pays du joueur"""
        joueur_info = self.session.get_joueur()
        if not joueur_info:
            print("Erreur lors de la récupération du joueur")
            return MenuJoueurVue()

        id_joueur = joueur_info["_Joueur__id_joueur"]
        pseudo_actuel = joueur_info["_Joueur__pseudo"]
        pays_actuel = joueur_info["_Joueur__pays"]

        nouveau_pseudo = inquirer.text(
            message=f"Entrez votre nouveau pseudo (actuel : {pseudo_actuel}) : "
        ).execute()
        nouveau_pays = inquirer.text(
            message=f"Entrez votre nouveau pays (actuel : {pays_actuel}) : "
        ).execute()

        req = requests.put(f"{host}/joueur/{id_joueur}/{nouveau_pseudo}/{nouveau_pays}")
        if req.status_code == 200:
            print("Informations mises à jour avec succès")
        else:
            print("Erreur lors de la mise à jour")
        return MenuJoueurVue()

    def se_crediter(self):
        """Permet à un administrateur d’ajouter du crédit à un joueur"""
        joueur_info = self.session.get_joueur()
        if not joueur_info:
            print("Impossible de récupérer le joueur")
            return MenuJoueurVue()

        pseudo = joueur_info["_Joueur__pseudo"]
        admin = inquirer.text(message="Êtes-vous un administrateur : (oui/non)").execute()
        if admin.lower() != "oui":
            print("Vous n'êtes pas admin")
            return MenuJoueurVue()

        try:
            credit = int(inquirer.text(message="Entrez le montant à ajouter : ").execute())
            req = requests.put(f"{host}/admin/crediter/{pseudo}/{credit}")
            if req.status_code == 200:
                print("Crédit ajouté avec succès")
            else:
                print("Erreur lors de l'ajout de crédit")
        except ValueError:
            print("Montant invalide")
        return MenuJoueurVue()

    def _texte_regles(self):
        """Retourne le texte des règles du poker"""
        return """
1. Les cartes : Chaque joueur reçoit 2 cartes cachées et 5 cartes communes sont placées face visible.
2. Les étapes du jeu : Pré-flop, Flop, Turn, River, Showdown.
3. Les enchères : Call, Raise, Fold, Check.
4. Combinaisons de mains : Carte haute, Paire, Double Paire, Brelan, Suite, Couleur, Full, Carré, Quinte Flush, Quinte Flush Royale.
5. Gagner la partie : À l'Abattage ou si tout le monde se couche.
6. Notions supplémentaires : Blinds, dealer.
"""
