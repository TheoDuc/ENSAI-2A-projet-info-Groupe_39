"""Implémentation de la classe Joueur"""


class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    credit : int
        crédits disponibles
    actif : bool
        indique si le joueur est actif
    pays : str
        pays du joueur
    age : int
        âge du joueur
    mail : str
        mail du joueur
    fan_pokemon : bool
        indique si le joueur est fan de Pokémon
    """

    def __init__(self, id_joueur: int, pseudo: str, credit: int, actif: bool, pays: str, age: int):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.credit = credit
        self.actif = actif
        self.pays = pays
        self.age = age
        self.mail = None
        self.fan_pokemon = False
        self.table = None  # Table à laquelle le joueur est éventuellement associé

    # --- Propriétés ---
    @property
    def id_joueur(self) -> int:
        return self._id_joueur

    @id_joueur.setter
    def id_joueur(self, value: int):
        self._id_joueur = value

    @property
    def pseudo(self) -> str:
        return self._pseudo

    @pseudo.setter
    def pseudo(self, value: str):
        self._pseudo = value

    @property
    def credit(self) -> int:
        return self._credit

    @credit.setter
    def credit(self, value: int):
        if value < 0:
            raise ValueError("Les crédits ne peuvent pas être négatifs.")
        self._credit = value

    @property
    def actif(self) -> bool:
        return self._actif

    @actif.setter
    def actif(self, value: bool):
        self._actif = value

    @property
    def pays(self) -> str:
        return self._pays

    @pays.setter
    def pays(self, value: str):
        self._pays = value

    # --- Méthodes métier ---
    def changer_pseudo(self, pseudo: str):
        """Change le pseudo du joueur"""
        self.pseudo = pseudo

    def changer_pays(self, pays: str):
        """Change le pays du joueur"""
        self.pays = pays

    def ajouter_credits(self, credits: int):
        """Ajoute des crédits au joueur"""
        if credits < 0:
            raise ValueError("Le nombre de crédits à ajouter doit être positif.")
        self.credit += credits

    def retirer_credits(self, credits: int) -> int:
        """Retire des crédits au joueur et retourne le nouveau solde"""
        if credits < 0:
            raise ValueError("Le nombre de crédits à retirer doit être positif.")
        if credits > self.credit:
            raise ValueError(
                "Le nombre de crédits à retirer doit être supérieur aux crédits possédés"
            )
        self.credit -= credits
        return self.credit

    def changer_statut(self):
        """Inverse le statut actif/inactif du joueur"""
        self.actif = not self.actif

    def rejoindre_table(self, table):
        """
        Associe le joueur à une table (si non déjà présent)
        et informe la table de l'arrivée du joueur.
        """
        if self.table is not None:
            raise ValueError(f"Le joueur {self.pseudo} est déjà à une table.")

        if not hasattr(table, "ajouter_joueur"):
            raise TypeError(
                "L'objet fourni n'est pas une table valide (méthode 'ajouter_joueur' manquante)."
            )

        self.table = table
        table.ajouter_joueur(self)

    def quitter_table(self):
        """
        Retire le joueur de la table actuelle, si présent.
        """
        if self.table is None:
            raise ValueError(f"Le joueur {self.pseudo} n'est actuellement à aucune table.")

        if hasattr(self.table, "retirer_joueur"):
            # On suppose que retirer_joueur() accepte un joueur directement
            try:
                self.table.retirer_joueur(self)
            except TypeError:
                # Si ta méthode prend un indice, il faut trouver l'indice correspondant
                if hasattr(self.table, "joueurs"):
                    indice = self.table.joueurs.index(self)
                    self.table.retirer_joueur(indice)
            finally:
                self.table = None
        else:
            self.table = None

    # --- Affichage et utilitaires ---
    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.age} ans, {self.credit} crédits, actif={self.actif})"

    def as_list(self) -> list:
        """Retourne les attributs principaux du joueur dans une liste"""
        return [self.pseudo, self.age, self.mail, self.fan_pokemon, self.pays, self.credit]
