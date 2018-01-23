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
		muf = 6.829e-5  #[J/kg]
		cpf = 8.976e3   #[J/kg/K]
		k = 2.163       #[W/m/K] Fuel, should it be the cladding since that's what the water is in contact with? 
		q = 17860       #[W/m]
		rhof = 613      #[kg/m3]
		rhog = 90.9     #[kg/m3]
		sigma = 0.00563 #[N/m]

		subcooled_liq = IAPWS97(T=Tin+273, x=0)
		sat_liq = IAPWS97(P=P, x=0)
		sat_steam = IAPWS97(P=P, x=1)
		Tsat = sat_liq.T-273


		LinPower = np.zeros(self.zMesh)
		HeatFlux = np.zeros(self.zMesh)
		v = np.zeros(self.zMesh)
		self.enthalpy = np.zeros(self.zMesh)
		self.Tbulk = np.zeros(self.zMesh)
		self.Tw = np.zeros(self.zMesh)
		self.HTC_nb = np.zeros(self.zMesh)
		LinPower[:] = q
		HeatFlux[:] = q/(2*np.pi*options.CladOR)
		self.Tw[:] = Tin # Initial guess



		# Heat transfer coefficients HTC_c (convection) & HTC_nb (nucleate boiling)
		# And converging to Tw (wall temperature)


		rho_in = IAPWS97(T=Tin+273, x=0).rho
		E = 1000
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

				liq = IAPWS97(T=self.Tbulk[i]+273, x=0)
				stm = IAPWS97(T=self.Tbulk[i]+273, x=1)
				Tw_water = IAPWS97(T=self.Tw[i]+273, x=0)
				Re = G*De/liq.mu
				Pr = liq.cp*1000*liq.mu/liq.k
				Nu = 0.0023*(Re**0.8)*(Pr**0.4)
				HTC_c = 0.023*(G*De/liq.mu)**0.8*Pr**0.4*liq.k/De
				S = 1/(1+2.53E-6*Re**1.17)
				self.HTC_nb[i] = S*0.00122*(liq.k**0.79)*((liq.cp*1000)**0.45)*(liq.rho**0.49)/(liq.sigma**0.5)/(liq.mu**0.29)/((stm.h-liq.h)**0.24)/(stm.rho**0.24)*(abs(self.Tw[i]-Tsat)**0.24)*(abs(Tw_water.P-sat_liq.P)**0.75)


				# Conservation equations

				# Energy
				a = G*(self.enthalpy[i]-self.enthalpy[i-1])/(L/self.zMesh)
				b = LinPower[i]/1000/A
				#print a-b

				# Momentum 
				rho_top = IAPWS97(T=self.Tbulk[i]+273, x=0).rho
				rho_bot = IAPWS97(T=self.Tbulk[i-1]+273, x=0).rho
				deltaP = G**2*(1/rho_top-1/rho_bot)
				P_sum = P_sum + deltaP
				

			rho_out = IAPWS97(T=self.Tbulk[self.zMesh-1]+273, x=0).rho
			totalP = G**2*(1/rho_out-1/rho_in)#*L
			#print("total pressure change with totalP:")
			#print totalP/(10**6)
			#print("total pressure change with deltaP:")
			#print P_sum/(10**6)
				
				



			self.Tw_updated = (HeatFlux[:]+self.Tbulk[:]*HTC_c+Tsat*self.HTC_nb[:])/(HTC_c+self.HTC_nb[:])

			E = max(abs(self.Tw_updated[:]-self.Tw[:]))

			count = count+1

			self.Tw[:] = self.Tw_updated

		
		print("Temperature at the wall:")
		print self.Tw
		print ("Temperature in the bulk liquid:")
		print self.Tbulk

			








###############################################################
# Tw is found with eq.13-19 in Todreas


#end class