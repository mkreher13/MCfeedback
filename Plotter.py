#class to plot
# Last modified by Miriam Rathbun on 04/10/2018

import numpy as np 
import matplotlib.pyplot as plt

class Plotter:

####################################################################
    def __init__(self):
        self

#################################################################### 

    def plotTemp(self, Tf, Tgap, Tclad, Tw, Tbulk, Mesh):
        print("plotting")

        plt.plot(Tf,Mesh,'r')
        plt.plot(Tclad,Mesh,'g')
        plt.plot(Tw,Mesh,'c')
        plt.plot(Tbulk,Mesh,'b')
        plt.xlabel('T (K)')
        plt.ylabel('Position from start of active fuel (cm)')
        plt.legend(['Average Fuel Temp','Clad Temp','Wall Temp','Bulk Water Temp'])
        plt.savefig('T_results.png')