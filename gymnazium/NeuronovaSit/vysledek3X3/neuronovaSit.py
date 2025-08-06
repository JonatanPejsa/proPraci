import numpy as np
import math
import random
import pickle


class Vrstva:
    def __init__(self, pocet_vstupu, pocet_neuronu):
        self.vahy = 0.1*np.random.randn(pocet_vstupu, pocet_neuronu)
        self.biases = 0.1*np.random.randn(pocet_neuronu)
        self.poce_vstupu = pocet_vstupu # kdyz budu chtit sit otestovat tak at vim kolik ma vstupu

    def vypocitej(self, predchozi_vrstva):
        self.vypocet = np.dot(predchozi_vrstva, self.vahy) + self.biases
        return self.vypocet

    # ------------ Aktivace -------------------
    def softmax(self, vysledek_hodnoty):
        exponencialni_hodnoty = np.exp(vysledek_hodnoty-max(vysledek_hodnoty))
        soucet = exponencialni_hodnoty.sum()
        self.vysledek = np.round(exponencialni_hodnoty/soucet,3)
    def relu(self, vysledek_hodnoty):
        self.vysledek = np.maximum(0, vysledek_hodnoty)

    def sigmoid(self, vysledek_hodnoty):
        self.vysledek = 1/(1 + np.exp(-vysledek_hodnoty))


class NeuronovaSit:
    def __init__(self, pocet_zadani, pocet_vrstev, pocet_neuronu_ve_vrstve):
        
        self.vrstvy = []
        self.vrstvy.append(Vrstva(pocet_zadani, pocet_neuronu_ve_vrstve[0]))
        for x in range(pocet_vrstev-1):
            self.vrstvy.append(Vrstva(pocet_neuronu_ve_vrstve[x], pocet_neuronu_ve_vrstve[x+1]))
    
    def spocitej_s_relu_konec_softmax(self, zadani):
        self.vrstvy[0].relu(self.vrstvy[0].vypocitej(zadani))
        for x in range(len(self.vrstvy)-1):
            self.vrstvy[x+1].relu(self.vrstvy[x+1].vypocitej(self.vrstvy[x].vysledek))
        self.vrstvy[-1].softmax(self.vrstvy[-1].vysledek)
        return self.vrstvy[-1].vysledek

    def spocitej_s_sigmoid(self, zadani):
        self.vrstvy[0].sigmoid(self.vrstvy[0].vypocitej(zadani))
        for x in range(len(self.vrstvy)-1):
            self.vrstvy[x+1].sigmoid(self.vrstvy[x+1].vypocitej(self.vrstvy[x].vysledek))
        self.vrstvy[-1].softmax(self.vrstvy[-1].vysledek)
        return self.vrstvy[-1].vysledek

    def vypocitej_tah(self, zadani):
        vys  = self.spocitej_s_relu_konec_softmax(zadani)
        return np.argmax(vys)

   
    # ----------------------- nahrávání dat  ----------------------------------------------------------------
    
    def nahraj(self, id):
        with open("data/"+str(id)+"vahy.txt", "rb") as f:  # Unpickling
            vahy = pickle.load(f)
        with open("data/"+str(id)+"biases.txt", "rb") as f:  # Unpickling
            biases = pickle.load(f)
        self.vrstvy = []
        for x in range(len(vahy)):
            self.vrstvy.append(Vrstva(0,0))
            self.vrstvy[x].vahy = np.array(vahy[x])
            self.vrstvy[x].biases = np.array(biases[x])
       

    