"""Implémentation de la classe JoueurDAO"""

import logging

from business_object.joueur import Joueur
from business_object.info_manche import InfoManche
from business_object.manche import Manche
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class MancheDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Manche de la base de données"""

    @log
    def creer(self, manche) -> bool:
        """Creation d'une manche dans la base de données

        Parameters
        ----------
        manche : Manche

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            logging.info(f"Valeurs envoyées : {manche.board.cartes}")
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO manche(carte1, carte2, carte3, carte4, carte5) "
                        " VALUES (%(carte1)s, %(carte2)s, %(carte3)s, %(carte4)s, %(carte5)s)"
                        " RETURNING id_manche;                                                ",
                        {
                            "carte1": str(manche.board.cartes[0]),
                            "carte2": str(manche.board.cartes[1]),
                            "carte3": str(manche.board.cartes[2]),
                            "carte4": str(manche.board.cartes[3]),
                            "carte5": str(manche.board.cartes[4])
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            created = True

        return created

    @log
    def supprimer(self, manche) -> bool:
        """Suppression d'une manche dans la base de données

        Parameters
        ----------
        manche : Manche
            manche à supprimer de la base de données

        Returns
        -------
            True si la manche a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer la manche de la bbd
                    cursor.execute(
                        "DELETE FROM manche        "          
                        "WHERE carte1=%(carte1)s and carte2=%(carte2)s and carte3=%(carte3)s and "
                        "carte4=%(carte4)s and carte5=%(carte5)s   ",
                        {
                        "carte1": str(manche.board.cartes[0]),
                        "carte2": str(manche.board.cartes[1]),
                        "carte3": str(manche.board.cartes[2]),
                        "carte4": str(manche.board.cartes[3]),
                        "carte5": str(manche.board.cartes[4]),
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0


manchedao = MancheDao()
joueur1 = Joueur(1, 'paul', 100, 'fr')
joueur2 = Joueur(1, 'paul2', 1002, 'fr2')
infomanche = InfoManche([joueur1, joueur2])
manche = Manche(infomanche, 5)
manche.preflop()
manche.flop()
manche.turn()
manche.river()
print(manchedao.creer(manche))
print(manchedao.supprimer(manche))

