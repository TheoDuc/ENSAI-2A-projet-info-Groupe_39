"""Implémentation de la classe Admin"""


class Admin:
    """Modélisation d'un administrateur dans le système de gestion de jeu"""

    def __init__(self, id_admin: int):
        """
        Instanciation d'un administrateur

        Paramètres
        ----------
        id_admin : int
            Identifiant unique de l'administrateur

        Renvois
        -------
        Admin
            Instance de 'Admin'
        """
        self._id_admin = id_admin

    # --- Propriété id_admin ---
    @property
    def id_admin(self) -> int:
        """
        Retourne l'identifiant de l'administrateur

        Renvois
        -------
        int
            Identifiant unique de l'administrateur
        """
        return self._id_admin

    # --- Méthodes principales ---
    def crediter(self, joueur, credits: int):
        """
        Ajoute des crédits à un joueur

        Paramètres
        ----------
        joueur : Joueur
            Instance du joueur à créditer
        credits : int
            Montant de crédits à ajouter

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Si le nombre de crédits à ajouter est inférieur ou égal à zéro
        """
        if credits <= 0:
            raise ValueError("Le nombre de crédits à ajouter doit être positif.")
        joueur.credits += credits

    def debiter(self, joueur, credits: int):
        """
        Retire des crédits à un joueur

        Paramètres
        ----------
        joueur : Joueur
            Instance du joueur à débiter
        credits : int
            Montant de crédits à retirer

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            Si le nombre de crédits à retirer est inférieur ou égal à zéro
            Si le joueur ne dispose pas d'assez de crédits pour effectuer l'opération
        """
        if credits <= 0:
            raise ValueError("Le nombre de crédits à retirer doit être positif.")
        if joueur.credits < credits:
            raise ValueError(
                "Le nombre de crédits à retirer doit être inférieur ou égal au nombre de crédits du joueur"
            )
        joueur.credits -= credits
