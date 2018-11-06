# Parsing input file
# Last edited by Miriam Rathbun on 02/27/2018

import numpy as np

class ModelOpts:

	def __init__(self):

		self

	def read(self, filename):

		inpFile = open(filename, 'r')

		SpacingList = []
		self.GridTop_z = []
		self.GridBot_z = []
		Z = 0


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
				Z = Z + float(arguments)
				if keyword == 'Grid':
					self.GridTop_z.append(Z)
				else:
					self.GridBot_z.append(Z)

			elif keyword == 'CladOR':
				self.CladOR = float(arguments)

			elif keyword == 'CladIR':
				self.CladIR = float(arguments)

			elif keyword == 'FuelOR':
				self.FuelOR = float(arguments)

			elif keyword == 'PinPitch':
				self.PinPitch = float(arguments)

			elif keyword == 'GridPitch':
				self.GridPitch = float(arguments)

			elif keyword == 'ExtraCladOR':
				self.ExtraCladOR = float(arguments)

			else:
				continue

		self.GapR = (self.CladIR+self.FuelOR)/2
		self.Spacing = np.array(SpacingList)
