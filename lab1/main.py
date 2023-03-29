#!/usr/bin/env python

from types import MethodType
import interface
from problem import *
from simplex import *
from bruteforce import *
from examples import inf_loop as prb


if __name__ == "__main__":
    # interface.Interface().run()
    prb.solve(Problem.Method.SIMPLEX, verbose=True)
