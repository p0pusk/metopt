#!/usr/bin/env python

import interface
from problem import *
from simplex import *
from bruteforce import *
from examples import prb3 as prb


if __name__ == "__main__":
    # values = interface.Interface().get_data()
    prb.solve()
