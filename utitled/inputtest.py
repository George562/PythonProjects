import numpy as np
import matplotlib.pyplot as plt
import pygame as pg

f = (lambda x, r: r * x * (1 - x))


def zoom(arr, x, y, k, increase=True):
    k = k if increase else 1 / k
    for i in range(len(arr)):
        arr[i] = (arr[i][0] - x) * k + x, (arr[i][1] - y) * k + y, *arr[i][2:]


N = 100
Dk = 0.01
maxK = 400

y = []
x = []

for k in range(maxK):
    k *= Dk
    test = [0.5]
    for i in range(1, N):
        test.append(f(test[-1], k))
    test = [round(i, 3) for i in test]
    if test[-1] == 0:
        y.append(0)
        x.append(k)
    else:
        done = False
        for i in set(test):
            if test.count(i) >= 10:
                y.append(i)
                x.append(k)
                done = True
        if not done:
            for i in set(test):
                y.append(i)
                x.append(k)
# y = np.array(y)
# x = np.array(x)
# plt.plot(x, y)

scw, sch = 1500, 800
sc = pg.display.set_mode((scw, sch))
s = len(y)
space = [(scw * x[i] / maxK / Dk, sch * (1 - y[i])) for i in range(s)]


def show():
    sc.fill((0, 0, 0))
    for i in range(s):
        pg.draw.circle(sc, (255, 255, 255), (int(space[i][0]), int(space[i][1])), 1)
    pg.display.update()


clock = pg.time.Clock()
show()
done = False
while not done:
    m_press = pg.mouse.get_pressed()
    if m_press[0]:
        zoom(space, *pg.mouse.get_pos(), 1.02)
        show()
    if m_press[2]:
        zoom(space, *pg.mouse.get_pos(), 1.02, False)
        show()
    if m_press[1]:
        relX, relY = pg.mouse.get_rel()
        space = list(map(lambda i: (i[0] + relX, i[1] + relY), space))
        show()
    pg.mouse.get_rel()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

# fig = plt.figure()
# ax = plt.axes(xlim=(0, N), ylim=(0, 1))
# line, = ax.plot([], [], lw=2)


# def init():
#     line.set_data([], [])
#     return line,
#
#
# def animate(k):
#     k = k * Dk
#     test = [0.5] * N
#     for i in range(1, N):
#         test[i] = f(test[i - 1], k)
#     print(k)
#     ax.set_ylim(min(test), max(test))
#     y = np.array(test)
#     x = np.arange(0, N, 1)
#     line.set_data(x, y)
#     return line,
#
#
# ani = FuncAnimation(fig, animate, frames=200,
#                     interval=500, blit=True, init_func=init)
#
plt.show()
