# Last edited by Miriam Rathbun on 02/27/2018
# OpenMC model of fuel pin & water cell

# Before running for the first time: 
#     export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from ModelOpts import *
from Channel import *
from Power import *

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

T.htc(options, P.LinPower)
P.fuel(T.Tf, T.Tgap, T.Tclad)
# adjust water temperature and density
# latest openmc will find the density for you 
# water cells each need a new material bc setting density isn't the same 
#     as temp - full core might require a change in setup. Also need 
#     equivalent water density in grid spacer cells 
# couple the HTC and Fuel, using the batch-by-batch MC
# convergence criteria: ~1K
# need to update power distribution 
# python naming conventions PEP8


























