# Last edited by Miriam Rathbun on 02/16/2018
# OpenMC model of fuel pin & water cell

# Before running for the first time: export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from ModelOpts import *
from Channel import *
from Power import *

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# Reading input parameters

options = ModelOpts()
options.read('input1.inp')


###############################################################################
#                      Calculations
###############################################################################

T=Channel()
T.Mesh(options)

# print("Vertical mesh:")
# print(T.Mesh)

P=Power()
P.Initial(options, T.Mesh)

T.HTC(options, P.LinPower)
P.Fuel(T.Tf)


























