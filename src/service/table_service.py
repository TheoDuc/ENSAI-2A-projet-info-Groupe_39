"""Implémentation de la classe TableService"""

from business_object.manche import Manche
from business_object.table import Table
from service.joueur_service import JoueurService
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

    def liste_tables(self) -> list[Table]:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """
        return self.tables

    def table_par_numero(self, numero_table: int) -> Table:
        """Blabla"""
        pass

    @log
    def creer_table(self, joueur_max: int, grosse_blind: int, mode_jeu: int = 1) -> Table:
        """
        Créer une table de jeu de poker

        Paramètres
        ----------
        joueur_max : int
            le nombre de joueurs maximum que la table peut accueillir
        hrosse_blind : int
            la valeur de la grosse blind
        mode_jeu : int
            le code du mode de jeu de la table

        Renvois
        -------
        Table
            la table créée
        """

        self.compteur_tables += 1
        numero = TableService.compteur_tables

        table = Table(
            numero_table=numero,
            joueur_max=joueur_max,
            grosse_blind=grosse_blind,
            mode_jeu=mode_jeu,
        )

        self.tables.append(table)
        return table

    @log
    def supprimer_table(self, table: Table) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """

        for joueur in list(table.joueurs):
            joueur.quitter_table()
        if table in self.tables:
            self.tables.remove(table)

    @log
    def ajouter_joueur(self, numero_table: int, id_joueur: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """

        joueur = JoueurService().trouver_par_id(id_joueur)
        table = self.table_par_numero(numero_table)

        joueur.rejoindre_table(table)

    @log
    def retirer_joueur(self, id_joueur: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        joueur.quitter_table()

    def affichages_tables(self) -> list[str]:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """

        return [str(table) for table in self.tables]

    @log
    def jouer(self, table: Table) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        ...

        Renvois
        -------
        ...
        """

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
                for i in range(len(table.joueurs)):
                    if not joueur.est_actif:
                        continue  # Passe les joueurs couchés ou all-in

                    print(f"Votre main est : {manche.info.mains[i]}")
                    print(f"Le board est : {manche.board}")

                    action = self.demander_action(joueur, table)
                    montant = self.demander_montant(action, joueur, table)

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
