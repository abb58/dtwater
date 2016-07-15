#!/usr/bin/tclsh

package require topotools
topo readlammpsdata system.data full
mv system.data system-moltemplate.data
topo writelammpsdata system.data full
quit
