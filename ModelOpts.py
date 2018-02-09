# Parsing input file
# Last edited by Miriam Rathbun on 02/09/2018

import numpy as np

class ModelOpts:

	def __init__(self):

		self

	def read(self, filename):

		inpFile = open(filename, 'r')

		SpacingList = []


		for line in inpFile:

			# Remove trailing white space
			line = line.strip()
			# Remove newline characters
			line = line.strip('\n')
			# Remove string after comment character (#)
			line, scratch1, scratch2 = line.partition('#')
			# Skip empyt lines
			if len(line) == 0:
				continue


			keyword, arguments = line.split(' ',1)
			if keyword == 'MaxMesh':
				self.MaxMesh = float(arguments)

			elif keyword == 'Tin':
				self.Tin = float(arguments)

			elif keyword == 'Pressure':
				self.Pressure = float(arguments)

			elif keyword == 'MassFlux':
				self.G = float(arguments)

			elif keyword == 'Active' or keyword == 'Grid':
				SpacingList.append(float(arguments))

			elif keyword == 'CladOR':
				self.CladOR = float(arguments)

			elif keyword == 'CladIR':
				self.CladIR = float(arguments)

			elif keyword == 'FuelOR':
				self.FuelOR = float(arguments)

			elif keyword == 'PinPitch':
				self.PinPitch = float(arguments)

			else:
				continue

		self.GapR = (self.CladIR+self.FuelOR)/2
		self.Spacing = np.array(SpacingList)

