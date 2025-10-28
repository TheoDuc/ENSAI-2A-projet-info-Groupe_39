from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from business_object.carte import Carte


class AbstractCombinaison(ABC):
    """
    Classe abstraite représentant une combinaison de cartes au poker.
    """

    def __init__(self, hauteur: str, kicker: Optional[Tuple[str, ...]] = None):
        if isinstance(hauteur, str):
            if hauteur not in Carte.VALEURS():
                raise ValueError(f"Hauteur invalide : {hauteur}")
        elif isinstance(hauteur, list):
            for h in hauteur:
                if h not in Carte.VALEURS():
                    raise ValueError(f"Hauteur invalide : {h}")
        else:
            raise ValueError("Hauteur doit être str ou list de str")

        self._hauteur = hauteur
        self._kicker = tuple(kicker) if kicker else ()

    @property
    def hauteur(self):
        return self._hauteur

    @property
    def kicker(self):
        return self._kicker

    # --- Méthodes abstraites ---
    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        pass

    # --- Comparaisons ---
    def _valeur_comparaison(self):
        # kickers en tuple
        kickers = self.kicker
        if isinstance(kickers, str):
            kickers = (kickers,)
        elif isinstance(kickers, list):
            kickers = tuple(kickers)

        # hauteur en tuple
        if isinstance(self.hauteur, str):
            hauteur_valeurs = (Carte.VALEURS().index(self.hauteur),)
        elif isinstance(self.hauteur, list):
            hauteur_valeurs = tuple(Carte.VALEURS().index(h) for h in self.hauteur)
        else:
            hauteur_valeurs = ()

        kickers_valeurs = tuple(Carte.VALEURS().index(k) for k in kickers)
        return (self.FORCE(), hauteur_valeurs, kickers_valeurs)

    def __eq__(self, other):
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() == other._valeur_comparaison()

    def __lt__(self, other):
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() < other._valeur_comparaison()

    # --- Représentations ---
    def __str__(self) -> str:
        if hasattr(self.hauteur, "__iter__") and not isinstance(self.hauteur, str):
            hauteur_str = " ".join(self.hauteur)
        else:
            hauteur_str = self.hauteur

        if self.kicker:
            return f"{self.__class__.__name__}({hauteur_str}, {self.kicker})"
        return f"{self.__class__.__name__} {hauteur_str}"

    def __repr__(self):
        return str(self)
