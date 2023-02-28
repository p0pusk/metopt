#!/usr/bin/env python

import interface
from problem import *
from simplex import *
from bruteforce import *
from examples import prb5 as prb


if __name__ == "__main__":
    # values = interface.Interface().get_data()
    # print(initialize_simplex(prb.A, prb.b, prb.c))
    # prb.solve()
    splx = Simplex(prb.A, prb.b, prb.c)
    splx.print()
