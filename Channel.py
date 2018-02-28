# Class to perform thermal analysis and compute heat transfer coeficient
# Last modified by Miriam Rathbun on 02/27/2018

# Assumptions:
# subcooled boiling at wall
# modified Chen correlation (eq.13-19 in Todreas)

import math
import numpy as np 
import scipy.linalg
import matplotlib.pyplot as plt
from iapws import IAPWS97


class Channel():

########################################################################

	def __init__(self):
		self

########################################################################

	def mesh(self, opt):

		TempMesh = [0.]

		for i in range(0,len(opt.Spacing)):
			NextMeshPoint = TempMesh[len(TempMesh)-1] + opt.Spacing[i]
			TempMesh.append(NextMeshPoint)
		# print TempMesh

		self.Mesh = TempMesh

		for i in range(0,len(TempMesh)-1):
			if opt.Spacing[i] >= opt.MaxMesh:
				UnifStep = np.ceil((TempMesh[i+1]-TempMesh[i])/opt.MaxMesh)+2
				UnifMesh1 = np.linspace(TempMesh[i],TempMesh[i+1],UnifStep)
				UnifMesh2 = np.delete(UnifMesh1,0)
				UnifMesh3 = np.delete(UnifMesh2,len(UnifMesh2)-1)
				self.Mesh = sorted(np.insert(self.Mesh,0,UnifMesh3))

		x_axis = np.zeros(len(self.Mesh))
		plt.scatter(x_axis,self.Mesh, c = "b", marker = "_")
		plt.savefig('Mesh.png')
		# print self.Mesh

