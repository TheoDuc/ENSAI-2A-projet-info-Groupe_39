from InquirerPy import inquirer
import os
import requests

from business_object.joueur import Joueur
from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/joueur/connection"

class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir son pseudo
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        # Appel du service pour trouver le joueur
        url = f"{host}{END_POINT}/{pseudo}"
        req = requests.get(url)

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if req.status_code == 200:
            reponse = req.json()
            joueur = Joueur(
                id_joueur=reponse["_Joueur__id_joueur"],
                pseudo=reponse["_Joueur__pseudo"],
                credit=reponse["_Joueur__credit"],
                pays=reponse["_Joueur__pays"],
            )
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
            Session().connexion(joueur)
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (pseudo innexistant, essayez de créer un compte.)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)


