import os
import pandas as pd
from subprocess import run
from VASP_job.code.io import io
from VASP_job.code.structure import structure
from VASP_job.code.magnetism import magnetism

class VASP_job:
	"""
	Main functionality of the module.
	"""

	def __init__(self,
				executable_path = '/u/edmen/workbench/devel/VASP/vasp.5.4.4-flag4/bin',
				executable_name = 'vasp_ncl',
				potential_path  = '/u/edmen/workbench/devel/VASP/potentials/potpaw_PBE',
				job_script_name = 'job',
				out_file        = 'out',
				bfields         = True,
				verbose         = 'normal'):

		###############################################################################
		# Check on chosen verbose
		if verbose != 'low' and verbose != 'normal' and verbose != 'high':
			print('WARNING: be aware that you have not selected an available value for verbose.')
			self.verbose = 'normal'
			print('verbose has been set to default: normal')
		else:
			self.verbose = verbose
		
		###############################################################################
		# Initialising external classes
		self.io        = io(os.getcwd(), job_script_name, out_file, bfields, self.verbose)
		self.structure = structure(self.verbose)
		self.magnetism = magnetism(self.verbose)

		###############################################################################
		# Checking executable and potential paths
		# Fixing "/" in the executable path if necessary
		executable_path = self.io.add_slash(executable_path)
		potential_path  = self.io.add_slash(potential_path)
		self.executable_path = executable_path
		self.potential_path  = potential_path
		
		# Full executable path
		self.executable_name = executable_name
		self.executable = self.executable_path + self.executable_name
			
		assert os.path.exists(self.executable)     is True, "\nYour executable does not exist!\nYour executable is:\n"+self.executable
		assert os.path.exists(self.potential_path) is True, "\nYour potential path does not exist!\nYour potential path is:\n"+self.potential_path
		
		###############################################################################
		if self.verbose == "high":
			self.io.write_initialization_info(self.executable)

		return
	
	###############################################################################
	# Auxiliary definitions

###############################################################################
	# main methods

	###############################################################################
	# properties
	@property
	def df(self):
		return self._df
	@df.setter
	def df(self, val):
		try:
			structure, magnetic_inputs = val
		except ValueError:
			raise ValueError("Pass an iterable with two items: structure (from ASE) and class.io.magnetic_inputs")
		else:

			# First get magmoms from magdirs and betahs (if betah is False, magmom = magdir at that site)
			self.io.number_of_atoms = len(structure)

			magnetic_inputs.betahs = self.magnetism.set_betahs_from_ms(magnetic_inputs.ms, self.io.number_of_atoms)
			magmoms = self.magnetism.set_magmoms(magnetic_inputs, self.io.number_of_atoms)

			self._df = pd.DataFrame({
			"elements"  : structure.get_chemical_symbols(),
			"positions" : list( structure.positions ),
			"magdirs"   : magnetic_inputs.magdirs,
			"ms"        : magnetic_inputs.ms,
			"betahs"    : magnetic_inputs.betahs,
			"magmoms"   : magmoms,
			"B_CONSTRs" : magnetic_inputs.B_CONSTRs
			})

		self.io.structure = structure
		self.io.magnetic_inputs = magnetic_inputs
		self.io.magmoms = magmoms

		return

	###############################################################################
	# functionalities
	def run_vasp(self):
		os.chdir(self.io.cwd)
		run("sbatch "+self.job_file, shell=True)
		return

	def prepare_calculation(self, mode="Cartesian"):

		# prepare structure
		self.structure.prepare_structure(self.io.structure)
		# prepare magnetism
		self.magnetism.prepare_magnetism(self.df)

		# write files
		self.io.write_inputs_and_job(self.executable, self.potential_path,
									 self.structure.cell, self.structure.positions, mode,
									 self.structure.kpoints, self.structure.elements, self.structure.species,
									 self.magnetism.magmoms, self.magnetism.B_CONSTRs)

		return


# Deprecated:

		# first sort atoms by elements
		# atoms = atoms.sort_values("elements")

			# "magmoms"   : magnetic_info[0],
			# "betahs"    : magnetic_info[1],
			# "B_CONSTRs" : magnetic_info[2]

			
		# self.io.magnetic_info = magnetic_info