import os

import requests
from InquirerPy import inquirer

from view.session import Session
from view.vue_abstraite import VueAbstraite

host = os.environ["HOST_WEBSERVICE"]


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
                "Tables",
                "Se créditer",
                "Infos de session",
                "Afficher les joueurs de la base de données",
                "Changer ses informations",
                "Lire les regles",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Infos de session":
                return MenuJoueurVue(Session().afficher(), temps_attente=3)

            case "Afficher les joueurs de la base de données":
                END_POINT = "/joueur/liste/"
                url = f"{host}{END_POINT}"
                req = requests.get(url)

                reponse = None

                # Si la requete à fonctionné
                if req.status_code == 200:
                    reponse = req.json()
                return MenuJoueurVue(reponse)

            case "Changer ses informations":
                END_POINT = "/joueur"
                joueur = Session().joueur

                nouveau_pseudo = inquirer.text(message="Entrez votre  nouveau pseudo : ").execute()
                nouveau_pays = inquirer.text(message="Entrez votre nouveau pays : ").execute()

                req = requests.put(
                    f"{host}{END_POINT}/{joueur.id_joueur}/{nouveau_pseudo}/{nouveau_pays}"
                )

                reponse = False
                if req.status_code == 200:
                    reponse = req.json()
                print(reponse)

                # Session().joueur = un truc mais je sais pas quoi
                return MenuJoueurVue(reponse)

            case "Tables":
                from view.menu_table import MenuTable

                return MenuTable()

            case "Se créditer":
                joueur = Session().joueur
                admin = inquirer.text(message="Etes vous un administrateur : (oui/non)").execute()
                if admin == "non":
                    return MenuJoueurVue(Session().joueur)
                credit = inquirer.text(message="Entrez votre montant à ajouter : ").execute()
                credit = int(credit)
                END_POINT = "/admin/crediter"

                req = requests.put(f"{host}{END_POINT}/{joueur.pseudo}/{credit}")

                reponse = False
                if req.status_code == 200:
                    reponse = req.json()
                print(reponse)

                # Session().joueur = un truc mais je sais pas quoi
                return MenuJoueurVue(Session().joueur)

            case "Lire les regles":
                texte = """
1. Les cartes :
   - Chaque joueur reçoit 2 cartes cachées (cartes privatives).
   - 5 cartes communes sont placées face visible au centre de la table, partagées par tous les joueurs.

2. Les étapes du jeu :
   - Pré-flop : Chaque joueur reçoit ses 2 cartes privatives. La première ronde d'enchères commence.
   - Le Flop : Trois cartes communes sont révélées. Nouvelle ronde d'enchères.
   - Le Turn : Une quatrième carte commune est révélée. Nouvelle ronde d'enchères.
   - La River : La cinquième et dernière carte commune est révélée. Dernière ronde d'enchères.
   - L'Abattage (Showdown) : Les joueurs restants montrent leurs cartes. Le joueur avec la meilleure main gagne.

3. Les enchères :
   - Suivre (Call) : Miser la même somme que le joueur précédent.
   - Relancer (Raise) : Miser plus que le joueur précédent.
   - Se coucher (Fold) : Abandonner la main et perdre les cartes.
   - Vérifier (Check) : Ne pas miser mais rester dans la partie, si personne n’a relancé avant.

4. Les combinaisons de mains (de la plus faible à la plus forte) :
   - Carte haute : La carte la plus élevée.
   - Paire : Deux cartes de même valeur (par exemple, deux rois).
   - Double paire : Deux paires de cartes de même valeur (par exemple, deux rois et deux 10).
   - Brelan : Trois cartes de même valeur (par exemple, trois 8).
   - Suite : Cinq cartes consécutives (par exemple, 7, 8, 9, 10, Valet).
   - Couleur (Flush) : Cinq cartes de la même couleur (pique, cœur, carreau, trèfle) mais pas nécessairement consécutives.
   - Full : Un brelan et une paire (par exemple, trois 7 et deux rois).
   - Carré : Quatre cartes de même valeur (par exemple, quatre dames).
   - Quinte Flush : Cinq cartes consécutives de la même couleur (par exemple, 5, 6, 7, 8, 9 de cœur).
   - Quinte Flush Royale : La meilleure main possible, c’est une quinte flush de l'As au 10 de la même couleur (par exemple, 10, Valet, Dame, Roi, As de cœur).

5. Gagner la partie :
   - À l'Abattage, le joueur avec la meilleure main gagne le pot.
   - Si un joueur mise de l'argent et que personne ne le suit, il remporte le pot immédiatement, sans devoir montrer ses cartes.

6. Quelques notions supplémentaires :
   - Blinds : Des mises forcées (petite blind et grande blind) sont placées avant que les cartes ne soient distribuées pour garantir qu'il y ait toujours de l'argent dans le pot.
   - dealer : Chaque tour sera initié par le joueur après le dealer 

Le but du poker est d'obtenir la meilleure main possible ou de convaincre les autres joueurs que vous avez la meilleure main pour les amener à se coucher.
"""
                return MenuJoueurVue(texte, input_attente=True)
