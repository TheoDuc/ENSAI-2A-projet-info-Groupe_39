"""Implémentation de la classe Table"""


class Table:
    """Modélisation d'une table de jeu

    On definit une table par :
    - le nombre maximum de joueurs
    - la grosse blind
    - le mode de jeu (0 = texas holdem, 1 = omaha)
    - la liste des joueurs
    - les cartes sur la table

    """

    def __init__(self, joueur_max=int, grosse_blind=int, mode_jeu=int, joueurs=list):
        self.__joueur_max = joueur_max
        self.__grosse_blind = grosse_blind
        self.__mode_jeu = mode_jeu
        self.__joueurs = joueurs
        self.__cartes = []

    # creer une classe property pour joueur_max, grosse_blind, mode_jeu et joueurs
    @property
    def joueur_max(self):
        return self.__joueur_max

    @property
    def grosse_blind(self):
        return self.__grosse_blind

    @property
    def mode_jeu(self):
        return self.__mode_jeu

    @property
    def joueurs(self):
        return self.__joueurs

    """
    __len__():int
    methodes: ajouter_joueur(joueur: Joueur) 
    retirer_joueur(indice:int) 
    mettre_gross_blind(credit:int)
    rotation_dealer()
    lancer_manche()
    que nous allons coder
    """

    def __len__(self) -> int:
        """Retourne le nombre de joueurs à la table"""
        return len(self.__joueurs)

    def ajouter_joueur(self, joueur) -> None:
        """Ajoute un joueur à la table"""
        if len(self.__joueurs) < self.__joueur_max:
            self.__joueurs.append(joueur)
        else:
            raise ValueError("Nombre maximum de joueurs atteint")

    def retirer_joueur(self, indice: int) -> None:
        """Retire un joueur de la table et le renvoie"""
        if 0 <= indice < len(self.__joueurs):
            return self.__joueurs.pop(indice)
        else:
            raise IndexError("Indice de joueur incorrect")

    def mettre_grosse_blind(self, credit: int) -> None:
        """
        Déduit la valeur de la grosse blind du crédit du joueur et l'ajoute au pot.

        Args:
            credit (int): le montant qui permettrait de mettre à joueur la grosse blind
            si le crédit est insuffisant, le joueur est éliminé de la partie
            sinon le montant de la grosse blind est déduit du crédit du joueur
        Raises:
            ValueError: si le crédit est insuffisant pour mettre la grosse blind
            la valeur credit sert a incrementer augmenter la mise du pot
            la valeur de la grosse blind devient l'ancienne grosse blind + le credit
        """
        if credit < self.__grosse_blind:
            raise ValueError("Crédit insuffisant pour mettre la grosse blind")
        # A implementer
        else:
            self.joueurs[1].credit -= self.__grosse_blind
            self.__grosse_blind += credit

    def rotation_dealer(self) -> None:
        dealer = self.retirer_joueur(0)
        self.ajouter_joueur(dealer)

    def lancer_manche(self) -> None:
        """Lance une manche"""
        # A implementer
        pass
