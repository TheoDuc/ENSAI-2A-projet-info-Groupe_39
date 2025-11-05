import pytest

from utils.reset_database import ResetDatabase
from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao

class TestJoueurDao():

    def test_creer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueur1 = Joueur(1, 'paul', 100, 'fr')
            joueurDao = JoueurDao()

            # WHEN
            resultat = joueurDao.creer(joueur1)

            # THEN
            assert resultat == True

    def test_creer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueur1 = Joueur(1, 'paul', 100, 'fr')
            joueurDao = JoueurDao()

            # WHEN
            resultat1 = joueurDao.creer(joueur1)
            resultat2 = joueurDao.creer(joueur1)

            # THEN
            assert resultat1 == True
            assert resultat2 == False
            


