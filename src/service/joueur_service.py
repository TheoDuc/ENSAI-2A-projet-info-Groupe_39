from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.log_decorator import log


class JoueurService:
    """
    - CRUD (création, lecture, modification, suppression)
    - Gestion du rattachement à une table
    - Consultation des informations d’un joueur
    """

    dao = JoueurDao()

    # --- CRUD de base ---

    @log
    def creer(self, pseudo: str, credit: int, pays: str) -> Joueur | None:
        """
        Crée un joueur et l’enregistre dans la base de données.

        Paramètres
        ----------
        pseudo : str
            Nom du joueur
        credit : int
            Crédits initiaux
        pays : str
            Pays du joueur

        Renvoie
        -------
        Joueur | None
            Le joueur créé si succès, None si échec.
        """
        nouveau_joueur = Joueur(
            id_joueur=1,
            pseudo=pseudo,
            credit=credit,
            pays=pays,
        )
        return nouveau_joueur if self.dao.creer(nouveau_joueur) else None

        # En ram
        id_joueur = len(self.joueurs) + 1 if hasattr(self, "joueurs") else 1
        nouveau_joueur = Joueur(id_joueur=id_joueur, pseudo=pseudo, credit=credit, pays=pays)
        if not hasattr(self, "joueurs"):
            self.joueurs = []
        self.joueurs.append(nouveau_joueur)

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        """
        Recherche un joueur dans la base par son identifiant.

        Paramètres
        ----------
        id_joueur : int
            Identifiant du joueur à rechercher

        Renvoie
        -------
        Joueur | None
            Le joueur correspondant si trouvé, sinon None
        """
        return self.dao.trouver_par_id(id_joueur)

        # En ram
        for joueur in getattr(self, "joueurs", []):
            if joueur.id_joueur == id_joueur:
                return joueur

    @log
    def lister_tous(self) -> list[Joueur]:
        """
        Retourne la liste de tous les joueurs enregistrés en base.

        Renvoie
        -------
        list[Joueur]
            Liste des joueurs existants
        """
        return self.dao.lister_tous()

        # En ram
        return getattr(self, "joueurs", [])

    @log
    def modifier(self, joueur: Joueur) -> Joueur | None:
        """
        Met à jour les informations d’un joueur en base.

        Paramètres
        ----------
        joueur : Joueur
            Objet Joueur à mettre à jour

        Renvoie
        -------
        Joueur | None
            Le joueur modifié si succès, sinon None
        """
        return joueur if self.dao.modifier(joueur) else None

        # En ram
        for i, j in enumerate(getattr(self, "joueurs", [])):
            if j.id_joueur == joueur.id_joueur:
                self.joueurs[i] = joueur
                return joueur

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        """
        Supprime un joueur de la base de données.

        Paramètres
        ----------
        joueur : Joueur
            Objet Joueur à supprimer

        Renvoie
        -------
        bool
            True si suppression réussie, False sinon
        """
        return self.dao.supprimer(joueur)

        # En ram
        for i, j in enumerate(getattr(self, "joueurs", [])):
            if j.id_joueur == joueur.id_joueur:
                del self.joueurs[i]
                return True
