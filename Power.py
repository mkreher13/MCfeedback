# Class to provide initial linear power
# Last modified by Miriam Rathbun on 02/14/2018

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
		self.Tf = np.zeros(len(Mesh))
		self.Tf[:] = opt.Tin
		self.LinPower = np.zeros(len(Mesh))
		self.LinPower[:] = q_prime

		# print self.Tf


		#####################################
		# Create OpenMC geometry
		#####################################

		FuelOR = opt.FuelOR*100  #[cm]
		CladIR = opt.CladIR*100  #[cm]
		CladOR = opt.CladOR*100  #[cm]
		Pitch = opt.PinPitch*100 #[cm]

		# Construct uniform initial source distribution over fissionable zones
		# Something may be wrong here
		lower_left = [-0.62992, -0.62992, 0]
		upper_right = [+0.62992, +0.62992, +365.76]
		uniform_dist = openmc.stats.Box(lower_left, upper_right, only_fissionable=True)

		# Settings file
		settings_file = openmc.Settings()
		settings_file.batches = 100
		settings_file.inactive = 50
		settings_file.particles = 10000
		settings_file.output = {'tallies': False}
		settings_file.temperature = {'multipole': True, 'tolerance': 1000} #need a multipole library
		settings_file.source = openmc.source.Source(space=uniform_dist)
		settings_file.seed = 1

		settings_file.export_to_xml()

		# Materials: to be modified for each mesh, add temperature info
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


		# Geometry file: add z-plane mesh
		fuel_or = openmc.ZCylinder(x0=0, y0=0, R=FuelOR)
		clad_ir = openmc.ZCylinder(x0=0, y0=0, R=CladIR)
		clad_or = openmc.ZCylinder(x0=0, y0=0, R=CladOR)
		left = openmc.XPlane(x0=-Pitch/2)
		right = openmc.XPlane(x0=Pitch/2)
		back = openmc.YPlane(y0=-Pitch/2)
		front = openmc.YPlane(y0=Pitch/2)
		z_list = []
		for i in range(0,len(Mesh)):
			z_list.append(openmc.ZPlane(z0=Mesh[i]))


		left.boundary_type = 'reflective'
		right.boundary_type = 'reflective'
		front.boundary_type = 'reflective'
		back.boundary_type = 'reflective'
		z_list[0].boundary_type = 'vacuum'
		z_list[-1].boundary_type = 'vacuum'

		fuel = openmc.Cell()
		gap = openmc.Cell()
		clad = openmc.Cell()
		water = openmc.Cell()

		fuel_list = []
		gap_list = []
		clad_list = []
		water_list = []
		for i in range(0,len(Mesh)-1):
			fuel_list.append(openmc.Cell())
			gap_list.append(openmc.Cell())
			clad_list.append(openmc.Cell())
			water_list.append(openmc.Cell())

		# print z_list

		j = 0
		for fuels in fuel_list:
			fuels.temperature = self.Tf[j]
			fuels.region = -fuel_or & +z_list[j] & -z_list[j+1]
			fuels.fill = uo2
			j = j+1
		j = 0
		for gaps in gap_list:
			gaps.temperature = self.Tf[j]
			gaps.region = +fuel_or & -clad_ir & +z_list[j] & -z_list[j+1]
			gaps.fill = helium
			j = j+1
		j = 0
		for clads in clad_list:
			clads.temperature = self.Tf[j]
			clads.region = +clad_ir & -clad_or & +z_list[j] & -z_list[j+1]
			clads.fill = zircaloy
			j = j+1
		j = 0
		for waters in water_list:
			waters.temperature = self.Tf[j]
			waters.region = +clad_or & +left & -right & +back & -front & +z_list[j] & -z_list[j+1]
			waters.fill = borated_water
			j = j+1


		fuel.region = -fuel_or & +z_list[0] & -z_list[-1]
		gap.region = +fuel_or & -clad_ir & +z_list[0] & -z_list[-1]
		clad.region = +clad_ir & -clad_or & +z_list[0] & -z_list[-1]
		water.region = +clad_or & +left & -right & +back & -front & +z_list[0] & -z_list[-1]

		fuel.fill = uo2
		gap.fill = helium
		clad.fill = zircaloy
		water.fill = borated_water

		# print fuel_list

		# keff is different with and without the random ZPlane
		root = openmc.Universe(universe_id=0, name='root universe')
		root.add_cells(fuel_list)
		root.add_cells(gap_list)
		root.add_cells(clad_list)
		root.add_cells(water_list)
		# root.add_cells([fuel, gap, clad, water])
		geometry_file = openmc.Geometry(root)
		geometry_file.export_to_xml()


		# Tallies


		# Plots
		plot = openmc.Plot()
		plot.width = [Pitch+450, Pitch+450] #+450, Pitch+450]
		plot.origin = [0., 0., 200]
		plot.color_by = 'cell'
		plot.filename = 'fuel-pin'
		plot.pixels = [1000, 1000]
		plot.basis = 'yz'
		# openmc.plot_inline(plot)

		
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




		

