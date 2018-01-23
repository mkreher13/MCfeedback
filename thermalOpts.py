# Parsing input file
# Last edited by Miriam Rathbun on 12/11/2017


class ThermalOpts:

	def __init__(self):

		self

	def read(self, filename):

		inpFile = open(filename, 'r')


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
			if keyword == 'length':
				self.length = float(arguments)

			elif keyword == 'MeshPoints':
				self.MeshPoints = int(arguments)

			elif keyword == 'Tin':
				self.Tin = float(arguments)

			elif keyword == 'Pressure':
				self.Pressure = float(arguments)

			elif keyword == 'MassFlux':
				self.G = float(arguments)

			elif keyword == 'CladOR':
				self.CladOR = float(arguments)

			elif keyword == 'Pitch':
				self.Pitch = float(arguments)

			else:
				continue