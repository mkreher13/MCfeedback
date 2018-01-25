# Class to perform thermal analysis and compute heat transfer coeficient
# Last modified by Miriam Rathbun on 12/12/2017

# Currently single-phase

import numpy as np 
import scipy.linalg
from thermalOpts import *
from iapws import IAPWS97


class Thermal():

###############################################################

	def __init__(self):
		self

###############################################################

	def var(self, options):

		self.zMesh = options.MeshPoints

###############################################################

	def HTC(self, options, A, De):

		P = options.Pressure
		Tin = options.Tin
		G = options.G
		L = options.length
		q = 17860.       #[W/m]

		subcooled_liq = IAPWS97(T=Tin, x=0)
		sat_liq = IAPWS97(P=P, x=0)
		sat_steam = IAPWS97(P=P, x=1)
		Tsat = sat_liq.T

		LinPower = np.zeros(self.zMesh)
		HeatFlux = np.zeros(self.zMesh)
		v = np.zeros(self.zMesh)
		self.enthalpy = np.zeros(self.zMesh)
		self.Tbulk = np.zeros(self.zMesh)
		self.Tw = np.zeros(self.zMesh)
		self.velocity = np.zeros(self.zMesh)
		LinPower[:] = q
		HeatFlux[:] = q/(2*np.pi*options.CladOR)
		self.Tw[:] = Tin # Initial guess



		# Heat transfer coefficients HTC_c (convection) & HTC_nb (nucleate boiling)
		# And converging to Tw (wall temperature)


		rho_in = IAPWS97(T=Tin, x=0).rho
		E = 1000.
		count = 1

		while E > 1E-3:

			P_sum = 0

			for i in range(0,self.zMesh):

				if i == 0:
					self.enthalpy[i-1] = subcooled_liq.h
					self.Tbulk[i-1] = Tin
					liq = subcooled_liq
				self.enthalpy[i] = LinPower[i]/1000*L/self.zMesh/(G*A) + self.enthalpy[i-1]
				self.Tbulk[i] = (self.enthalpy[i]-self.enthalpy[i-1])/(liq.cp) + self.Tbulk[i-1]

				liq = IAPWS97(T=self.Tbulk[i], x=0)
				stm = IAPWS97(T=self.Tbulk[i], x=1)
				Tw_water = IAPWS97(T=self.Tw[i], x=0)
				Re = G*De/liq.mu
				Pr = liq.cp*1000*liq.mu/liq.k
				Nu = 0.023*(Re**0.8)*(Pr**0.4)
				HTC_c = Nu*liq.k/De
				S = 1/(1+2.53E-6*Re**1.17)
				HTC_nb = S*0.00122*(liq.k**0.79)*((liq.cp*1000)**0.45)*(liq.rho**0.49)/(liq.sigma**0.5)/(liq.mu**0.29)/((stm.h-liq.h)**0.24)/(stm.rho**0.24)*(abs(self.Tw[i]-Tsat)**0.24)*(abs(Tw_water.P-sat_liq.P)**0.75)


				# Conservation equations
				rho_top = IAPWS97(T=self.Tbulk[i], x=0).rho
				rho_bot = IAPWS97(T=self.Tbulk[i-1], x=0).rho

				# Mass
				self.velocity[i] = G/rho_top

				# Energy - used to calculate enthaply, so no need to check. 
				#a = G*(self.enthalpy[i]-self.enthalpy[i-1])/(L/self.zMesh)
				#b = LinPower[i]/1000/A
				#print a-b

				# Momentum 
				acc = G**2*(1/rho_top-1/rho_bot)
				f = 0.184/527714.535424**0.2
				fric = f*G**2/De/2/((rho_top+rho_bot)/2)*L/self.zMesh
				grav = 9.81*(rho_top+rho_bot)/2*L/self.zMesh
				deltaP = acc + fric + grav
				P_sum = P_sum + deltaP
				

			rho_out = IAPWS97(T=self.Tbulk[self.zMesh-1], x=0).rho
			totalP = G**2*(1/rho_out-1/rho_in) + f*G**2/De/2/((rho_out+rho_in)/2)*L + 9.81*(rho_out+rho_in)/2*L 
			#print("Total pressure change between inlet/outlet: %f" % totalP)
			#print("Total pressure change by sum of increments: %f" % P_sum)
			#print("Velocity in the channel:")

			self.Tw_updated = (HeatFlux[:]+self.Tbulk[:]*HTC_c+Tsat*HTC_nb)/(HTC_c+HTC_nb)

			E = max(abs(self.Tw_updated[:]-self.Tw[:]))

			count = count+1

			self.Tw[:] = self.Tw_updated

		
		print("Temperature in the bulk liquid [C]:")
		print(self.Tbulk)
		print("Temperature at the wall [C]:")
		print(self.Tw)
		# print("Water velocity [m/s]:")
		# print(self.velocity)
		# print("Total pressure change between inlet/outlet: %f [Pa]" % P_sum)


		################
		# Fuel Temperature

		self.Tf = np.zeros(self.zMesh)
		kf = 2.4             #[W/m/K]
		kc = 17.             #[W/m/K]
		hg = 31000.          #[W/m^2/K]
		clad_or = 0.00475    #[m]
		clad_ir = 0.0040005  #[m]
		fuel_or = 0.0039218  #[m]
		gap_r = (clad_ir+fuel_or)/2 

		for i in range(0,self.zMesh):
			self.Tf[i] = self.Tw[i] + q/2.0/np.pi*(1.0/4.0/kf+1/gap_r/hg+1/kc*np.log(clad_or/clad_ir))

		print("Temperature in the fuel [C]:")
		print(self.Tf)




###############################################################
# Tw is found with eq.13-19 in Todreas


#end class