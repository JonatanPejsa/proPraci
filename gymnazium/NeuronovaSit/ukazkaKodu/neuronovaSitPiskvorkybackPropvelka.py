import copy
import datasetcreatorvelky
import numpy as np
import math
import random
import pickle
import datetime
import time

class Vrstva:
    def __init__(self, pocet_vstupu, pocet_neuronu):
        self.vahy = 0.1*np.random.randn(pocet_vstupu, pocet_neuronu)
        self.biases = 0.1*np.random.randn(pocet_neuronu)
        self.poce_vstupu = pocet_vstupu  # Pokud budu chtít síť otestovat, tak ať vím kolik má vstupů

    def vypocitej(self, predchozi_vrstva):
        self.vypocet = np.dot(predchozi_vrstva, self.vahy) + self.biases
        return self.vypocet

    # ------------ Aktivace -------------------
    def softmax(self, vysledek_hodnoty):
        exponencialni_hodnoty = np.exp(vysledek_hodnoty - max(vysledek_hodnoty))
        soucet = exponencialni_hodnoty.sum()
        self.vysledek = np.round(exponencialni_hodnoty/soucet,6)
        return self.vysledek
    def relu(self, vysledek_hodnoty):
        self.vysledek = np.maximum(0.01*vysledek_hodnoty, vysledek_hodnoty)
        return self.vysledek
    def sigmoid(self, vysledek_hodnoty):
        self.vysledek = 1/(1 + np.exp(-vysledek_hodnoty))


