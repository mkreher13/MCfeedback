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

	def Initial(self, opt, Mesh):

		#####################################
		# Initial power distribution
		#####################################

		q_prime = 17860
		self.LinPower = np.zeros(len(Mesh))
		self.LinPower[:] = q_prime


		#####################################
		# Create OpenMC geometry
		#####################################

		FuelOR = opt.FuelOR*100  #[cm]
		CladIR = opt.CladIR*100  #[cm]
		CladOR = opt.CladOR*100  #[cm]
		Pitch = opt.PinPitch*100 #[cm]

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

		# Materials: to be modified
		uo2 = openmc.Material(material_id=1, name='UO2 fuel at 2.4% wt enrichment')
		uo2.set_density('g/cm3', 10.29769)
		uo2.add_element('U', 1., enrichment=2.4)
		uo2.add_element('O', 2.)

		helium = openmc.Material(material_id=2, name='Helium for gap')
		helium.set_density('g/cm3', 0.001598)
		helium.add_element('He', 2.4044e-4)

		zircaloy = openmc.Material(material_id=3, name='Zircaloy 4')
		zircaloy.set_density('g/cm3', 6.55)
		zircaloy.add_element('Sn', 0.014  , 'wo')
		zircaloy.add_element('Fe', 0.00165, 'wo')
		zircaloy.add_element('Cr', 0.001  , 'wo')
		zircaloy.add_element('Zr', 0.98335, 'wo')

		borated_water = openmc.Material(material_id=4, name='Borated water')
		borated_water.set_density('g/cm3', 0.740582)
		borated_water.add_element('B', 4.0e-5)
		borated_water.add_element('H', 5.0e-2)
		borated_water.add_element('O', 2.4e-2)
		borated_water.add_s_alpha_beta('c_H_in_H2O')

		materials_file = openmc.Materials([uo2, helium, zircaloy, borated_water])
		materials_file.export_to_xml()


		# Geometry file
		fuel_or = openmc.ZCylinder(surface_id=1, x0=0, y0=0, R=FuelOR, name='Fuel OR')
		clad_ir = openmc.ZCylinder(surface_id=2, x0=0, y0=0, R=CladIR, name='Clad IR')
		clad_or = openmc.ZCylinder(surface_id=3, x0=0, y0=0, R=CladOR, name='Clad OR')
		left = openmc.XPlane(surface_id=4, x0=-Pitch/2, name='left')
		right = openmc.XPlane(surface_id=5, x0=Pitch/2, name='right')
		bottom = openmc.YPlane(surface_id=6, y0=-Pitch/2, name='bottom')
		top = openmc.YPlane(surface_id=7, y0=Pitch/2, name='top')
		entrance = openmc.ZPlane(surface_id=8, z0=0, name='entrance')
		exit = openmc.ZPlane(surface_id=9, z0=100, name='exit')

		left.boundary_type = 'reflective'
		right.boundary_type = 'reflective'
		top.boundary_type = 'reflective'
		bottom.boundary_type = 'reflective'
		entrance.boundary_type = 'vacuum'
		exit.boundary_type = 'vacuum'

		fuel = openmc.Cell(cell_id=1, name='cell 1')
		gap = openmc.Cell(cell_id=2, name='cell 2')
		clad = openmc.Cell(cell_id=3, name='cell 3')
		water = openmc.Cell(cell_id=4, name='cell 4')

		fuel.region = -fuel_or & +entrance & -exit
		gap.region = +fuel_or & -clad_ir & +entrance & -exit
		clad.region = +clad_ir & -clad_or & +entrance & -exit
		water.region = +clad_or & +left & -right & +bottom & -top & +entrance & -exit

		fuel.fill = uo2
		gap.fill = helium
		clad.fill = zircaloy
		water.fill = borated_water

		root = openmc.Universe(universe_id=0, name='root universe')
		root.add_cells([fuel, gap, clad, water])
		geometry_file = openmc.Geometry(root)
		geometry_file.export_to_xml()

		plot = openmc.Plot()
		plot.width = [Pitch+150, Pitch+150]
		plot.origin = [0., 0., 50]
		plot.color_by = 'material'
		plot.filename = 'fuel-pin'
		plot.pixels = [1000, 1000]
		plot.basis = 'yz'
		#openmc.plot_inline(plot)

		
		# Move Files to PinGeo folder
		shutil.move('settings.xml', 'PinGeo/settings.xml')
		shutil.move('materials.xml', 'PinGeo/materials.xml')
		shutil.move('geometry.xml', 'PinGeo/geometry.xml')
		# shutil.move('plots.xml', 'PinGeo/plots.xml')



###############################################################

	def Fuel(self, Tf):

		# Update fuel temperatures in OpenMC
		print("Fuel temperature:")
		print(Tf)


		openmc.run(cwd='PinGeo')




		

