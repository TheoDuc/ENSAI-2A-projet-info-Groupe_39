from business_object.joueur import Joueur
from business_object.table import Table
from utils.log_decorator import log


class TableService:
    """
    Service métier pour la gestion des tables de poker :
    - Création, suppression et consultation des tables
    - Gestion des joueurs à l’intérieur des tables
    """

    tables: list[Table] = []

    @log
    def creer_table(self, joueur_max: int, grosse_blind: int, mode_jeu: int = 1) -> Table:
        """
        Crée une nouvelle table et l’ajoute à la liste des tables.

        Paramètres
        ----------
        joueur_max : int
            Nombre maximum de joueurs sur la table
        grosse_blind : int
            Valeur de la grosse blind
        mode_jeu : int, optionnel
            Mode de jeu (1 = Texas Hold'em), par défaut 1

        Renvoie
        -------
        Table
            L’objet Table créé
        """
        table = Table(joueur_max=joueur_max, grosse_blind=grosse_blind, mode_jeu=mode_jeu)
        self.tables.append(table)
        return table

    @log
    def ajouter_joueur(self, table: Table, joueur: Joueur) -> None:
        """
        Ajoute un joueur à une table existante.

        Paramètres
        ----------
        table : Table
            La table où ajouter le joueur
        joueur : Joueur
            Joueur à ajouter
        """
        table.ajouter_joueur(joueur)
        joueur.rejoindre_table(table)

    @log
    def retirer_joueur(self, table: Table, joueur: Joueur) -> None:
        """
        Retire un joueur d’une table.

        Paramètres
        ----------
        table : Table
            La table d’origine
        joueur : Joueur
            Joueur à retirer

        Exceptions
        ----------
        ValueError
            Si le joueur n’est pas sur la table
        """
        if joueur not in table.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} n'est pas sur la table.")
        joueur.quitter_table()

    @log
    def lister_tables(self) -> list[Table]:
        """
        Retourne toutes les tables existantes.

        Renvoie
        -------
        list[Table]
            Liste des tables actives
        """
        return self.tables

    @log
    def supprimer_table(self, table: Table) -> None:
        """
        Supprime une table et libère les joueurs qu’elle contient.

        Paramètres
        ----------
        table : Table
            La table à supprimer
        """
        for joueur in list(table.joueurs):
            joueur.quitter_table()
        self.tables.remove(table)
