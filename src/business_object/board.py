"""Implémentation de la classe Board"""

from business_object.liste_cartes import AbstractListeCartes


class Board(AbstractListeCartes):
    """Modélisation du board de poker"""

    def __eq__(self, other) -> bool:
        """
        Compare l'égalité entre deux listes de cartes

        Paramètres
        ----------
        other : any
            objet comparée

        Renvois
        -------
        bool
            Vrai si l'ordre des cartes et les cartes sont identiques.
            Le type des deux objets doit aussi être identique.
        """

        if type(self) is not type(other):
            return False

        if len(self) != len(other):
            return False

        for carte1, carte2 in self.cartes, other.cartes:
            if carte1 != carte2:
                return False

        return True
