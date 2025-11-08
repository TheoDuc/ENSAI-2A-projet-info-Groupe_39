import pytest

from utils.reset_database import ResetDatabase
from dao.manche_dao import MancheDao
from business_object.joueur import Joueur
from business_object.info_manche import InfoManche
from business_object.manche import Manche

"""
class TestMancheDao:

    def creer_manche(self):
        # Crée une instance de Manche prête à être utilisée
        joueur1 = Joueur(1, "paul", 100, "fr")
        joueur2 = Joueur(2, "luc", 200, "us")
        info = InfoManche([joueur1, joueur2])
        manche = Manche(info, 10)
        manche.preflop()
        manche.flop()
        manche.turn()
        manche.river()
        return manche

    def test_creer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()

            # WHEN
            resultat = mancheDao.creer(manche)

            # THEN
            assert resultat is True

    def test_creer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            joueur1 = Joueur(1, "paul", 100, "fr")
            joueur2 = Joueur(2, "luc", 200, "us")
            info = InfoManche([joueur1, joueur2])
            manche = Manche(info, 10)
            manche.preflop()
            # on ne va PAS jusqu’à river -> cartes incomplètes

            # WHEN
            resultat = mancheDao.creer(manche)

            # THEN
            assert resultat is False


    def test_supprimer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()
            mancheDao.creer(manche)

            # WHEN
            resultat = mancheDao.supprimer(manche)

            # THEN
            assert resultat is True

    def test_supprimer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()

            # WHEN
            resultat = mancheDao.supprimer(manche)

            # THEN
            assert resultat is False
"""