class NeuronovaSit:
    def __init__(self, pocet_zadani, pocet_vrstev, pocet_neuronu_ve_vrstve):
        self.update_id()
        self.vrstvy = []
        self.vrstvy.append(Vrstva(pocet_zadani, pocet_neuronu_ve_vrstve[0]))
        for x in range(pocet_vrstev-1):
            self.vrstvy.append(Vrstva(pocet_neuronu_ve_vrstve[x], pocet_neuronu_ve_vrstve[x+1]))
    def update_id(self):
        self.id = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    def spocitej_s_relu_konec_softmax(self, zadani):
        if len(self.vrstvy)>1:

            self.vrstvy[0].relu(self.vrstvy[0].vypocitej(zadani))

            for x in range(len(self.vrstvy)-2):
                self.vrstvy[x+1].relu(self.vrstvy[x+1].vypocitej(self.vrstvy[x].vysledek))
            self.vrstvy[-1].softmax(self.vrstvy[-1].vypocitej(self.vrstvy[-2].vysledek))
            #self.vrstvy[-1].relu(self.vrstvy[-1].vypocitej(self.vrstvy[-2].vysledek))
        else:
            self.vrstvy[-1].softmax(self.vrstvy[-1].vypocitej(zadani))
        return self.vrstvy[-1].vysledek

    def spocitej_s_sigmoid(self, zadani):
        self.vrstvy[0].sigmoid(self.vrstvy[0].vypocitej(zadani))
        for x in range(len(self.vrstvy)-1):
            self.vrstvy[x+1].sigmoid(self.vrstvy[x+1].vypocitej(self.vrstvy[x].vysledek))
        return self.vrstvy[-1].vysledek

    def vypocitej_tah(self, zadani):
        vys  = self.spocitej_s_relu_konec_softmax(zadani)
        return np.argmax(vys)

    # ----------------------- ztráty -----------------------------------------------------------------------------------
    def loss_categorical_entropy(self, predikce, ocekavani):
        loss= 0
        for x in range(len(predikce)):
            loss += -(math.log(predikce[x])*ocekavani[x])
        return loss
    def moje_vlastni_loss(self, predikce, ocekavani):
        loss = []
        for x in range(len(predikce)):
            loss.append((predikce[x]-ocekavani[x])**2)
        return loss
    # ----------------------- ukladání a nahrávání dat  ----------------------------------------------------------------
    def uloz(self):
        data_vahy = [self.vrstvy[0].vahy.tolist()]
        data_biases = [self.vrstvy[0].biases.tolist()]
        for x in range(len(self.vrstvy) - 1):
            data_vahy.append(self.vrstvy[x + 1].vahy.tolist())
            data_biases.append(self.vrstvy[x + 1].biases.tolist())
        with open("data/"+str(self.id) + "vahy.txt", "wb") as f:  # Pickling
            pickle.dump(data_vahy, f)
            f.close()
        with open("data/"+str(self.id) + "biases.txt", "wb") as f:  # Pickling
            pickle.dump(data_biases, f)
            f.close()
    def nahraj(self, id):
        with open("data/"+str(id)+"vahy.txt", "rb") as f:  # Unpickling
            vahy = pickle.load(f)
            f.close()
        with open("data/"+str(id)+"biases.txt", "rb") as f:  # Unpickling
            biases = pickle.load(f)
            f.close()
        self.vrstvy = []
        for x in range(len(vahy)):
            self.vrstvy.append(Vrstva(0,0))
            self.vrstvy[x].vahy = np.array(vahy[x])
            self.vrstvy[x].biases = np.array(biases[x])
        self.update_id() # abych poznal od jakého sítě to je, ale nepřepsal jí když jí uložím znovu

    # ----------------------- mutace -----------------------------------------------------------------------------------
    def mutace_vrstev(self):
        for j in range(len(self.vrstvy)):
            vrstva = np.copy(self.vrstvy[j].vahy)
            mask = np.random.randint(0, 2, size=vrstva.shape).astype(bool)
            r = np.multiply(((random.randint(0,2000)-1000)/700+np.random.rand(*vrstva.shape)),vrstva)#* np.max(vrstva) 900

            vrstva[~mask] = r[~mask]
            self.vrstvy[j].vahy = vrstva
            self.update_id()


    def mutace_biases(self):
        for j in range(len(self.vrstvy)):
            vrstva = np.copy(self.vrstvy[j].biases)
            mask = np.random.randint(0, 10, size=vrstva.shape).astype(bool)
            r = 1*np.random.rand(*vrstva.shape) #* np.max(vrstva)
            vrstva[~mask] = r[~mask]
            self.vrstvy[j].biases = vrstva
            self.update_id()
    def spojeni_siti(self, sit):
        for j in range(len(self.vrstvy)):
            vrstva_vahy = np.copy(self.vrstvy[j].vahy)
            vrstva_vahy_sit = np.copy(sit.vrstvy[j].vahy)
            vrstva_biases = np.copy(self.vrstvy[j].biases)
            vrstva_biases_sit = np.copy(sit.vrstvy[j].biases)

            mask = np.random.randint(0, 2, size=vrstva_vahy.shape).astype(bool)
            mask2 = np.random.randint(0, 2, size=vrstva_biases.shape).astype(bool)

            vrstva_vahy = np.multiply(vrstva_vahy, mask)
            vrstva_vahy[~mask] = vrstva_vahy_sit[~mask]
            vrstva_biases = np.multiply(vrstva_biases, mask2)
            vrstva_biases[~mask2] = vrstva_biases_sit[~mask2]
            self.vrstvy[j].vahy = vrstva_vahy
            self.vrstvy[j].biases = vrstva_biases
            self.update_id()

    # ----------------------- zpatecni propagace -----------------------------------------------------------------------

    def back_propagation(self,zadani, ocekavani):
        pole_deriv_vahy = []
        pole_deriv_biases = []

        predikce = self.spocitej_s_relu_konec_softmax(zadani)

        loss= self.deriv_moje(predikce, ocekavani)

        #aktivace = self.deriv_Relu(self.vrstvy[-2].vysledek)
        aktivace2 = self.softmax_derivace(predikce)

        diagonal = np.diag(aktivace2)
        #print(aktivace2)
        #print(loss)

        predchozi = self.vrstvy[-2].vysledek
        konecna_deriv_vahy = []
        konecna_deriv_biases = [0]*len(loss)
        konecna_deriv_dalsi = [0]*len(predchozi)
        for y in range(len(predchozi)):
            konecna_deriv_vahy.append([])
            for x in range(len(loss)):
                konecna_deriv_vahy[y].append(predchozi[y]*diagonal[x]*loss[x])#predchozi[y]*aktivace[y]*loss[x] 2radky potom nebyly
                """for z in range(len(aktivace2)):
                    konecna_deriv_vahy[y][x] += predchozi[y]*aktivace2[x][z]*loss[z]""" #progtam bude mnohem rychlejší bez tohohle
                konecna_deriv_biases[x]= (diagonal[x]*loss[x])
                konecna_deriv_dalsi[y]+= (self.vrstvy[-1].vahy[y][x] * diagonal[x] *loss[x])

        pole_deriv_vahy.append(konecna_deriv_vahy)
        pole_deriv_biases.append(konecna_deriv_biases)


        for vrstva in range(len(self.vrstvy)-2):
            aktivace = self.deriv_Relu(self.vrstvy[-2-vrstva].vysledek)
            predchozi = self.vrstvy[-3-vrstva].vysledek
            konecna_deriv_vahy = []
            konecna_deriv_biases = [0] * len(konecna_deriv_dalsi)
            konecna_deriv_dalsi_prozatim = [0] * len(predchozi)
            for y in range(len(predchozi)):
                konecna_deriv_vahy.append([])
                for x in range(len(konecna_deriv_dalsi)):
                    konecna_deriv_vahy[y].append(predchozi[y] * aktivace[x] * konecna_deriv_dalsi[x])
                    konecna_deriv_biases[x] = (aktivace[x] * konecna_deriv_dalsi[x]) # TODO myslím si, že tam má být rovná se a ne přičítání
                    konecna_deriv_dalsi_prozatim[y] += (self.vrstvy[-2-vrstva].vahy[y][x] * aktivace[x] * konecna_deriv_dalsi[x])
            pole_deriv_vahy.append(konecna_deriv_vahy)
            pole_deriv_biases.append(konecna_deriv_biases)
            konecna_deriv_dalsi = konecna_deriv_dalsi_prozatim

        aktivace = self.deriv_Relu(self.vrstvy[0].vypocitej(zadani))
        predchozi = zadani

        konecna_deriv_vahy = []
        konecna_deriv_biases = [0] * len(konecna_deriv_dalsi)
        for y in range(len(predchozi)):
            konecna_deriv_vahy.append([])
            for x in range(len(konecna_deriv_dalsi)): # loss tu bylo predtim
                konecna_deriv_vahy[y].append(predchozi[y] * aktivace[x] * konecna_deriv_dalsi[x])
                konecna_deriv_biases[x] = (aktivace[x] * konecna_deriv_dalsi[x])
        pole_deriv_vahy.append(konecna_deriv_vahy)
        pole_deriv_biases.append(konecna_deriv_biases)

        return pole_deriv_vahy, pole_deriv_biases

    def gradient_descent(self, trenovaci_data, po_kolika, pocet_pokusu, alfa):


        for y in range(pocet_pokusu):
            if y%10000==0:
                self.uloz()
                self.update_id()
                print("ulozeno")
            print(round(y*100/pocet_pokusu,2))
            #print(self.vrstvy[0].vahy[0])
            data = self.vyber_nahodny_z_dat(trenovaci_data, po_kolika)
            data = trenovaci_data[y%len(data):y%len(data)+po_kolika]
            if y == len(trenovaci_data):
                random.shuffle(trenovaci_data)
            celkove_vahy, celkove_biases = [], []
            for c in range(len(self.vrstvy)):
                celkove_vahy.append(np.zeros_like(self.vrstvy[len(self.vrstvy)-1-c].vahy))
                celkove_biases.append(np.zeros_like(self.vrstvy[len(self.vrstvy)-1-c].biases))

            for j in data:
                vstup = j[0]  # np.array(j[0]).flatten()
                ocekavani = j[1]


                #print(self.vrstvy[0].vahy)
                vahy, biases = self.back_propagation(vstup, ocekavani)


                for i in range(len(self.vrstvy)):
                    celkove_vahy[i] = np.add(np.array(vahy[i])*alfa, celkove_vahy[i])
                    celkove_biases[i] = np.add(np.array(biases[i])*alfa, celkove_biases[i])


            for i in range(len(self.vrstvy)):
                celkove_vahy[i] = celkove_vahy[i] / po_kolika
                celkove_biases[i] = celkove_biases[i] /po_kolika

            for x in range(len(self.vrstvy)):
                self.vrstvy[x].vahy = np.add(self.vrstvy[x].vahy, celkove_vahy[len(self.vrstvy)-1-x])
                self.vrstvy[x].biases = np.add(self.vrstvy[x].biases, celkove_biases[len(self.vrstvy)-1-x])


        for j in trenovaci_data:
            vstup = j[0]


            print(j[1]) #print(np.argmax(j[1]))
            values = self.spocitej_s_relu_konec_softmax(vstup)
            print(values)
            #print(np.argmax(values))

    def vyber_nahodny_z_dat(self,trenovaci_data, pocet):
        data =[]
        for x in range(pocet):
            data.append(random.choice(trenovaci_data))
        return data
    def deriv_softmax(self, x, vysledek):
        I = np.eye(x.shape[0])

        return vysledek * (I - vysledek.T)
    def deriv_Relu(self, x):
        return np.where(x <= 0, 0.01, 1)

    def deriv_moje(self,ocekavani, predikce):

        loss = []
        for x in range(len(predikce)):
            loss.append(2*(predikce[x] - ocekavani[x]))
        return loss


    def softmax_derivace(self, vysledek):
        # Vypočítáme softmax
        s = vysledek
        # Vytvoříme diagonální matici softmax hodnot
        s_diag = np.diag(s)
        # Vypočítáme derivaci softmax
        derivace = s_diag - np.outer(s, s)
        return derivace

