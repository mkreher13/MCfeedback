# Last edited by Miriam Kreher on 04/23/2019
# OpenMC model of fuel pin & water cell

# Before running for the first time: 
#     export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from ModelOpts import *
from Channel import *
from Power import *
from Output import *
import numpy as np
import openmc.capi
import openmc
import copy
# import sys
import os
from time import time
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

results=Output(T, P)

########################################################################
#                      Iterations
########################################################################

Tf_change = 1.0
LP_change = 1.0
i = 0
window_counter = 1
n = 15

for i in range(0,n):
# while Tf_change > 1e-3:
	iteration = i
	Tf_old = copy.copy(T.Tf)
	LP_old = copy.copy(T.LinPower)
	T.htc(options, P.Tally)
	P.update(T.Tf, T.Tclad, T.Tbulk, T.Mesh, T.RhoBulk) #T.gap
	os.chdir('PinGeo')
	startTime = time()

	# For FullMC:
	# openmc.run()
	# runTime = time()-startTime
	# print("Runtime: ", runTime, "Iteration: ", iteration)

	#For single-batch MC:
	if i == 0:
		# print(T.Tf)
		openmc.capi.init()
		openmc.capi.simulation_init()
		openmc.capi.next_batch()
		t = openmc.capi.tallies

		# t1 = np.zeros(len(T.Mesh)-1)
		# t2 = np.zeros(len(T.Mesh)-1)
		# t3 = np.zeros(len(T.Mesh)-1)
		# t4 = np.zeros(len(T.Mesh)-1)
		# t5 = np.zeros(len(T.Mesh)-1)
		# t6 = np.zeros(len(T.Mesh)-1)
		# t7 = np.zeros(len(T.Mesh)-1)
		# t8 = np.zeros(len(T.Mesh)-1)
		# t9 = np.zeros(len(T.Mesh)-1)
		# t10 = np.zeros(len(T.Mesh)-1)
	else:
		openmc.capi.next_batch()

	#For windowed flushing
	# if window_counter == 1:
	# 	t1[:] = t[2].results[:,0,1]
	# elif window_counter == 2:
	# 	t2[:] = t[2].results[:,0,1]
	# elif window_counter == 3:
	# 	t3[:] = t[2].results[:,0,1]
	# elif window_counter == 4:
	# 	t4[:] = t[2].results[:,0,1]
	# elif window_counter == 5:
	# 	t5[:] = t[2].results[:,0,1]
	# elif window_counter == 6: 
	# 	t6[:] = t[2].results[:,0,1]
	# elif window_counter == 7: 
	# 	t7[:] = t[2].results[:,0,1]
	# elif window_counter == 8: 
	# 	t8[:] = t[2].results[:,0,1]
	# elif window_counter == 9:
	# 	t9[:] = t[2].results[:,0,1]
	# elif window_counter == 10:
	# 	t10[:] = t[2].results[:,0,1]


	t = openmc.capi.tallies
	# print(t[2].results[:,0,1])

	# P.power_factors(t)
	P.power_factors(t) #, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10)
	os.chdir('..')

	if i != 0:
		Tf_change = max(abs(T.Tf[:]-Tf_old[:])/Tf_old[:])
		LP_change = max(abs(T.LinPower[:]-LP_old[:])/LP_old[:])
		T.Tf_change.append(Tf_change)
		T.LP_change.append(LP_change)

	results.plotTemp(T.Tf, T.Tclad, T.Tw, T.Tbulk, T.Mesh, T.Tf_change, LP_change) #T.gap
	results.outfiles(i, n, T.Tf, T.Tclad, T.Tw, T.Tbulk, T.Mesh, T.Tf_change, T.LP_change, T.LinPower, P.Var, P.k, t)#t[2].results[:,0,1]), T.gap

	#For flushing tallies
	# t[2].reset()

	#For windowed flushing
	# if window_counter == 1:
	# 	window_counter = 2
	# elif window_counter == 2:
	# 	window_counter = 3
	# elif window_counter == 3:
	# 	window_counter = 4
	# elif window_counter == 4:
	# 	window_counter = 5
	# elif window_counter == 5:
	# 	window_counter = 1 #6
	# elif window_counter == 6:
	# 	window_counter = 7
	# elif window_counter == 7:
	# 	window_counter = 8
	# elif window_counter == 8:
	# 	window_counter = 9
	# elif window_counter == 9:
	# 	window_counter = 10
	# elif window_counter == 10:
	# 	window_counter = 1
	
	
	# runTime = time()-startTime
	# print("Runtime: ", runTime)
	

os.chdir('PinGeo')
# openmc.capi.simulation_finalize()
# openmc.capi.finalize()
os.chdir('..')
results.kfile.close()






# do I still need equivalent water density in grid spacer cells?
# simple, flush, windowed
# convergence criteria: ~1K
# python naming conventions PEP8


