########################################################################

	def htc(self, opt, LinPower):

		L = (self.Mesh[len(self.Mesh)-1]-self.Mesh[0])/100 # Conversion to meters
		P = opt.Pressure
		Tin = opt.Tin
		G = opt.G
		A = opt.PinPitch**2-np.pi*opt.CladOR**2
		Area = np.full(len(self.Mesh),A)
		De_avg = 4*A/(2*np.pi*opt.CladOR+opt.PinPitch**2)
		# Assigning smaller area at grid spacer
		for j in range(0,len(opt.GridTop_z)):
			for i in range(0,len(self.Mesh)):
				if self.Mesh[i] > opt.GridBot_z[j] and self.Mesh[i] <= opt.GridTop_z[j]:
					# print self.Mesh[i]
					Area[i] = opt.GridPitch**2-np.pi*opt.CladOR**2
		# print Area
		De = 4*Area[:]/(2*np.pi*opt.CladOR+opt.PinPitch**2)


		subcooled_liq = IAPWS97(T=Tin, x=0)
		sat_liq = IAPWS97(P=P, x=0)
		sat_steam = IAPWS97(P=P, x=1)
		Tsat = sat_liq.T

		HeatFlux = np.zeros(len(self.Mesh))
		self.enthalpy = np.zeros(len(self.Mesh))
		self.Tbulk = np.zeros(len(self.Mesh))
		self.Tw = np.zeros(len(self.Mesh))
		self.Tw_updated = np.zeros(len(self.Mesh))
		self.velocity = np.zeros(len(self.Mesh))
		count = np.zeros(len(self.Mesh))
		HeatFlux[:] = LinPower[:]/(2*np.pi*opt.CladOR)



		# Heat transfer coefficients HTC_c (convection) & HTC_nb (nucleate boiling)

		P_sum = 0.

		for i in range(0,len(self.Mesh)):

			E = 1000.

			if i == 0:
				self.enthalpy[i] = subcooled_liq.h
				self.Tbulk[i] = Tin
				self.Tw[i] = Tin
			else:
				MeshStep = (self.Mesh[i]-self.Mesh[i-1])/100. # Converted to meters
				self.Tw[i] = self.Tw[i-1]
				self.enthalpy[i] = LinPower[i]/1000.*MeshStep/(G*Area[i]) + self.enthalpy[i-1]
				self.Tbulk[i] = (self.enthalpy[i]-self.enthalpy[i-1])/(liq.cp) + self.Tbulk[i-1]

			liq = IAPWS97(T=self.Tbulk[i], x=0)
			stm = IAPWS97(T=self.Tbulk[i], x=1)
			Re = G*De[i]/liq.mu
			Pr = liq.cp*1000.*liq.mu/liq.k
			Nu = 0.023*(Re**0.8)*(Pr**0.4)
			HTC_c = Nu*liq.k/De[i]
			S = 1/(1.+2.53E-6*Re**1.17)




			# Converging to Tw (wall temperature)
			while E > 1.E-3:
				Tw_water = IAPWS97(T=self.Tw[i], x=0)
				HTC_nb = S*0.00122*(liq.k**0.79)*((liq.cp*1000)**0.45)*(liq.rho**0.49)/(liq.sigma**0.5)/(liq.mu**0.29)/((stm.h-liq.h)**0.24)/(stm.rho**0.24)*(abs(self.Tw[i]-Tsat)**0.24)*(abs(Tw_water.P-P)**0.75)
				self.Tw_updated[i] = (HeatFlux[i]+self.Tbulk[i]*HTC_c+Tsat*HTC_nb)/(HTC_c+HTC_nb)
				E = abs(self.Tw_updated[i]-self.Tw[i])#/self.Tw_updated[i]
				self.Tw[i] = self.Tw_updated[i]
				count[i] = count[i]+1

			if i != 0:

				# Conservation equations
				rho_top = IAPWS97(T=self.Tbulk[i], x=0).rho
				rho_bot = IAPWS97(T=self.Tbulk[i-1], x=0).rho

				# Mass
				self.velocity[i] = G/rho_top

				# Energy - used to calculate enthaply, so no need to check. 
				# a = G*(self.enthalpy[i]-self.enthalpy[i-1])/MeshStep
				# b = LinPower[i]/1000/Area[i]
				# print a-b

				# Momentum 
				acc = G**2*(1/rho_top-1/rho_bot)
				f = 0.184/Re**0.2
				fric = f*G**2/De[i]/2/((rho_top+rho_bot)/2)*MeshStep
				grav = 9.81*(rho_top+rho_bot)/2*MeshStep
				deltaP = acc + fric + grav
				P_sum = P_sum + deltaP

				

		rho_out = IAPWS97(T=self.Tbulk[len(self.Mesh)-1], x=0).rho
		rho_in = subcooled_liq.rho
		self.velocity[0] = G/rho_in
		totalP = G**2*(1/rho_out-1/rho_in) + f*G**2/De_avg/2/((rho_out+rho_in)/2)*L + 9.81*(rho_out+rho_in)/2*L 
		# print("Total pressure change between inlet/outlet: %f [Pa]" % totalP)
		# print("Total pressure change by sum of increments: %f [Pa]" % P_sum)

			
		
		# print("Temperature in the bulk liquid [K]:")
		# print(self.Tbulk)
		# print("Temperature at the wall [K]:")
		# print(self.Tw)
		# print("Number of interations a each node:")
		# print(count)
		# print("Water velocity [m/s]:")
		# print(self.velocity)
		# print("Total pressure change between inlet/outlet: %f [Pa]" % P_sum)


		##################
		# Fuel Temperature

		self.Ts = np.zeros(len(self.Mesh)) # Pellet surface
		self.Tf = np.zeros(len(self.Mesh)) # Effective temperature in fuel
		self.Tgap = np.zeros(len(self.Mesh))
		self.Tclad = np.zeros(len(self.Mesh))
		kf = 2.4             #[W/m/K]
		kc = 17.             #[W/m/K]
		hg = 31000.          #[W/m^2/K]
		w = 0.92

		self.Ts[:] = self.Tw[:] + LinPower[:]/2.0/np.pi*(1/opt.GapR/hg+1/kc*np.log(opt.CladOR/opt.CladIR))
		self.Tf[:] = w*(self.Tw[:] + LinPower[:]/2.0/np.pi*(1.0/4.0/kf+1/opt.GapR/hg+1/kc*np.log(opt.CladOR/opt.CladIR))) + (1-w)*self.Ts[:]
		self.Tgap[:] = self.Tw[:] + LinPower[:]/2.0/np.pi*(1/opt.GapR/hg+1/kc*np.log(opt.CladOR/opt.CladIR))
		self.Tclad[:] =  self.Tw[:] + LinPower[:]/2.0/np.pi*(1/kc*np.log(opt.CladOR/opt.CladIR))

		# print("Temperature in the fuel [K]:")
		# print(self.Tf)
		# print("Temperature in the gap [K]:")
		# print(self.Tgap)
		# print("Temperature in the clad [K]:")
		# print(self.Tclad)


########################################################################
#end class