"""Implémentation de la classe TableService"""

from business_object.table import Table
from service.joueur_service import JoueurService
from service.manche_joueur_service import MancheJoueurService
from service.manche_service import MancheService
from utils.log_decorator import log


class TableService:
    """
    Service métier pour la gestion des tables de poker :
    - Création, suppression et consultation des tables
    - Gestion des joueurs à l’intérieur des tables
    - Gestion du déroulement des manches
    """

    __tables: list[Table] = []
    compteur_tables: int = 0

    def liste_tables(self) -> list[Table]:
        """Liste l'ensemble des tables disponibles"""
        return self.__tables

    def affichages_tables(self) -> list[str]:
        """Affichage de l'ensemble des tables créées"""
        return [str(table) for table in self.__tables]

    def table_par_numero(self, numero_table: int) -> Table:
        """
        Renvoie la table correspondant au numéro si elle existe

        Paramètres
        ----------
        numero_table : int
            le numéro de la table recherchée

        Renvois
        -------
        Table
            la table recherchée si elle existe

        Exceptions
        ----------
        ValueError
            si aucune table n'est trouvée avec ce numéro
        """

        for table in self.__tables:
            if table.numero_table == numero_table:
                return table

        raise ValueError(f"Aucune table existante ne porte le numéro {numero_table}")

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
        numero = self.compteur_tables

        table = Table(
            numero_table=numero,
            joueur_max=joueur_max,
            grosse_blind=grosse_blind,
            mode_jeu=mode_jeu,
        )

        self.__tables.append(table)
        return table

    @log
    def supprimer_table(self, numero_table: int) -> None:
        """
        Supprime une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table à supprimer

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)

        for joueur in list(table.joueurs):
            joueur.quitter_table()
        if table in self.tables:
            self.__tables.remove(table)

    @log
    def ajouter_joueur(self, numero_table: int, id_joueur: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où ajouter un joueur
        id_joueur : int
            l'identifiant du joueur à ajouter à la table

        Renvois
        -------
        None
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
        id_joueur : int
            l'identifiant du joueur à retirer de sa table

        Renvois
        -------
        None
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        joueur.quitter_table()

    @log
    def lancer_manche(self, numero_table: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où lancer la manche

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)

        table.nouvelle_manche()

    @log
    def terminer_manche(self, numero_table: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où lancer la manche

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)

        id_manche = MancheService().creer_manche(table.manche)
        MancheJoueurService().creer_manche_joueur(id_manche, table.manche.info)
        table.rotation_dealer()
