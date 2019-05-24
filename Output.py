#class to plot
# Last modified by Miriam Kreher on 11/06/2018

import copy
import numpy as np 
import matplotlib.pyplot as plt

class Output:

####################################################################
    def __init__(self, T, P):

        self.Tf_out = copy.copy(T.Tf)
        self.LP_out = copy.copy(T.LinPower)
        # self.Var_out = copy.copy(P.Var)
        self.kfile = open('output/k.txt', 'a')
        # self.t1 = open('output/tallies/t1.txt', 'a')
        # self.t2 = open('output/tallies/t2.txt', 'a')
        # self.t3 = open('output/tallies/t3.txt', 'a')
        # self.t4 = open('output/tallies/t4.txt', 'a')
        # self.t5 = open('output/tallies/t5.txt', 'a')
        # self.t6 = open('output/tallies/t6.txt', 'a')
        # self.t7 = open('output/tallies/t7.txt', 'a')
        # self.t8 = open('output/tallies/t8.txt', 'a')
        # self.t9 = open('output/tallies/t9.txt', 'a')
        # self.t10 = open('output/tallies/t10.txt', 'a')
        # self.t11 = open('output/tallies/t11.txt', 'a')
        # self.t12 = open('output/tallies/t12.txt', 'a')
        # self.t13 = open('output/tallies/t13.txt', 'a')
        # self.t14 = open('output/tallies/t14.txt', 'a')

#################################################################### 

    def plotTemp(self, Tf, Tclad, Tw, Tbulk, Mesh, Tf_change, LP_change): #Tgap
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
        # plt.ylim(top=0.035)
        # plt.ylim(bottom=0.0)
        plt.xlabel('Cycles')
        plt.ylabel('Max relative temperature change')
        plt.savefig('Tf_change.png')
        plt.clf()

        # plt.plot(LP_change, 'r')
        # plt.ylim(top=0.035)
        # plt.ylim(bottom=0.0)
        # plt.xlabel('Cycles')
        # plt.ylabel('Max relative linear power change')
        # plt.savefig('LP_change.png')
        # plt.clf()

        # plt.plot(self.k_out,'r')
        # plt.xlabel('Cycles')
        # plt.ylabel('k-effective')
        # plt.savefig('eigenvalue.png')
        # plt.clf()

#################################################################### 

    def outfiles(self, i, n, Tf, Tclad, Tw, Tbulk, Mesh, Tf_change, LP_change, LinPower, Var, k, tally): #Tgap

        self.Tf_out = np.vstack([self.Tf_out,Tf])
        np.savetxt("output/Tf.txt", np.transpose(self.Tf_out))
        self.LP_out = np.vstack([self.LP_out,LinPower])
        np.savetxt("output/LinPower.txt", np.transpose(self.LP_out))
        # self.Var_out = np.vstack([self.Var_out,Var])
        # np.savetxt("output/Var.txt", np.transpose(self.Var_out))
        # np.savetxt("output/Tf.txt", Tf)
        # np.savetxt("output/Tgap.txt", Tgap)
        np.savetxt("output/Tclad.txt", Tclad)
        np.savetxt("output/Tw.txt", Tw)
        np.savetxt("output/Tbulk.txt", Tbulk)
        np.savetxt("output/Mesh.txt", Mesh)
        np.savetxt("output/Tf_change.txt", Tf_change)
        np.savetxt("output/LP_change.txt", LP_change)


        # self.t1.write(str(tally[0])+' ')
        # self.t2.write(str(tally[1])+' ')
        # self.t3.write(str(tally[2])+' ')
        # self.t4.write(str(tally[3])+' ')
        # self.t5.write(str(tally[4])+' ')
        # self.t6.write(str(tally[5])+' ')
        # self.t7.write(str(tally[6])+' ')
        # self.t8.write(str(tally[7])+' ')
        # self.t9.write(str(tally[8])+' ')
        # self.t10.write(str(tally[9])+' ')
        # self.t11.write(str(tally[10])+' ')
        # self.t12.write(str(tally[11])+' ')
        # self.t13.write(str(tally[12])+' ')
        # self.t14.write(str(tally[13])+' ')

        # if i == n-1:
        #     self.t1.write('\n')
        #     self.t2.write('\n')
        #     self.t3.write('\n')
        #     self.t4.write('\n')
        #     self.t5.write('\n')
        #     self.t6.write('\n')
        #     self.t7.write('\n')
        #     self.t8.write('\n')
        #     self.t9.write('\n')
        #     self.t10.write('\n')
        #     self.t11.write('\n')
        #     self.t12.write('\n')
        #     self.t13.write('\n')
        #     self.t14.write('\n')







        # self.kfile.write(str(k)+"\n")

