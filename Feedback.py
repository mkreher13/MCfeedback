# Last edited by Miriam Rathbun on 04/10/2018
# OpenMC model of fuel pin & water cell

# Before running for the first time: 
#     export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from ModelOpts import *
from Channel import *
from Power import *
from Plotter import *
import numpy as np
import openmc.capi
import os

########################################################################
#                      Simulation Input File Parameters
########################################################################

# Reading input parameters

options = ModelOpts()
options.read('input1.inp')


########################################################################
#                      Calculations
########################################################################

T=Channel()
T.mesh(options)

# print("Vertical mesh:")
# print(T.Mesh)

P=Power()
P.initial(options, T.Mesh)

n = 100
for i in range(0,n):
	T.htc(options, P.Tally)
	P.update(T.Tf, T.Tgap, T.Tclad, T.Tbulk, T.Mesh, T.RhoBulk)
	os.chdir('PinGeo')
	if i == 0:
		openmc.capi.init()
		openmc.capi.simulation_init()
		openmc.capi.next_batch()
	else:
		openmc.capi.next_batch()
	t = openmc.capi.tallies
	P.power_factors(t)
	os.chdir('..')

os.chdir('PinGeo')
openmc.capi.simulation_finalize()
openmc.capi.finalize()
os.chdir('..')
results=Plotter()
results.plotTemp(T.Tf, T.Tgap, T.Tclad, T.Tw, T.Tbulk, T.Mesh)



# do I still need equivalent water density in grid spacer cells?
# couple the HTC and Fuel, using the batch-by-batch MC
# convergence criteria: ~1K
# need to update power distribution 
# python naming conventions PEP8


























