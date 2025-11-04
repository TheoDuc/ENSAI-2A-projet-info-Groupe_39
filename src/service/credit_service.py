"""Service de gestion des crédits pendant une manche."""

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class CreditService:
    """
    Service de gestion des crédits des joueurs pendant une manche.

    Les opérations sont enregistrées temporairement dans un dictionnaire `temp_credits`
    pour éviter d’impacter la base tant que la manche n’est pas terminée.
    """

    def __init__(self):
        # Dictionnaire temporaire : {id_joueur: crédit_actuel_durant_la_manche}
        self.temp_credits = {}

    @log
    def initialiser_joueurs(self, joueurs: list[Joueur]) -> None:
        """Initialise le solde temporaire des joueurs pour la manche."""
        self.temp_credits = {j.id_joueur: j.credit for j in joueurs}

    @log
    def crediter(self, joueur: Joueur, montant: int) -> None:
        """Crédite un joueur (dans la manche uniquement)."""
        if montant <= 0:
            raise ValueError("Le montant à créditer doit être positif.")

        if joueur.id_joueur not in self.temp_credits:
            raise KeyError(f"Le joueur {joueur.pseudo} ne fait pas partis de la manche.")

        self.temp_credits[joueur.id_joueur] += montant

    @log
    def debiter(self, joueur: Joueur, montant: int) -> None:
        """Débite un joueur (dans la manche uniquement)."""
        if montant <= 0:
            raise ValueError("Le montant à débiter doit être positif.")

        if joueur.id_joueur not in self.temp_credits:
            raise KeyError(f"Le joueur {joueur.pseudo} ne fait pas partis de la manche.")

        if self.temp_credits[joueur.id_joueur] < montant:
            raise ValueError(f"{joueur.pseudo} n’a pas assez de crédits pour miser {montant}.")

        self.temp_credits[joueur.id_joueur] -= montant

    @log
    def solde_temporaire(self, joueur: Joueur) -> int:
        """Retourne le crédit temporaire d’un joueur pendant la manche."""
        return self.temp_credits.get(joueur.id_joueur, 0)

    @log
    def finaliser_credits(self) -> None:
        """
        Met à jour la base de données à la fin de la manche.
        Les crédits réels des joueurs sont remplacés par les valeurs finales de temp_credits.
        """
        dao = JoueurDao()

        for id_joueur, credit_final in self.temp_credits.items():
            joueur = dao.trouver_par_id(id_joueur)
            if joueur is None:
                raise ValueError(f"Joueur ID {id_joueur} introuvable dans la base de donnée.")
            joueur._Joueur__credit = credit_final  # mise à jour interne (propre au modèle)
            dao.modifier(joueur)
