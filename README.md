# MCfeedback
Single-pin coupled Thermal-MC code to study feedback effects in Monte Carlo. 

Variable grid spacing:  
Based on the grid spacer locations, a uniform mesh is inserted between spacings that are further apart than the prescribed maximum spacing value. 

Mesh setup:  
At the edges: T, h, rho with average values in the cell
In the cell: Tally, LinearPower, HeatFlux

Channel code:  
PWR conditions, all subcooled boiling using a modified Chen correlation (Todreas & Kazimi). Uses equivalent temperature model BE2 (Grandi, Smith, Xu, Rhodes "EFFECT OF CASMO-5 CROSS-SECTION DATA AND DOPPLER TEMPERATURE DEFINITIONS ON LWR REACTIVITY INITIATED ACCIDENTS"). In a pin cell, the area is reduced to conserve water displacement.  
Energy conservation:

Power code:  
Initially creates OpenMC geometry for fuel pin and surrounding water with multipole data. Grids are represented by increased clad thickness to conserve water displacement. Each cell has its own temperature. 
Updates temperature in each cell and runs OpenMC.  
Power tally is completed in Power and used in Channel. Note that this tally accounts for incoming neutron energy and fissioning isotope, and it assumes that all energy is locally deposited in the fuel.  Produces an arbitrarily large number, scaled down to conserve expected fuel pin power of 66945.4 W.  

Run types:  
Regular, to show instability.  
Flush tallies.  
Windowed tally accumulation.  

Project context:  
Exascale, fast running TH surrogate model. This serves as the initial conditions to figure out the best iteration before doing the expensive CFD. 
