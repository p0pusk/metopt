from plot import Plot
import pygame as pg
import sys

FPS = 100
sc = pg.display.set_mode((1300, 700))
clock = pg.time.Clock()

plot = Plot(sc, 0.37, 1)

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

    sc.fill((0, 0, 0))
    plot.draw()
    plot.update()
    pg.display.update()
    clock.tick(FPS)
