# Last edited by Miriam Rathbun on 01/29/2018
# OpenMC model of fuel pin & water cell

# Before running for the first time: export PYTHONPATH=~/Desktop/MCFeedback/iapws:$PYTHONPATH

from thermal import *
from power import *

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# Reading input parameters

options = ThermalOpts()
options.read('input1.inp')


# Channel calculated parameters

A = options.Pitch**2-np.pi*options.CladOR**2
De = 4*A/(2*np.pi*options.CladOR)


###############################################################################
#                      Calculations
###############################################################################



T=Thermal()
T.Mesh(options)

P=Power()
P.Initial(options, T.Mesh)

T.HTC(options, A, De, P.LinPower)

























