import numpy as np
import itertools
import novyalgo as algo
import random

def vytvor_dataset(velikost_pole):
    okolo = list(itertools.product([1, -1, 0], repeat=2))
    okolo.pop(-1)

    data_set = []
    for y in range(velikost_pole):
        for x in range(velikost_pole):
            pole = np.zeros((velikost_pole, velikost_pole))
            pole[y][x] = -1
            odpoved = np.zeros((velikost_pole, velikost_pole))
            nejde = 0

            if y == 0 or y == velikost_pole-1:
                if x == 0 or x == velikost_pole-1:
                    nejde = 5
                else:
                    nejde = 3
            elif x == 0 or x == velikost_pole-1:
                nejde = 3

            for i in okolo:
                if y - i[0] >= 0 and y - i[0] <= velikost_pole-1 and x - i[1] >= 0 and x - i[1] <= velikost_pole-1:
                    odpoved[y - i[0]][x - i[1]] = 1 / (8 - nejde)

            data_set.append([pole.flatten(), odpoved.flatten()])
    return data_set
#print(vytvor_dataset(10))
def dataset_z_algoritmu(velikost_pole):
    data_set = []
    algoritmus = algo.Algorithm()
    for i in range(velikost_pole):
        for j in range(velikost_pole):
            if not (j == int(velikost_pole-1)/2 and i ==int(velikost_pole-1)/2):
                vstupy = np.zeros((velikost_pole, velikost_pole))
                vstupy[i][j] = -1
                vstupy[int((velikost_pole - 1) / 2)][int((velikost_pole - 1) / 2)] = 1
                for z in range(5):
                    print(i, j, z)
                    tah = algoritmus.tah(vstupy, True)
                    data_set.append([vstupy.flatten(), tah[1].flatten()])
                    vstupy[tah[0][1]][tah[0][0]] = 1
                    tah2 = algoritmus.tah(vstupy, False)
                    vstupy[tah2[0][1]][tah2[0][0]] = -1


    for x in range(7):
        vstupy = np.zeros((velikost_pole, velikost_pole))
        vstupy[int((velikost_pole - 1) / 2)][int((velikost_pole - 1) / 2)] = 1
        tah2 = algoritmus.tah(vstupy, False)
        vstupy[tah2[0][1]][tah2[0][0]] = -1
        for z in range(10):
            tah = algoritmus.tah(vstupy, True)
            data_set.append([vstupy.flatten(), tah[1].flatten()])
            vstupy[tah[0][1]][tah[0][0]] = 1
            tah2 = algoritmus.tah(vstupy, False)
            vstupy[tah2[0][1]][tah2[0][0]] = -1

    vstupy = np.zeros((velikost_pole, velikost_pole))
    p = np.zeros((velikost_pole, velikost_pole))
    p[int((velikost_pole - 1) / 2)][int((velikost_pole - 1) / 2)] = 1
    data_set.append([vstupy.flatten(), p.flatten()])
    data_set.append([vstupy.flatten(), p.flatten()])
    data_set.append([vstupy.flatten(), p.flatten()])


    """for p in range(200):
        vstupy = np.zeros((velikost_pole, velikost_pole))
        vstupy[int((velikost_pole-1)/2)][int((velikost_pole-1)/2)] = 1

        x = random.randint(0,velikost_pole-1)
        y = random.randint(0,velikost_pole-1)
        while vstupy[y][x]!=0:
            x = random.randint(0, velikost_pole-1)
            y = random.randint(0, velikost_pole-1)
        vstupy[y][x] = -1
        for z in range(7):
            print(p, z)
            tah = algoritmus.tah(vstupy, True)
            data_set.append([vstupy.flatten(), tah[1].flatten()])
            vstupy[tah[0][1]][tah[0][0]] = 1
            if z%2==0:
                x = random.randint(0, velikost_pole-1)
                y = random.randint(0, velikost_pole-1)
                while vstupy[y][x] != 0:
                    x = random.randint(0, velikost_pole-1)
                    y = random.randint(0, velikost_pole-1)
                vstupy[y][x] = -1
            else:
                tah = algoritmus.tah(vstupy, False)
                vstupy[tah[0][1]][tah[0][0]] = -1"""

    for p in range(10):
        vstupy = np.zeros((velikost_pole, velikost_pole))
        vstupy[int((velikost_pole-1)/2)][int((velikost_pole-1)/2)] = 1

        x = random.randint(0,velikost_pole-1)
        y = random.randint(0,velikost_pole-1)
        while vstupy[y][x]!=0:
            x = random.randint(0, velikost_pole-1)
            y = random.randint(0, velikost_pole-1)
        vstupy[y][x] = -1
        for z in range(5):
            print(p, z)
            tah = algoritmus.tah(vstupy, True)
            data_set.append([vstupy.flatten(), tah[1].flatten()])
            vstupy[tah[0][1]][tah[0][0]] = 1
            x = random.randint(0, velikost_pole-1)
            y = random.randint(0, velikost_pole-1)
            while vstupy[y][x] != 0:
                x = random.randint(0, velikost_pole-1)
                y = random.randint(0, velikost_pole-1)
            vstupy[y][x] = -1

    print(data_set)
    return data_set
import numpy as np

def generate_random_array(velikost):
    arr = np.zeros((velikost, velikost))
    num_elements = int(0.01 * arr.size) + np.random.randint(int(0.49 * arr.size))
    indices = np.random.choice(arr.size, 2*num_elements, replace=False)
    np.put(arr, indices[:num_elements], 1)
    np.put(arr, indices[num_elements:], -1)
    return arr
def dataset_z_algoritmu_nahodny(velikost_pole, pocet):
    data_set = []
    algoritmus = algo.Algorithm()
    for x in range(pocet):
        print(x)
        vstup = generate_random_array(velikost_pole)
        tah = algoritmus.tah(vstup, True)
        data_set.append([vstup.flatten(), tah[1].flatten()])
    return data_set
#dataset_z_algoritmu(9)
#print(dataset_z_algoritmu_nahodny(9,40000))