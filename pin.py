# Last edited by Miriam Rathbun on 11/23/2017
# OpenMC model of fuel pin & water cell

from thermal import *

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
T.var(options)
T.HTC(options, A, De)


# Next step: map out calculations with meshing (zMesh)























