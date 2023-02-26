from typing import List
import numpy as np
import copy
from enum import Enum


class RestrictionType(Enum):
    eq = 0
    leq = -1
    geq = 1


class ObjectiveDirection(Enum):
    MIN = 1
    MAX = -1


class Problem:
    def __init__(
        self,
        dim: int,
        A,
        b,
        c,
        restrictions: List[RestrictionType] = [],
        x_restrictions: List[int] = [],
        obj_direction: ObjectiveDirection = ObjectiveDirection.MIN,
    ) -> None:
        self.dim = int(dim)
        self.A = A
        self.b = b
        self.c = c
        self.restrictions = restrictions
        self.x_restrictions = x_restrictions
        self.obj_direction = obj_direction

    def ToStandart():
        pass
