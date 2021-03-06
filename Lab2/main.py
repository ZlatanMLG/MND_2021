from random import randint
from pprint import pprint
import numpy as np
from math import sqrt
m = 8
roman = {(2, 3, 4): 1.72, (5, 6, 7): 2.13, (8, 9): 2.37, (10, 11): 2.54, (12, 13): 2.66, (14, 15, 16, 17): 2.8, (18, 19, 20): 2.96}
mat_sX = [-25, -5, -30, 45]
mat_sY = [(30 - 110) * 10, (20 - 110) * 10]
print("Задані Х:\n", mat_sX, "\nЗадані Y:\n", mat_sY, "\nНормована матриця планування експерименту:")
mat_X = [[-1, -1], [1, -1], [-1, 1]]


def start(m):
    global mat_serY
    mat_Y = [[randint(mat_sY[1], mat_sY[0]) for i in range(m)] for k in range(3)]
    print(mat_X, "\nМатриця згенерованих значень Y:")
    pprint(mat_Y)
    mat_serY = [sum(mat_Y[k1]) / m for k1 in range(3)]
    print("Середні значення Y:", mat_serY)
    mat_disY = [sum([((k1 - mat_serY[j]) ** 2) for k1 in mat_Y[j]]) / m for j in range(3)]
    print("Дисперсії в рядках:", mat_disY)
    vidhil = sqrt((2 * (2 * m - 2)) / (m * (m - 4)))
    mat_Fuv = [mat_disY[0] / mat_disY[1], mat_disY[2] / mat_disY[0], mat_disY[2] / mat_disY[1]]
    print("Обчислеенні значення Fuv: ", mat_Fuv)
    mat_Q = [mat_Fuv[i2] * ((m - 2) / m) for i2 in range(3)]
    print("Обчислеенні значення Quv: ", mat_Q)
    mat_R = [abs(mat_Q[i3] - 1) / vidhil for i3 in range(3)]
    print("Обчислеенні значення Ruv: ", mat_R)
    for i in roman.keys():
        if m in i:
            value = roman[i]
            break
        if m >= 21:
            print("Занадто велике значення М")
            exit()
    return max(mat_R) < value


if start(m):
    print("Однорідна")
    print("M = ", m)
while not start(m):
    m += 1
    print("Неоднорідна")
tran = [list(i) for i in zip(*mat_X)]
mx_mat = [sum(tran[i]) / 3 for i in range(2)]
mx1 = mx_mat[0]
mx2 = mx_mat[1]
my = sum(mat_serY) / 3
print("Нормовані коефіцієнти рівняння регресії:\nmx1, mx2: ", mx_mat, "\nmy:", my)
a1 = (tran[0][0] ** 2 + tran[0][1] ** 2 + tran[0][2] ** 2) / 3
a2 = (tran[0][0] * tran[1][0] + tran[0][1] * tran[1][1] + tran[0][2] * tran[1][2]) / 3
a3 = (tran[1][0] ** 2 + tran[1][1] ** 2 + tran[1][2] ** 2) / 3
ax1 = [(tran[i][0] * mat_serY[0] + tran[i][1] * mat_serY[1] + tran[i][2] * mat_serY[2]) / 3 for i in range(2)]
a11 = ax1[0]
a22 = ax1[1]
print("a1: ", a1, "\na2: ", a2, "\na3: ", a3, "\na11: ", a11, "\na22: ", a22)
znamen = np.linalg.det(np.array([[1, mx1, mx2], [mx1, a1, a2], [mx2, a2, a3]]))
b0 = np.linalg.det(np.array([[my, mx1, mx2], [a11, a1, a2], [a22, a2, a3]])) / znamen
b1 = np.linalg.det(np.array([[1, my, mx2], [mx1, a11, a2], [mx2, a22, a3]])) / znamen
b2 = np.linalg.det(np.array([[1, mx1, my], [mx1, a1, a11], [mx2, a2, a22]])) / znamen
perevirka = [b0 + b1 * tran[0][i] + b2 * tran[1][i] for i in range(3)]
print("Перевірка 1: ", perevirka)
d_x1 = abs(mat_sX[1] - mat_sX[0]) / 2
d_x2 = abs(mat_sX[3] - mat_sX[2]) / 2
x10 = (mat_sX[1] + mat_sX[0]) / 2
x20 = (mat_sX[3] + mat_sX[2]) / 2
print("Дельта x1: ", d_x1, "\nДельта x2: ", d_x2, "\nx10: ", x10, "\nx20: ", x20)
A0 = b0 - b1 * x10 / d_x1 - b2 * x20 / d_x2
A1 = b1 / d_x1
A2 = b2 / d_x2
print("a0: ", A0, "\na1: ", A1, "\na2: ", A2)
perevirka21 = A0 + A1 * -25 + A2 * -30
perevirka22 = A0 + A1 * -5 + A2 * -30
perevirka23 = A0 + A1 * -25 + A2 * 45
perevirka2 = [perevirka21, perevirka22, perevirka23]
print("Перевірка по рядкам 2: ", perevirka2)

