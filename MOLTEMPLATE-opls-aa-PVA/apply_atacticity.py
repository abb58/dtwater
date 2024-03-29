#!/usr/bin/python

# Written by Abhishek Bagusetty to apply Atactic Condition
# to the polymer structure generated by moltemplae program
# especially for Poly(Vinyl Alchohol) polymer.
#
# Date : 2016, March 16
# Johnson Group, University of Pittsburgh

import random
import os
import sys

#============ PHASE-1 ====================
print('Phase-1 : Run vmd to generate xyz file for Phase 2')
os.system("vmd -dispdev text -e ./vmd-tcl-recenter-atoms.tcl")
filexyz=open('system.xyz','r')
filexyzout=open('system-temp.xyz','a')
N=filexyz.readline()
comment=filexyz.readline()
filexyzout.write(N)
filexyzout.write(comment)
for i in range(int(N)):
    field=filexyz.readline()
    id=int(field.split()[0])
    if id==1 or id==2 or id==5:
        filexyzout.write('{0} {1:10.12f} {2:10.12f} {3:10.12f}'.format('C',float(field.split()[1]), float(field.split()[2]), float(field.split()[3]))+"\n")
    elif id==3:
        filexyzout.write('{0} {1:10.12f} {2:10.12f} {3:10.12f}'.format('H',float(field.split()[1]), float(field.split()[2]), float(field.split()[3]))+"\n")
    else:
        filexyzout.write('{0} {1:10.12f} {2:10.12f} {3:10.12f}'.format('O',float(field.split()[1]), float(field.split()[2]), float(field.split()[3]))+"\n")

filexyzout.close()
filexyz.close()
os.remove('system.xyz')
os.rename('system-temp.xyz','system.xyz')
print('Phase-1 : COMPLETE !')


#============ PHASE-2 ====================
# Recenter all the atoms for the simulation box
print('Phase-2 : Started to recenter atoms')
import ase
import sys
import numpy as np
import ase.io

atoms=ase.io.read('system.xyz',index=0,format='xyz')

# Set the Lattice Parameters information & PBC info
cell = [(800.0, 0.0, 0.0),
        (0.0,  800.0, 0.0),
        (0.0,    0.0, 800.0)]
atoms.set_cell(cell, scale_atoms=False, fix=None)
atoms.set_pbc((True, True, True))
atoms.center()
ase.io.write('system-recenter.xyz', atoms)
print('Phase-2 : COMPLETE !')


#============ PHASE-3 ====================
# Apply atactic condition
print('Phase-3 : Atactic condition under play')
fileout=open('system-out.data','a')
natoms=0
natomtps=0

with open('system.data','r') as file:

    while True:
        line=file.readline()
        if "atoms" in line:
            natoms=int(line.split()[0])
        if "atom types" in line:
            natomtps=int(line.split()[0])

        fileout.write(line)
        if line.startswith('Atoms #'):
            break

    # Read the existing coordinates
    fileout.write('\n')
    file.readline() # Skip the empty line
    atomID,molID,atomtp,q,x,y,z=[],[],[],[],[],[],[]
    filexyz=open('system-recenter.xyz','r')
    filexyz.readline()  # N
    filexyz.readline()  # comment in the file
    for i in range(int(natoms)):
        list=file.readline()
        atomID.append(int(list.split()[0]))
        molID.append(int(list.split()[1]))
        atomtp.append(int(list.split()[2]))
        q.append(float(list.split()[3]))

        listxyz=filexyz.readline()
        x.append(float(listxyz.split()[1]))
        y.append(float(listxyz.split()[2]))
        z.append(float(listxyz.split()[3]))

    # Analyze and apply for tacticity
    for i in range(natoms):
        if atomtp[i]==5 and atomtp[i+1]==3:         # for -C- and -H- bonded to -O(-)-
            if atomtp[i+2]==4:                      # For O(-) bonded to -CH-
                invert=random.choice([False,True])
                if invert==True:
                    print('Sequence detected for flip atom ID {0}'.format(atomID[i]))
                    y[i+1]=(y[i+1]-1.7)
                    y[i+2]=(y[i+2]-1.7)

    # Write out the new coordinates to the outfile
    for i in range(int(natoms)):
        fileout.write('{0} {1} {2} {3:6.3f} {4:20.12f} {5:20.12f} {6:20.12f}'.format(atomID[i], molID[i], atomtp[i], q[i], x[i], y[i], z[i])+"\n")

    # Write out the remaining part of the file.
    lists=file.readlines()
    for i in range(len(lists)):
        fileout.write(lists[i])

    # Rename "system-out.data" to "system.data"
    os.rename("system.data", "system-old.data")
    os.rename("system-out.data", "system.data")

print('Phase-3 : COMPLETE !')


