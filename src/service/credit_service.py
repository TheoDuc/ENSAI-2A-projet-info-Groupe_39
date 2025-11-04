from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class CreditService:
    """
    Service métier pour la gestion des crédits des joueurs pendant une manche.
    - Les crédits temporaires sont utilisés pour ne pas impacter directement la base.
    """

    dao = JoueurDao()
    temp_credits: dict[int, int] = {}

    @log
    def initialiser_joueurs(self, joueurs: list[Joueur]) -> None:
        """
        Initialise les crédits temporaires pour la manche.

        Paramètres
        ----------
        joueurs : list[Joueur]
            Joueurs participant à la manche
        """
        self.temp_credits = {j.id_joueur: j.credit for j in joueurs}

    @log
    def crediter(self, joueur: Joueur, montant: int) -> None:
        """
        Ajoute des crédits à un joueur (temporaire).

        Paramètres
        ----------
        joueur : Joueur
            Joueur à créditer
        montant : int
            Montant à créditer

        Exceptions
        ----------
        ValueError
            Si le montant est <= 0
        """
        if montant <= 0:
            raise ValueError("Le montant à créditer doit être positif.")
        self.temp_credits[joueur.id_joueur] += montant

    @log
    def debiter(self, joueur: Joueur, montant: int) -> None:
        """
        Retire des crédits à un joueur (temporaire).

        Paramètres
        ----------
        joueur : Joueur
            Joueur à débiter
        montant : int
            Montant à retirer

        Exceptions
        ----------
        ValueError
            Si le montant est <= 0 ou si le joueur n’a pas assez de crédits
        """
        if montant <= 0:
            raise ValueError("Le montant à débiter doit être positif.")
        if self.temp_credits[joueur.id_joueur] < montant:
            raise ValueError(f"{joueur.pseudo} n’a pas assez de crédits pour miser {montant}.")
        self.temp_credits[joueur.id_joueur] -= montant

    @log
    def solde_temporaire(self, joueur: Joueur) -> int:
        """
        Retourne le solde temporaire d’un joueur pendant la manche.

        Paramètres
        ----------
        joueur : Joueur
            Joueur concerné

        Renvoie
        -------
        int
            Crédit temporaire
        """
        return self.temp_credits.get(joueur.id_joueur, 0)

    @log
    def finaliser_credits(self) -> None:
        """
        Met à jour les crédits réels des joueurs en base après la manche.
        """
        for id_joueur, credit_final in self.temp_credits.items():
            joueur = self.dao.trouver_par_id(id_joueur)
            joueur._Joueur__credit = credit_final
            self.dao.modifier(joueur)
        self.temp_credits.clear()
