import os

import requests
from InquirerPy import inquirer

from business_object.joueur import Joueur
from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]
END_POINT = "/joueur/connexion"  # Corrigé : "connexion" avec deux n


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo)"""

    def choisir_menu(self):
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        url = f"{host}{END_POINT}/{pseudo}"

        try:
            req = requests.get(url)
            req.raise_for_status()
        except requests.RequestException:
            print("Erreur serveur ou pseudo inexistant")
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue("Erreur serveur ou pseudo inexistant", temps_attente=2)

        data = req.json()
        joueur = Joueur(
            id_joueur=data["_Joueur__id_joueur"],
            pseudo=data["_Joueur__pseudo"],
            credit=data["_Joueur__credit"],
            pays=data["_Joueur__pays"],
        )

        # Connexion dans la session (avec l'ID seulement)
        Session().connexion(joueur.id_joueur)

        message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"
        from view.menu_joueur_vue import MenuJoueurVue

        return MenuJoueurVue(message, temps_attente=1)
