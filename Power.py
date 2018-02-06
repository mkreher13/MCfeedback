# Class to provide initial linear power
# Last modified by Miriam Rathbun on 02/06/2018

import numpy as np
import openmc

class Power():

###############################################################

	def __init__(self):
		self

###############################################################

	def Initial(self, options, Mesh):

		q_prime = 17860
		self.LinPower = np.zeros(len(Mesh))
		self.LinPower[:] = q_prime

###############################################################

	def Fuel(self, Tf):

		print("Fuel temperature:")
		print(Tf)

		# Incorporate Tf into materials xml file

		# openmc.run(cwd='PinGeo')

