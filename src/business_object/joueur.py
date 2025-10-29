"""Implémentation de la classe Joueur"""


class Joueur:
    """Modélisation d'un joueur de poker"""

    def __init__(self, id_joueur: int, pseudo: str, credit: int, pays: str, table=None) -> "Joueur":
        """
        Instanciation d'un joueur (poker)

        Paramètres
        ----------
        id_joueur : int
            identifiant du joueur
        pseudo : str
            pseudo du joueur
        credit : int
            crédits que possède le joeuur
        pays : str
            pays du joueur
        actif : bool
            spécifie si le joueur est à une table ou non

        Renvois
        -------
        Joueur
            Instance de 'Joueur'
        """

        if not isinstance(id_joueur, int):
            raise TypeError(f"L'identifiant du joueur doit être un int : {type(id_joueur)}")
        if id_joueur < 1:
            raise ValueError(
                f"L'identifiant du joueur doit être un entier strictement positif : {id_joueur}"
            )

        if not isinstance(pseudo, str):
            raise TypeError(f"Le pseudo du joueur doit être un str : {type(pseudo)}")

        if not isinstance(credit, int):
            raise TypeError(f"Le crédit du joueur doit être un int : {type(credit)}")
        if credit < 0:
            raise ValueError(f"Le crédit du joueur doit être un entier positif : {credit}")

        if not isinstance(pays, str):
            raise TypeError(f"Le pays du joueur doit être un str : {type(pays)}")

        self.__id_joueur = id_joueur
        self.__pseudo = pseudo
        self.__credit = credit
        self.__pays = pays
        self.__table = table

    @property
    def id_joueur(self) -> int:
        """Retourne l'identifiant du joueur"""
        return self.__id_joueur

    @property
    def pseudo(self) -> str:
        """Retourne le pseudo du joueur"""
        return self.__pseudo

    @property
    def credit(self) -> int:
        """Retourne les crédits du joueur"""
        return self.__credit

    @property
    def pays(self) -> str:
        """Retourne le pays du joueur"""
        return self.__pays

    @property
    def table(self):
        """Retourne la table où se trouve le joueur"""
        return self.__table

    def __str__(self):
        """Permet d'afficher le pseudo et les crédits du joueur"""
        return f"{self.__pseudo} : {self.__credit} crédits"

    def __eq__(self, other) -> bool:
        """
        Vérifie l'égalité entre deux joueurs

        Paramètres
        ----------
        other : any
            objet comparée

        Renvois
        -------
        bool
            Vrai si l'identifiant des deux joueurs est le même
        """

        if not isinstance(other, Joueur):
            return False

        return self.__id_joueur == other.id_joueur

    def ajouter_credits(self, credits: int) -> None:
        """
        Ajoute des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de credits à ajouter

        Renvois
        -------
        None
        """

        if not isinstance(credits, int):
            raise TypeError(f"Les crédits doivent être de type int : {type(credits)}")

        if credits < 0:
            raise ValueError(f"Le nombre de crédits à ajouter doit être positif : {credits}")

        self.__credit += credits

    def retirer_credits(self, credits: int) -> int:
        """
        Retire des crédits à un joueur

        Paramètres
        ----------
        credits : int
            nombre de credits à retirer

        Renvois
        -------
        int
            Nombre de crédits possédés par le joueur
        """

        if not isinstance(credits, int):
            raise TypeError(f"Les crédits doivent être de type int : {type(credits)}")

        if credits < 0:
            raise ValueError(f"Le nombre de crédits à retirer doit être positif : {credits}")

        if credits > self.credit:
            raise ValueError(
                f"Le joueur {self.pseudo} a trop peu de crédits pour retirer {credits}: {self.credit}"
            )

        self.__credit -= credits
        return self.credit

    def rejoindre_table(self, table) -> None:
        """
        Associe le joueur à une table (si il n'en a pas déjà une)

        Paramètres
        ----------
        table : Table
            La table que le joueur rejoint

        Renvois
        -------
        None
        """

        from business_object.table import Table

        if self.table is not None:
            raise Exception(f"Le joueur {self.pseudo} est déjà à une table")

        if not isinstance(table, Table):
            raise TypeError(f"le paramètre table doit être de type Table : {type(table)}")

        table.ajouter_joueur(self)
        self.__table = table

    def quitter_table(self) -> None:
        """
        Retire le joueur de sa table si il en a une, et remplace son attribut table par None

        Paramètres
        ----------
        table : Table
            La table que le joueur rejoint

        Renvois
        -------
        None
        """

        if self.table is None:
            raise Exception(f"Le joueur {self.pseudo} n'est actuellement à aucune table")

        indice = indice = self.__table.joueurs.index(self)
        self.__table.retirer_joueur(indice)
        self.__table = None
