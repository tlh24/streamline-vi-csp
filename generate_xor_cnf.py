#!/usr/bin/env python3

import subprocess as sp
import argparse as ap
import tempfile
import numpy as np
import sys
import random
import os
import shutil

parser = ap.ArgumentParser()
parser.add_argument('--num_variables', type=int, default=5)
parser.add_argument('--xor_density', type=float, default=1)
parser.add_argument('--xor_num_vars', type=int, default=3)
parser.add_argument('--cnf_file_path', type=str, default='xor.cnf')
args = parser.parse_args()

assert args.cnf_file_path.endswith('.cnf'), f"Filename must end in .cnf: {args.cnf_file_path}"
assert not os.path.exists(args.cnf_file_path), f"File already exists: {args.cnf_file_path}"

from sympy.logic.boolalg import ITE, And, Xor, Or, Not
import sympy
from sympy.logic.boolalg import to_cnf

num_xors = int(args.num_variables * args.xor_density)

variables = sympy.symbols(','.join(map(str, range(1, args.num_variables+1))))
# In case num_variables=1, sympy.symbols returns a single Symbol rather than a tuple.
# We wrap it in a tuple so random.sample doesn't fail.
if isinstance(variables, sympy.Symbol):
    variables = (variables,)

xors = []
for _ in range(num_xors):
    xor_vars = random.sample(variables, args.xor_num_vars)
    for i in range(len(xor_vars)):
        if np.random.random() < 0.5:
            xor_vars[i] = Not(xor_vars[i])
    xor = Xor(*xor_vars)
    if np.random.random() < 0.5:
        xor = Not(xor)
    xors.append(xor)
formula = And(*xors)
cnf_formula = to_cnf(formula)

with open(args.cnf_file_path, 'w') as f:
    print('p cnf %d %d' % (args.num_variables, len(cnf_formula.args)), file=f)

    for clause in cnf_formula.args:
        for variable in clause.args:
            if isinstance(variable, sympy.Symbol):
                # The end=' ' argument replaces Python 2's trailing comma
                print(variable.name, end=' ', file=f)
            else:
                print('-%s' % (variable.args[0].name), end=' ', file=f)
        print('0', file=f)

print('Finished writing to', args.cnf_file_path)
