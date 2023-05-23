import math
from enum import Enum
import pygame as pg

ORANGE = (255, 150, 100)


class State(Enum):
    IDLE = 0
    FORWARD = 1
    TURNING = 2
    FINNISHING = 3


class Plot:
    scale = 200
    init_x = 50
    init_y = 50
    river_len = 800
    state = State.FORWARD

    def __init__(self, surface, w, r):
        self.surface = surface
        self.r = r * self.scale
        self.w = w * self.scale
        self.h = 2 * (math.sqrt(self.scale**2 - self.w**2)+self.r)
        self.degree = 0

        self.ul: tuple[float, float] = (self.init_x + self.h, self.init_y+ (self.scale-self.w))
        self.ur: tuple[float, float] = (self.init_x + self.h, self.init_y +self.scale)
        self.bl: tuple[float, float] = (self.init_x, self.init_y+(self.scale-self.w))
        self.br: tuple[float, float] = (self.init_x, self.init_y + +self.scale)

    def update(self):
        if self.state == State.FORWARD:
            if (
                self.br[0] + self.h / 2 + self.r
                >= self.init_x + self.river_len - self.scale
            ):
                # self.br = (
                #     self.init_x + self.river_len - self.scale - self.h / 2 - self.r,
                #     self.ur[1],
                # )
                # self.bl = (self.init_x + self.river_len - self.h / 2 - self.r, self.ul[1])
                # self.ur = (self.br[0] + self.h, self.ur[1])
                # self.ul = (self.bl[0] + self.h, self.ul[1])

                self.turning_point = (self.br[0] + self.h / 2, self.br[1])
                self.degree = 0
                self.state = State.TURNING
                return
            step = 1
            self.ul = (self.ul[0] + step, self.ul[1])
            self.ur = (self.ur[0] + step, self.ur[1])
            self.bl = (self.bl[0] + step, self.bl[1])
            self.br = (self.br[0] + step, self.br[1])
        elif self.state == State.TURNING:
            if self.degree >= math.pi / 2:
                self.state = State.FINNISHING
                return

            delta_rot = 0.001
            corner = (
                self.init_x + self.river_len - self.scale,
                self.init_y + self.scale,
            )

            self.turning_point = self._rotate_point(
                self.turning_point,
                corner,
                -delta_rot,
            )

            self._rotate_around(self.turning_point, delta_rot)
            self.degree += delta_rot

            dy = self.r * (math.sin(self.degree) - math.sin(self.degree - delta_rot))
            dx = self.r * (-math.cos(self.degree) + math.cos(self.degree - delta_rot))
            self._move(dx, dy)

            pg.draw.line(self.surface, (255, 0, 0), corner, self.turning_point)
            pg.draw.circle(self.surface, (255, 0, 0), self.turning_point, 5)
            pg.draw.line(
                self.surface,
                (0, 255, 0),
                (self.br[0], self.br[1]),
                (self.br[0], self.init_y),
            )

        elif self.state == State.FINNISHING:
            if self.ur[1] >= self.river_len:
                self.ul = (self.init_x + self.h, self.init_y)
                self.ur = (self.init_x + self.h, self.init_y + self.w)
                self.bl = (self.init_x, self.init_y)
                self.br = (self.init_x, self.init_y + self.w)
                self.degree = 0
                self.state = State.FORWARD
                return
            step = 1
            self.ul = (self.ul[0], self.ul[1] + step)
            self.ur = (self.ur[0], self.ur[1] + step)
            self.bl = (self.bl[0], self.bl[1] + step)
            self.br = (self.br[0], self.br[1] + step)

    def draw(self):
        pg.draw.polygon(self.surface, ORANGE, [self.bl, self.br, self.ur, self.ul])

        pg.draw.circle(
            self.surface,
            (0, 0, 0),
            ((self.ul[0] + self.bl[0]) / 2, (self.ul[1] + self.bl[1]) / 2),
            self.r,
        )
        pg.draw.circle(
            self.surface,
            (0, 0, 0),
            ((self.ur[0] + self.br[0]) / 2, (self.ur[1] + self.br[1]) / 2),
            self.r,
        )

        self.draw_river()

    def draw_river(self):
        pg.draw.line(
            self.surface,
            (255, 255, 255),
            (self.init_x, self.init_y),
            (self.init_x + self.river_len, self.init_y),
            width=2,
        )

        pg.draw.line(
            self.surface,
            (255, 255, 255),
            (self.init_x, self.init_y + self.scale),
            (self.init_x + self.river_len - self.scale, self.init_y + self.scale),
            width=2,
        )

        pg.draw.line(
            self.surface,
            (255, 255, 255),
            (self.init_x + self.river_len, self.init_y),
            (
                self.init_x + self.river_len,
                self.init_y + self.river_len,
            ),
            width=2,
        )

        pg.draw.line(
            self.surface,
            (255, 255, 255),
            (self.init_x + self.river_len - self.scale, self.init_y + self.scale),
            (
                self.init_x + self.river_len - self.scale,
                self.init_y + self.river_len,
            ),
            width=2,
        )

    def _rotate_point(self, p: tuple[float, float], o: tuple[float, float], theta):
        px = math.cos(theta) * (p[0] - o[0]) - math.sin(theta) * (p[1] - o[1]) + o[0]
        py = math.sin(theta) * (p[0] - o[0]) + math.cos(theta) * (p[1] - o[1]) + o[1]
        return (px, py)

    def _rotate_around(self, o: tuple[float, float], theta):
        self.ul = self._rotate_point(self.ul, o, theta)
        self.ur = self._rotate_point(self.ur, o, theta)
        self.bl = self._rotate_point(self.bl, o, theta)
        self.br = self._rotate_point(self.br, o, theta)

    def _move(self, dx, dy):
        self.ul = (self.ul[0] + dx, self.ul[1] + dy)
        self.ur = (self.ur[0] + dx, self.ur[1] + dy)
        self.bl = (self.bl[0] + dx, self.bl[1] + dy)
        self.br = (self.br[0] + dx, self.br[1] + dy)
