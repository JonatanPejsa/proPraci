import pygame
import numpy as np
from neuronovaSit import NeuronovaSit
#from neuronovaSitPiskvorky3X3pokus2 import Vrstva
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
X = 630#930
Y = 630#930
hra_bezi = True
clock = pygame.time.Clock()
pole_spiritu = []

screen = pygame.display.set_mode((X, Y))
velikost_obrazku = 200#300
KRIZEK = pygame.transform.scale(pygame.image.load('obrazky/krizek.png').convert(),(velikost_obrazku,velikost_obrazku))
KOLECKO = pygame.transform.scale(pygame.image.load('obrazky/kolecko.png').convert(),(velikost_obrazku,velikost_obrazku))
PRAZDNE = pygame.transform.scale(pygame.image.load('obrazky/prazdne_pole.png'),(velikost_obrazku,velikost_obrazku))

class Ctverecek(pygame.sprite.Sprite):

    def __init__(self, pozice, image, x, y):
        super(Ctverecek, self).__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=pozice)
        self.velikost_obrazku = velikost_obrazku

    def zmena(self, hrac):
        if hrac:
            self.image = KRIZEK
        else:
            self.image = KOLECKO
def kontrola_vyteze(board):

    for row in board:
        if abs(sum(row)) == 3:
            return row[0]

    for col in range(3):
        if abs(sum(board[row][col] for row in range(3))) == 3:
            return board[0][col]

    if abs(sum(board[i][i] for i in range(3))) == 3:
        return board[0][0]
    if abs(sum(board[i][2-i] for i in range(3))) == 3:
        return board[0][2]

    if all(board[i][j] != 0 for i in range(3) for j in range(3)):
        return 2

    return 0
def legalni_krok(board, row, col):

    if board[row][col] != 0:
        return False

    return True
def hra():
    ai = NeuronovaSit(9,3,[9,9,9])
    ai.nahraj("18.03.2024_18-37-29")#06.03.2024_06-18-44, 04.03.2024_23-25-31  trol xd-> 16.03.2024_21-47-57 #17.03.2024_10-14-09 # nejlepsi 18.03.2024_18-37-29
    spusteno = True
    all_sprites_list = pygame.sprite.Group()
    pole_spiritu = []
    pos = (-100000, -1000000)
    hraci_pole =[]
    for y in range(3):
        pole_spiritu.append([])
        pol= []
        for x in range(3):
            pole = Ctverecek(((velikost_obrazku+15)*x+velikost_obrazku/2,(velikost_obrazku+15)*(y)+velikost_obrazku/2),PRAZDNE,x,y)
            pole_spiritu[y].append(pole)
            all_sprites_list.add(pole)
            pol.append(0)
        hraci_pole.append(pol)
    ai_board = np.array(hraci_pole)
    input = ai_board.flatten()
    vys = ai.vypocitej_tah(input)

    souradnice_x = vys % 3
    souradnice_y = vys // 3
    pole_spiritu[souradnice_y][souradnice_x].zmena(True)
    hraci_pole[souradnice_y][souradnice_x] = 1
    while(spusteno):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spusteno = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    hra()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

        clicked_sprites = [s for s in all_sprites_list if s.rect.collidepoint(pos)]
        for x in clicked_sprites:
            if legalni_krok(hraci_pole, x.y, x.x):
                hraci_pole[x.y][x.x] = -1
                x.zmena(False)
                
                pos = (-100000, -100000)
                ai_board = np.array(hraci_pole)
                input = ai_board.flatten()
                vys= ai.vypocitej_tah(input)

                souradnice_x = vys%3
                souradnice_y = vys//3
                print(vys)
                pole_spiritu[souradnice_y][souradnice_x].zmena(True)
                hraci_pole[souradnice_y][souradnice_x] = 1


        pressed_keys = pygame.key.get_pressed()
        all_sprites_list.update(pressed_keys)
        screen.fill((0, 0, 0))
        all_sprites_list.draw(screen)
        pygame.display.flip()

        clock.tick(60)

hra()