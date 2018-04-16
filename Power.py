# Class to provide initial linear power
# Last modified by Miriam Rathbun on 04/10/2018

import numpy as np
import shutil
import openmc
import os

class Power():

########################################################################

	def __init__(self):
		self

########################################################################

	def initial(self, opt, Mesh):

		#####################################
		# Create OpenMC geometry
		#####################################

		FuelOR = opt.FuelOR*100  #[cm]
		CladIR = opt.CladIR*100  #[cm]
		CladOR = opt.CladOR*100  #[cm]
		Pitch = opt.PinPitch*100 #[cm]

		# Construct uniform initial source distribution over fissionable zones
		lower_left = [-0.62992, -Pitch/2, 0]
		upper_right = [+0.62992, +Pitch/2, +365.76]
		uniform_dist = openmc.stats.Box(lower_left, upper_right, only_fissionable=True)

		# Settings file
		self.settings_file = openmc.Settings()
		self.settings_file.batches = 100
		self.settings_file.inactive = 50
		self.settings_file.particles = 5000
		self.settings_file.output = {'tallies': False}
		self.settings_file.temperature = {'multipole': True, 'tolerance': 1000}
		self.settings_file.source = openmc.source.Source(space=uniform_dist)
		self.settings_file.seed = 1

		self.settings_file.export_to_xml()


		# Materials file
		uo2 = openmc.Material(material_id=1, name='UO2 fuel at 2.4% wt enrichment')
		uo2.temperature = opt.Tin
		uo2.set_density('g/cm3', 10.29769)
		uo2.add_element('U', 1., enrichment=2.4)
		uo2.add_element('O', 2.)

		helium = openmc.Material(material_id=2, name='Helium for gap')
		helium.temperature = opt.Tin
		helium.set_density('g/cm3', 0.001598)
		helium.add_element('He', 2.4044e-4)

		zircaloy = openmc.Material(material_id=3, name='Zircaloy 4')
		zircaloy.temperature = opt.Tin
		zircaloy.set_density('g/cm3', 6.55)
		zircaloy.add_element('Sn', 0.014  , 'wo')
		zircaloy.add_element('Fe', 0.00165, 'wo')
		zircaloy.add_element('Cr', 0.001  , 'wo')
		zircaloy.add_element('Zr', 0.98335, 'wo')

		# borated_water = openmc.Material()
		# borated_water.temperature = opt.Tin
		# borated_water.set_density('g/cm3', 0.7406)
		# borated_water.add_element('B', 4.0e-5)
		# borated_water.add_element('H', 5.0e-2)
		# borated_water.add_element('O', 2.4e-2)
		# borated_water.add_s_alpha_beta('c_H_in_H2O')
		borated_water = openmc.model.borated_water(boron_ppm=432.473,temperature=opt.Tin,pressure=15)


		self.materials_file = openmc.Materials([uo2, helium, zircaloy, borated_water])
		self.materials_file.export_to_xml()


		# Geometry file
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

		self.fuel_list = []
		self.gap_list = []
		self.clad_list = []
		self.water_list = []
		for i in range(0,len(Mesh)-1):
			self.fuel_list.append(openmc.Cell())
			self.gap_list.append(openmc.Cell())
			self.clad_list.append(openmc.Cell())
			self.water_list.append(openmc.Cell())

		j = 0
		for fuels in self.fuel_list:
			fuels.region = -fuel_or & +z_list[j] & -z_list[j+1]
			fuels.fill = uo2
			j = j+1
		j = 0
		for gaps in self.gap_list:
			gaps.region = +fuel_or & -clad_ir & +z_list[j] & -z_list[j+1]
			gaps.fill = helium
			j = j+1
		j = 0
		for clads in self.clad_list:
			clads.region = +clad_ir & -clad_or & +z_list[j] & -z_list[j+1]
			clads.fill = zircaloy
			j = j+1
		j = 0
		for waters in self.water_list:
			waters.region = +clad_or & +left & -right & +back & -front & +z_list[j] & -z_list[j+1]
			waters.fill = borated_water
			j = j+1

		self.root = openmc.Universe(universe_id=0, name='root universe')
		self.root.add_cells(self.fuel_list)
		self.root.add_cells(self.gap_list)
		self.root.add_cells(self.clad_list)
		self.root.add_cells(self.water_list)
		self.geometry_file = openmc.Geometry(self.root)
		self.geometry_file.export_to_xml()


		# Tallies
		# power distribution: fission q recoverable (Sterling's note: starts 0, might be data pb)
		# openmc accounts for incoming neutron energy and isotope
		cell_filter = openmc.CellFilter(self.fuel_list)
		t = openmc.Tally(tally_id=1)
		t.filters.append(cell_filter)
		t.scores = ['fission-q-recoverable']
		tallies = openmc.Tallies([t])
		tallies.export_to_xml()


		# Plots
		plot = openmc.Plot()
		plot.width = [Pitch+450, Pitch+450]
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
		shutil.move('tallies.xml', 'PinGeo/tallies.xml')
		# shutil.move('plots.xml', 'PinGeo/plots.xml')

		openmc.run(cwd='PinGeo')
		sp = openmc.StatePoint('PinGeo/statepoint.'+str(self.settings_file.batches)+'.h5')
		tally = sp.get_tally(scores=['fission-q-recoverable'])
		self.Tally = np.ndarray.flatten(tally.sum)*0.000015
		# print(self.Tally)
		# os.remove('PinGeo/statepoint.'+str(self.settings_file.batches)+'.h5')
		# os.remove('PinGeo/summary.h5')
		# del sp


