# OpenMC BEAVRS single pin geometry 
# Last edited by Miriam Rathbun on 02/05/2018

import numpy as np
import openmc

# Geometry plotting
plot = openmc.Plot()
plot.width = [1.25984, 1.25984]
plot.origin = [0., 0., 400]
plot.pixels = [1000, 1000]
#plot.basis = 'yz'

openmc.plot_inline(plot)

#openmc.run()