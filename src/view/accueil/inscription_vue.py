from InquirerPy import inquirer

from service.joueur_service import JoueurService
from view.vue_abstraite import VueAbstraite


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        if JoueurService().pseudo_deja_utilise(pseudo):
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")

        pays = inquirer.text(message="Entrez votre pays : ").execute()

        # Appel du service pour créer le joueur
        joueur = JoueurService().creer(pseudo, pays)

        # Si le joueur a été créé
        if joueur:
            message = (
                f"Votre compte {joueur.pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
