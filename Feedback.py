# Last edited by Miriam Rathbun on 04/10/2018
# OpenMC model of fuel pin & water cell

# Before running for the first time: 
#     export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from ModelOpts import *
from Channel import *
from Power import *
from Output import *
import numpy as np
import openmc.capi
import copy
# import sys
import os
# from mpi4py import MPI

########################################################################
#                      Simulation Input File Parameters
########################################################################

# comm = MPI.COMM_WORLD

# size = comm.Get_size()
# rank = comm.Get_rank()
# print("hello world from process", rank, "of", size)

# args = sys.argv
# print(args)

# Reading input parameters

options = ModelOpts()
options.read('input1.inp')


########################################################################
#                      Problem Setup
########################################################################

T=Channel()
T.mesh(options)

P=Power()
P.initial(options, T.Mesh) #, int(args[1]))


########################################################################
#                      Iterations
########################################################################

Tf_change = 1.0
i = 0

# n = 2 #100
# for i in range(0,n):
while Tf_change > 1e-3:
	iteration = i
	Tf_old = copy.copy(T.Tf)
	T.htc(options, P.Tally)
	print("Fuel Temperature:")
	print(T.Tf)
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

	if i != 0:
		Tf_change = max(abs(T.Tf[:]-Tf_old[:])/Tf_old[:])
		T.Tf_change.append(Tf_change)
	i = i+1

os.chdir('PinGeo')
openmc.capi.simulation_finalize()
openmc.capi.finalize()
os.chdir('..')
# P.finalize()
results=Output()
results.plotTemp(T.Tf, T.Tgap, T.Tclad, T.Tw, T.Tbulk, T.Mesh, T.Tf_change)
results.outfiles(T.Tf, T.Tgap, T.Tclad, T.Tw, T.Tbulk, T.Mesh, T.Tf_change)



# do I still need equivalent water density in grid spacer cells?
# simple, flush, windowed
# convergence criteria: ~1K
# python naming conventions PEP8


















