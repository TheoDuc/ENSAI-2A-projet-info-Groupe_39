"""Service de gestion des tables de poker."""

import logging

from business_object.joueur import Joueur
from business_object.table import Table
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class TableService:
    """Service de gestion des tables et de leurs joueurs."""

    def __init__(self):
        self.tables: list[Table] = []

    @log
    def creer_table(self, joueur_max: int, grosse_blind: int, mode_jeu: int = 1) -> Table:
        """Crée une nouvelle table et l’ajoute à la liste des tables."""
        table = Table(joueur_max=joueur_max, grosse_blind=grosse_blind, mode_jeu=mode_jeu)
        self.tables.append(table)
        logger.info(f"Nouvelle table créée (grosse blind = {grosse_blind}, max = {joueur_max})")
        return table

    @log
    def ajouter_joueur(self, table: Table, joueur: Joueur) -> None:
        """Ajoute un joueur à une table existante."""
        table.ajouter_joueur(joueur)
        joueur.rejoindre_table(table)

    @log
    def retirer_joueur(self, table: Table, joueur: Joueur) -> None:
        """Retire un joueur de la table."""
        if joueur not in table.joueurs:
            raise ValueError(f"Le joueur {joueur.pseudo} n'est pas sur la table.")
        joueur.quitter_table()

    @log
    def lister_tables(self) -> list[Table]:
        """Retourne la liste de toutes les tables actives."""
        return self.tables

    @log
    def supprimer_table(self, table: Table) -> None:
        """Supprime une table et libère les joueurs."""
        for joueur in list(table.joueurs):
            joueur.quitter_table()
        self.tables.remove(table)
        logger.info("Table supprimée avec succès.")
