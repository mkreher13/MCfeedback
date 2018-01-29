# Class to provide initial linear power
# Last modified by Miriam Rathbun on 01/29/2018

import numpy as np

class Power():

###############################################################

	def __init__(self):
		self

###############################################################

	def Initial(self, options, Mesh):

		q = 17860
		self.LinPower = np.zeros(len(Mesh))
		self.LinPower[:] = q