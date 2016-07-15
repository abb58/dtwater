#!/usr/bin/python

import sys
import os
import numpy as np

n = 50

myfile=open('pva.lt','a')
    
mystring="""# This is a simple example showing how to build a long polymer
# (in this case, an simple PVA chain). I split the
# PVA polymer molecule into individual -CH2-, -CH-, -OH-, -H- units.
# 
# Abhishek Bagusetty
# The Johnson Group, University of Pittsburgh
# Date : July 14, 2016
#
# PVA - OPLS_AA force field
#


import "oplsaa.lt"        # load the "OPLSAA" force-field information
import "chohgroup.lt"     # load the definition of the  "CHOH" object
import "ch2group.lt"      # load the definition of the  "CH2" object
import "ch3group.lt"      # load the definition of the  "CH3" object for capping start
import "ch3endgroup.lt"   # load the definition of the  "CH3" object for capping end


PVA inherits OPLSAA {

  create_var {$mol}  # optional:force all monomers to share the same molecule-ID

  monomers  = new CH2 [%(i)d].rot(0,1,0,0).move(2.5066446,0,0)
  monomers1 = new CHOH [%(i)d].rot(0,1,0,0).move(2.5066446,0,0)

  # Cap the ends with united atom "CH3"
  monomers3 = new CH3 [1]
  monomers4 = new CH3END [1]

  # Now add a list of bonds connecting the carbon atoms together:
  # (Angles, dihedrals, impropers will be automatically added later.)

  write('Data Bond List') {
""" % {'i':n}
myfile.write(mystring)#.format(Cdist,Hdist))

count = 1
for i in range(n):
    myfile.write('    $bond:b{1}   $atom:monomers[{0}]/C $atom:monomers1[{0}]/C'.format(i,i+1,count)+"\n")
    count = count+1

for i in range(n):
    if(i<n-1):
        myfile.write('    $bond:b{2}   $atom:monomers1[{0}]/C $atom:monomers[{1}]/C'.format(i,(i+1),count)+"\n")
        count=count+1

#for i in range(n):
#    myfile.write('    $bond:b{1}   $atom:monomers1[{0}]/C $atom:monomers2[{0}]/O'.format(i,count)+"\n")
#    count = count+1

# Bonds for the caps
myfile.write('    $bond:b{0}   $atom:monomers1[{1}]/C $atom:monomers4[0]/C'.format(count, n-1)+"\n")
count = count+1
myfile.write('    $bond:b{0}   $atom:monomers[0]/C $atom:monomers3[0]/C'.format(count)+"\n")

    
myfile.write('  }'+"\n\n")
myfile.write('} # PVA'+"\n")

# Closing the file
myfile.close()

#=================================================================================================
# Cap the start of polymer with "CH3"

myfile=open('ch3group.lt','w')
mystring ="""import "oplsaa.lt"    # <-- defines the "OPLSAA" force field

CH3 inherits OPLSAA {

# atom-id  mol-id atom-type  charge     x                    y                   z
  write("Data Atoms") {
    $atom:C  $mol:... @atom:80   0.00  -1.253322300   0.0000000000000000   0.0000000000000000
    $atom:H1  $mol:... @atom:85  0.00  -1.253322300   0.6310438442242609   0.8924307629540046
    $atom:H2  $mol:... @atom:85  0.00  -1.253322300   0.6310438442242609  -0.8924307629540046
    $atom:H3  $mol:... @atom:85  0.00  -2.145753063  -0.6310438442242609   0.0000000000000000
  }

  # Now specify which pairs of atoms are bonded:
  write('Data Bond List') {
    $bond:CH1 $atom:C $atom:H1
    $bond:CH2 $atom:C $atom:H2
    $bond:CH3 $atom:C $atom:H3
  }
  
} # CH3

CH3.move(0,0.4431163,0)
"""
myfile.write(mystring)
myfile.close()

#=================================================================================================

# Cap the end of polymer with "CH3-end"

myfile=open('ch3endgroup.lt','w')
Cdist = 2.5066446*n
mystring ="""import "oplsaa.lt"    # <-- defines the "OPLSAA" force field

CH3END inherits OPLSAA {

  write("Data Atoms") {
    $atom:C   $mol:... @atom:80  0.00   %(i)f   0.000                 0.000
    $atom:H1  $mol:... @atom:85  0.00   %(i)f   0.6310438442242609    0.8924307629540046
    $atom:H2  $mol:... @atom:85  0.00   %(i)f   0.6310438442242609   -0.8924307629540046
    $atom:H3  $mol:... @atom:85  0.00   %(i)f  -0.6310438442242609    0.000 
  }

  # Now specify which pairs of atoms are bonded:
  write('Data Bond List') {
    $bond:CH1 $atom:C $atom:H1
    $bond:CH2 $atom:C $atom:H2
    $bond:CH3 $atom:C $atom:H3
  }
  
} # CH3END

CH3END.move(0,0.4431163,0)
""" % {'i':Cdist}
myfile.write(mystring)
myfile.close()

#=================================================================================================

myfile=open('ch2group.lt','w')

mystring="""import "oplsaa.lt"    # <-- defines the "OPLSAA" force field

CH2 inherits OPLSAA {

  # atom-id  mol-id atom-type  charge    x        y                z
  write("Data Atoms") {
    $atom:C  $mol:...  @atom:81  0.00   0.000   0.000             0.000
    $atom:H1  $mol:... @atom:85  0.00   0.000   0.63104384422426  0.892430762954
    $atom:H2  $mol:... @atom:85  0.00   0.000   0.63104384422426  -0.892430762954
  }

  # Now specify which pairs of atoms are bonded:
  write('Data Bond List') {
    $bond:CH1 $atom:C $atom:H1
    $bond:CH2 $atom:C $atom:H2
  }

} # CH2

CH2.move(0,0.4431163,0)
"""
myfile.write(mystring)
myfile.close()

#=================================================================================================

myfile=open('chohgroup.lt','w')

mystring="""import "oplsaa.lt"    # <-- defines the "OPLSAA" force field

CHOH inherits OPLSAA {

  # atom-id  mol-id atom-type  charge    x           y                z
  write("Data Atoms") {
    $atom:C  $mol:... @atom:100  0.00   1.2533222   0.000              0.000
    $atom:H1 $mol:... @atom:85   0.00   1.2533222  +0.73104384422426  -0.692430762954
    $atom:O  $mol:... @atom:96   0.00   1.2533222  +0.831043844      +0.792430762954
    $atom:H2 $mol:... @atom:97   0.00   1.8370222  +0.831043844      +0.792430762954
  }

  # Now specify which pairs of atoms are bonded:
  write('Data Bond List') {
    $bond:CH1 $atom:C $atom:H1
    $bond:CO  $atom:C $atom:O
    $bond:OH2 $atom:O $atom:H2
  }

} # CHOH

CHOH.move(0,0.9431163,0)
"""
myfile.write(mystring)
myfile.close()

#=================================================================================================

myfile=open('system.lt','w')
mystring="""import "pva.lt"  # Defines the "Alkane50" molecule

polymer = new PVA

# Specify the size of the world the polymer lives in:
write_once("Data Boundary") {
  0.0  800.0  xlo xhi
  0.0  800.0  ylo yhi
  0.0  800.0  zlo zhi
}
"""
myfile.write(mystring)
myfile.close()
#=================================================================================================
