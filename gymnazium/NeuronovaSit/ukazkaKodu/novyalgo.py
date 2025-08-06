import numpy as np
import random
class Algorithm:

    def tah(self, pole, hrac):
        body = self.vytvor_body(len(pole))
        for y in range(len(pole)):
            for x in range(len(pole[0])):
                if pole[y][x] ==0:
                    rady = [[],[],[],[]]
                    for z in range(9):
                        if y-4+z >= 0 and y-4+z <= len(pole)-1 and  x-4+z >= 0 and x-4+z <= len(pole)-1:
                            rady[0].append(pole[y-4+z][x-4+z])
                        else:
                            rady[0].append(-2)
                        if y -4+ z >= 0 and y -4+ z <= len(pole) - 1 and x  >= 0 and x <= len(pole) - 1:
                            rady[1].append(pole[y -4+ z][x])
                        else:
                            rady[1].append(-2)
                        if y+4 - z >= 0 and y +4- z <= len(pole) - 1 and x-4 + z >= 0 and x -4+ z <= len(pole) - 1:
                            rady[2].append(pole[y +4- z][x-4+z])
                        else:
                            rady[2].append(-2)
                        if y  >= 0 and y  <= len(pole) - 1 and x-4 + z >= 0 and x-4 + z <= len(pole) - 1:
                            rady[3].append(pole[y][x-4+z])
                        else:
                            rady[3].append(-2)
                    for rada in rady:
                        body[y][x]+=self.oboduj_radu(rada, hrac)
                else:
                    body[y][x] = -1000000000

        return self.vyber_nejlepsi_tah(body)

    def oboduj_radu(self,rada, hrac):

        zasebou = 0
        predtim = 0
        for j in range(4):
            if rada[5+j] == 1:
                if predtim == 1 or predtim == 0:
                    zasebou+=1
                    predtim = 1
                elif predtim == -1:
                    zasebou -=1

                    break
            elif rada[5+j] == -1:
                if predtim == -1 or predtim == 0:
                    zasebou += 1
                    predtim = -1
                elif predtim == 1:

                    zasebou -= 1
                    break
            elif rada[5 + j] == 0:
                break
            else:
                zasebou -= 1
                break

        for j in range(4):
            if rada[3-j] == 1:
                if predtim == 1 or predtim == 0:
                    zasebou+=1
                    predtim = 1
                elif predtim == -1:

                    zasebou -=1
                    break
            elif rada[3-j] == -1:
                if predtim == -1 or predtim == 0:
                    zasebou += 1
                    predtim = -1
                elif predtim == 1:

                    zasebou -= 1
                    break
            elif rada[3 - j] == 0:
                break
            else:
                zasebou -= 1
                break

        if predtim == hrac:
            return zasebou**3 + 1
        else:
            return zasebou ** 3

    def vytvor_body(self, velikost_pole):
        body = []
        for y in range(velikost_pole):
            pole = []
            for x in range(velikost_pole):
                pole.append(0)
            body.append(pole)
        return body
    def vyber_nejlepsi_tah(self, polebodu):
        maxcislo = np.amax(polebodu)
        vys = np.zeros((len(polebodu), len(polebodu)))
        #print(maxcislo)
        pocet = 0
        pozice = []
        for y in range(len(polebodu)):
            for x in range(len(polebodu)):
                if polebodu[y][x] == maxcislo:
                    pocet +=1
                    pozice.append([x, y])
        for y in range(len(polebodu)):
            for x in range(len(polebodu)):
                if polebodu[y][x] == maxcislo:
                    vys[y][x]=1/pocet
        vytez = random.choice(pozice)
        return vytez, vys
"""pol = []
for y in range(15):
    pol.append([])
    for x in range(15):
        pol[y].append(0)
pol[7][7] = 1
pol[8][8] = 1
pol[7][9] = 1
pol[6][8] = 1
algo = Algorithm()"""
#print(algo.tah(pol, True))