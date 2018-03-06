# MCfeedback
Single-pin coupled Thermal-MC code to study feedback effects in Monte Carlo. 

Variable grid spacing:
Based on the grid spacer locations, a uniform mesh is inserted between spacings that are further apart than the prescribed maximum spacing value. 

Channel code:
PWR conditions, all subcooled boiling using a modified Chen correlation (Todreas & Kazimi).
Uses equivalent temperature model BE2 (Grandi, Smith, Xu, Rhodes "EFFECT OF CASMO-5 CROSS-SECTION DATA AND DOPPLER TEMPERATURE DEFINITIONS ON LWR REACTIVITY INITIATED ACCIDENTS").
Currently trying to create cell & edge consistency. Right now, the Tally has a 0 inserted at the bottom to make it a long as the mesh edge vectors, but Channel needs to be modified to use cells values where appropriate. 
Energy conservation. 

Power code:
Initially creates OpenMC geometry for fuel pin and surrounding water with multipole data. Each cell has its own temperature. 
Updates temperature in each cell and runs the OpenMC. 
Power tally is completed in Power and used in Channel. Note that this tally accounts for incoming neutron energy and fissioning isotope, and it assumes that all energy is locally deposited in the fuel.  Produces an arbitrarily large number, scaled down to conserve expected fuel pin power by a factor of 0.00015. (Right now, the Tally has a 0 inserted at the bottom to make it a long as the mesh edge vectors, but Channel needs to be modified to use cells values.)
Future work: run only one batch at a time. (insert source that says convergence is achieved this way)

Project context:
Exascale, fast running TH surrogate model. This serves as the initial conditions to figure out the best iteration before doing the expensive CFD. 
