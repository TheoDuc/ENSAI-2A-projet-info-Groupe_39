"""Implémentation de la classe Admin"""


class Admin:
    def __init__(self, id_admin: int):
        """Crée un administrateur avec un identifiant unique."""

        self._id_admin = id_admin

    @property
    def id_admin(self) -> int:
        """Retourne l'identifiant de l'administrateur."""
        return self._id_admin

    @id_admin.setter
    def id_admin(self, value: int):
        """Modifie l'identifiant de l'administrateur."""

        if not isinstance(value, int):
            raise TypeError("L'identifiant de l'admin doit être un entier.")

        self._id_admin = value

    # --- Méthodes principales ---
    def crediter(self, joueur, credits: int):
        """Ajoute des crédits à un joueur."""

        if credits <= 0:
            raise ValueError("Le nombre de crédits à ajouter doit être positif.")

        joueur.credits += credits

    def debiter(self, joueur, credits: int):
        """Retire des crédits à un joueur."""

        if credits <= 0:
            raise ValueError("Le nombre de crédits à retirer doit être positif.")

        if joueur.credits < credits:
            raise ValueError(
                "Le nombre de crédits à retirer doit être inférieur au nombre de crédits du joueur"
            )

        joueur.credits -= credits