########################################################################

	def update(self, Tf, Tgap, Tclad, Tbulk, Mesh, RhoBulk):

		# Update temperatures in OpenMC
		print("Fuel temperature:")
		print(Tf)

		self.settings_file.batches = 50
		self.settings_file.inactive = 0
		self.settings_file.particles = 10000
		self.settings_file.export_to_xml()
		shutil.move('settings.xml', 'PinGeo/settings.xml')

		# NewWaterMat_list = []
		# for i in range(0,len(Mesh)-1):
		# 	NewWaterMat_list.append(openmc.Material())
		# j = 0
		# for NewWater in NewWaterMat_list:
		# 	NewWater.set_density('g/cm3', RhoBulk[j]/1000)
		# 	NewWater.temperature = (Tbulk[j]+Tbulk[j+1])/2
		# 	NewWater.add_element('B', 4.0e-5)
		# 	NewWater.add_element('H', 5.0e-2)
		# 	NewWater.add_element('O', 2.4e-2)
		# 	NewWater.add_s_alpha_beta('c_H_in_H2O')
		# 	self.materials_file.append(NewWater)
		# 	j = j+1

		self.materials_file.export_to_xml()
		shutil.move('materials.xml', 'PinGeo/materials.xml')

		j = 0
		for fuels in self.fuel_list:
			fuels.temperature = (Tf[j]+Tf[j+1])/2
			j = j+1
		j = 0
		for gaps in self.gap_list:
			gaps.temperature = (Tgap[j]+Tgap[j])/2.
			j = j+1
		j = 0
		for clads in self.clad_list:
			clads.temperature = (Tclad[j]+Tclad[j+1])/2.
			j = j+1
		j = 0
		for waters in self.water_list:
			# waters.fill = NewWaterMat_list[j]
			waters.temperature = (Tbulk[j]+Tbulk[j+1])/2
			j = j+1

		self.root.add_cells(self.fuel_list)
		self.root.add_cells(self.gap_list)
		self.root.add_cells(self.clad_list)
		self.root.add_cells(self.water_list)
		self.geometry_file = openmc.Geometry(self.root)
		self.geometry_file.export_to_xml()
		shutil.move('geometry.xml', 'PinGeo/geometry.xml')

		# Tallies
		# power distribution: fission q recoverable (starts 0, might be data pb)
		# openmc accounts for incoming neutron energy and isotope
		cell_filter = openmc.CellFilter(self.fuel_list)
		t = openmc.Tally(tally_id=2)
		t.filters.append(cell_filter)
		t.scores = ['fission-q-recoverable']
		self.tallies = openmc.Tallies([t])
		self.tallies.export_to_xml()
		shutil.move('tallies.xml', 'PinGeo/tallies.xml')

########################################################################

	def power_factors(self, t):


		self.Tally = t[2].results[:,0,1]*0.000015
		# #openmc_tally_get_scores()
		# print(openmc.capi.openmc_tally_results())

		# sp = openmc.StatePoint('PinGeo/statepoint.'+str(self.settings_file.batches)+'.h5')
		# tally = sp.get_tally(scores=['fission-q-recoverable'])
		# self.Tally = np.ndarray.flatten(tally.sum)*0.000015





		

