#class to plot
# Last modified by Miriam Rathbun on 04/10/2018

import numpy as np 
import matplotlib.pyplot as plt

class Output:

####################################################################
    def __init__(self):
        self

#################################################################### 

    def plotTemp(self, Tf, Tgap, Tclad, Tw, Tbulk, Mesh, Tf_change):
        print("plotting")

        plt.plot(Tf,Mesh,'r')
        plt.plot(Tclad,Mesh,'g')
        plt.plot(Tw,Mesh,'c')
        plt.plot(Tbulk,Mesh,'b')
        plt.xlabel('T (K)')
        plt.ylabel('Position from start of active fuel (cm)')
        plt.legend(['Average Fuel Temp','Clad Temp','Wall Temp','Bulk Water Temp'])
        plt.savefig('T_results.png')
        plt.clf()

        plt.plot(Tf_change, 'r')
        plt.savefig('Tf_change.png')
        plt.clf()

#################################################################### 

    def outfiles(self, Tf, Tgap, Tclad, Tw, Tbulk, Mesh, Tf_change):
        
        np.savetxt("output/Tf.txt", Tf)
        np.savetxt("output/Tgap.txt", Tgap)
        np.savetxt("output/Tclad.txt", Tclad)
        np.savetxt("output/Tw.txt", Tw)
        np.savetxt("output/Tbulk.txt", Tbulk)
        np.savetxt("output/Mesh.txt", Mesh)
        np.savetxt("output/Tf_change.txt", Tf_change)
