#!/usr/bin/python

import ase
import sys
import numpy as np
import ase.io

filename=sys.argv[1]
atoms=ase.io.read(filename,index=0,format='xyz')

# Set the Lattice Parameters information & PBC info
cell = [(9.856, 0.0, 0.0),
        (-3.6959999999999997,    6.4016597847745800,    0.0000000000000000),
        (0, 0, 40.0)]
atoms.set_cell(cell, scale_atoms=False, fix=None)
atoms.set_pbc((True, True, True))
#ase.io.write('origatoms.png', atoms, show_unit_cell=True)


# Replicate How many units in each direction and recenter them to the
# box
replicate=(6,6,1)
repeatatoms=atoms.repeat(replicate)
repeatatoms.center()

# Write out the replicated file in xyz format
#ase.io.write('repeatatoms-{0}.png'.format(replicate), repeatatoms, rotation='-73x', show_unit_cell=True)
ase.io.write('replicated-{0}.xyz'.format(replicate), repeatatoms)


