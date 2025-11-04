from business_object.table import Table
from business_object.joueur import Joueur

class TablesService:
    def __init__(self):
        self.tables = []  # juste en RAM

    def ajouter_un_joueur(self, joueur : Joueur):
        i = 0
        ok = False
        while i < len(self.tables) and ok == False:
            l = len(self.tables[i])
            if l < 6:
                self.tables[i].ajouter_joueur(joueur)
                ok = True
            i += 1
        if ok == False:
            nouvelle_table == Table(6, 1, [joueur])

    def retirer_un_joueur(self, joueur : Joueur):
        for i in range(len(self.tables)):
            for j in range(len(self.tables[i])):
                if self.tables[i].joueurs[j] == joueur :
                    self.tables[i].joueurs.pop(j)
                    if self.tables[i].joueurs == []:
                        self.tables.pop(i)