def main():
    input = 0.8
    sit = NeuronovaSit(1, 2, [2,2])

    #sit.nahraj("07.03.2024_18-10-07")



    print(f"{sit.vrstvy[0].vahy} {sit.vrstvy[1].vahy} ")
    print(f"{sit.vrstvy[0].biases} {sit.vrstvy[1].biases}")

    #sit.vrstvy[0].vahy[0][0] = 1
    vys =sit.spocitej_s_relu_konec_softmax([0.8])
    print(sit.vrstvy[0].vysledek)
    print("vpoho")
    #vys = sit.spocitej_s_sigmoid([input])

    #print(sit.back_propagation2(vys, [input/2,input/3],0.01))
    for x in range(2):
        vys = sit.spocitej_s_relu_konec_softmax([input])
        print(vys)
        sit.back_propagation2([input], [input/2,input/3], 0.01)

    vys = sit.spocitej_s_relu_konec_softmax([input])
    print(vys)

    #print(sit.softmax_grad(np.array([0.6,0.4])))

def hello():
    input = 0.8
    sit = NeuronovaSit(81, 3, [81,81,81])
    sit.nahraj("29.03.2024_18-31-48")
    #sit.gradient_descent([[[input],[1,0]]], 0, 100,0.1)
    #print(sit.deriv_softmax(np.array([0.2,0.2,0.6]),np.array([0.2,0.2,0.6])))
    #print(sit.softmax_derivace(np.array([0.2,0.2,0.3,0.3])))
    #print(sit.deriv_moje([0.2,0.2,0.6], [0.3,0.3,0.3]))
    #print(sit.vyber_nahodny_z_dat(data, 3))
    dataset = datasetcreatorvelky.dataset_z_algoritmu(9)
    #dataset=[dataset[0],dataset[1]]
    #print(dataset)
    print(sit.gradient_descent(dataset, 20, 1000000, 0.01))

    #print(sit.vrstvy[0].softmax(np.array([10000000000000000,2])))

    sit.uloz()
    #main()
def jou():
    sit = NeuronovaSit(81, 3, [81,81,81])
    pl = np.zeros((9, 9))
    pl[4][4]=1

    sit.nahraj("29.03.2024_10-45-02")
    sit.gradient_descent([[np.zeros((9, 9)).flatten(), pl.flatten()]], 1, 50, 0.2)
    sit.uloz()

def xd():
    sit = NeuronovaSit(5, 2,[500,10])
    timer = time.time()
    print(sit.gradient_descent([[[0.2,0.2,0.2,0.2,0.5], [1,0,0,0,0,0,0,0,0,0]]],1,10000,1))
    print(time.time()-timer)
if __name__ == "__main__":
    xd()