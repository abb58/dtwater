#!/usr/bin/tclsh

package require topotools
topo readlammpsdata system.data full
animate write xyz system.xyz
quit
