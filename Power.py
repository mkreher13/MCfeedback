# Class to provide initial linear power
# Last modified by Miriam Rathbun on 02/09/2018

import numpy as np
import shutil
import openmc

class Power():

###############################################################

	def __init__(self):
		self

###############################################################

	def Initial(self, options, Mesh):

		#####################################
		# Initial power distribution
		#####################################

		q_prime = 17860
		self.LinPower = np.zeros(len(Mesh))
		self.LinPower[:] = q_prime


		#####################################
		# Create OpenMC geometry
		#####################################

		# Construct uniform initial source distribution over fissionable zones
		lower_left = [-0.62992, -0.62992, -10.0]
		upper_right = [+0.62992, +0.62992, +10.0]
		source = openmc.source.Source(space=openmc.stats.Box(lower_left, upper_right))
		source.space.only_fissionable = True


		# Settings file
		settings_file = openmc.Settings()
		settings_file.batches = 10
		settings_file.inactive = 5
		settings_file.particles = 10000
		settings_file.output = {'tallies': False}
		settings_file.source = source
		settings_file.sourcepoint_write = False
		settings_file.temperature = {'multipole': True, 'tolerance': 1000}

		settings_file.export_to_xml()


		# Move Files to PinGeo folder
		shutil.move('settings.xml', 'PinGeo/settings.xml')



###############################################################

	def Fuel(self, Tf):

		# Update fuel temperatures in OpenMC
		print("Fuel temperature:")
		print(Tf)


		#openmc.run(cwd='PinGeo')




		

