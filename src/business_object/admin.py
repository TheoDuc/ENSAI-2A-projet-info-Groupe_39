"""Implémentation de la classe Admin"""

from business_object.joueur import Joueur


class Admin:
    def __init__(self, id_admin: int) -> "Admin":
        """
        Crée un administrateur avec un identifiant unique

        Paramètres
        ----------
        id_admin : int
            l'identifiant de l'administrateur

        Renvois
        -------
        Admin
            Instance de 'Admin'
        """

        if not isinstance(id_admin, int):
            raise TypeError(f"L'identifiant administrateur doit être un int : {type(id_admin)}")

        if id_admin < 1:
            raise ValueError(
                f"L'identifiant du joueur doit être un entier strictement positif : {id_admin}"
            )

        self.__id_admin = id_admin

    @property
    def id_admin(self) -> int:
        """Retourne l'identifiant de l'administrateur."""
        return self.__id_admin

    def crediter(self, joueur: Joueur, credits: int) -> None:
        """
        Ajoute des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de crédits à ajouter

        Renvois
        -------
        None
        """

        joueur.ajouter_credits(credits)

    def debiter(self, joueur: Joueur, credits: int) -> None:
        """
        Retire des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de crédits à retirer

        Renvois
        -------
        None
        """

        joueur.retirer_credits(credits)

    def set_credits(self, joueur: Joueur, credits: int) -> None:
        """
        Met les crédits d'un joueur à un certain niveau

        Paramètres
        ----------
        credits : int
            Nouvelle quantité de crédits du joueur

        Renvois
        -------
        None
        """

        joueur.retirer_credits(joueur.credit)
        joueur.ajouter_credits(credits)
