from business_object.joueur import Joueur
from business_object.manche import Manche
from business_object.table import Table
from service.action_service import ActionService
from utils.log_decorator import log


class TableService:
    """
    Service métier pour la gestion des tables de poker :
    - Création, suppression et consultation des tables
    - Gestion des joueurs à l’intérieur des tables
    - Gestion du déroulement des manches
    """

    tables: list[Table] = []
    compteur_tables: int = 0

    @log
    def creer_table(self, joueur_max: int, grosse_blind: int, mode_jeu: int = 1) -> Table:
        TableService.compteur_tables += 1
        numero = TableService.compteur_tables

        table = Table(
            numero_table=numero,
            joueur_max=joueur_max,
            grosse_blind=grosse_blind,
            mode_jeu=mode_jeu,
        )

        TableService.tables.append(table)
        return table

    @log
    def ajouter_joueur(self, table: Table, joueur: Joueur) -> None:
        table.ajouter_joueur(joueur)
        joueur.rejoindre_table(table)

    @log
    def retirer_joueur(self, table: Table, joueur: Joueur) -> None:
        if joueur not in table.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} n'est pas sur la table.")
        joueur.quitter_table()

    @log
    def supprimer_table(self, table: Table) -> None:
        for joueur in list(table.joueurs):
            joueur.quitter_table()
        if table in self.tables:
            self.tables.remove(table)

    @log
    def rotation_dealer(self, table: Table) -> None:
        if not table.joueurs or len(table.joueurs) < 2:
            print("Pas de rotation possible : moins de 2 joueurs.")
            return

        nb_joueurs = len(table.joueurs)
        index_actuel = getattr(table, "dealer_index", 0)  # On part de 0 si non défini

        # Cherche le prochain joueur actif
        for i in range(1, nb_joueurs + 1):
            suivant_index = (index_actuel + i) % nb_joueurs
            suivant = table.joueurs[suivant_index]
            if suivant.est_actif:
                table.dealer_index = suivant_index
                return

        print("Aucun joueur actif trouvé pour devenir dealer.")

    @log
    def action_joueur(self, table: Table, joueur: Joueur, action: str, montant: int = 0) -> None:
        action_service = ActionService()
        if action == "all_in":
            action_service.all_in(table.manche, joueur)
            joueur.est_actif = False
            joueur.all_in = True
        elif action == "checker":
            action_service.checker(table.manche, joueur)
            joueur.a_checke = True
        elif action == "suivre":
            action_service.suivre(table.manche, joueur, montant)
        elif action == "se_coucher":
            action_service.se_coucher(table.manche, joueur)
            joueur.est_actif = False
            joueur.est_couche = True
        else:
            raise ValueError(f"Action inconnue pour le joueur : {action}")

    def demander_action(self, joueur: Joueur, table: Table) -> str:
        """
        Demande au joueur quelle action il souhaite effectuer.
        Retourne une action valide sous forme de chaîne.
        """
        actions_possibles = ["checker", "suivre", "se_coucher", "all_in"]
        while True:
            print(f"\nJoueur {joueur.pseudo} — Crédit: {joueur.credit}")
            print("Actions possibles : ")
            for a in actions_possibles:
                print(f"- {a}")
            action = input("Choisissez votre action : ").strip().lower()
            if action in actions_possibles:
                return action
            print("Action invalide. Réessayez.")

    def demander_montant(self, action: str, joueur: Joueur, table: Table) -> int:
        if action == "suivre":
            while True:
                try:
                    montant = int(input(f"Montant à suivre (max {joueur.credit}) : "))
                    if 0 < montant <= joueur.credit:
                        return montant
                    else:
                        print("Montant invalide.")
                except ValueError:
                    print("Veuillez entrer un nombre valide.")
        elif action == "all_in":
            return joueur.credit
        return 0

    @log
    def jouer(self, table: Table) -> None:
        if len(table.joueurs) < 2:
            raise ValueError("Impossible de démarrer une manche avec moins de deux joueurs.")
        # Réinitialisation des joueurs pour la manche
        for joueur in table.joueurs:
            joueur.est_actif = True
            joueur.a_checke = False
            joueur.est_couche = False
            joueur.all_in = False

        # Création et initialisation de la manche
        table.nouvelle_manche()
        manche: Manche = table.manche

        # Phases du jeu
        for phase in ["preflop", "flop", "turn", "river"]:
            getattr(manche, phase)()
            print(f" Phase {phase.capitalize()} terminée")

            # Boucle sur les joueurs actifs
            while not manche.fin_du_tour():
                for joueur in table.joueurs:
                    if not joueur.est_actif:
                        continue  # Passe les joueurs couchés ou all-in

                    action = self.demander_action(joueur, table)
                    montant = self.demander_montant_si_necessaire(action, joueur, table)

                    try:
                        self.action_joueur(table, joueur, action, montant)
                    except ValueError as e:
                        print(f"Erreur : {e}")
                        continue

        # Distribution du pot

        gains = manche.distribuer_pot()
        for pseudo, montant in gains.items():
            print(f"{pseudo} reçoit {montant} crédits")

        # Rotation du dealer
        self.rotation_dealer(table)
        print("--- Manche terminée ---")
