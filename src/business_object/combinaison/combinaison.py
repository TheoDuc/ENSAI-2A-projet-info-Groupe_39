from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Optional, Tuple

from business_object.carte import Carte


@total_ordering
class AbstractCombinaison(ABC):
    """Classe abstraite représentant une combinaison de cartes au poker"""

    def __init__(self, hauteur: str, kicker: Optional[Tuple[str, ...]] = None):
        if hauteur not in Carte.VALEURS():
            raise ValueError(f"Hauteur invalide : {hauteur}")
        self._hauteur = hauteur
        self._kicker = kicker or ()

    @property
    def hauteur(self) -> str:
        return self._hauteur

    @property
    def kicker(self) -> Tuple[str, ...]:
        return self._kicker

    # --- Méthodes abstraites ---
    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        """Force de la combinaison"""
        pass

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """Vérifie si cette combinaison est présente"""
        pass

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        """Construit la combinaison à partir d'une liste de cartes"""
        pass

    # --- Comparaisons ---
    def _valeur_comparaison(self):
        """Convertit hauteur et kicker en valeurs numériques pour comparaison"""
        return (
            self.FORCE(),
            Carte.VALEURS().index(self.hauteur),
            tuple(Carte.VALEURS().index(k) for k in self.kicker),
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return False
        return self._valeur_comparaison() == other._valeur_comparaison()

    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() < other._valeur_comparaison()

    # --- Représentations ---
    def __str__(self) -> str:
        if self.kicker:
            return f"{self.__class__.__name__}({self.hauteur}, {self.kicker})"
        return f"{self.__class__.__name__}({self.hauteur})"

    def __repr__(self) -> str:
        return str(self)
