from dataclasses import dataclass, fields
from VASP_job.code.dataclass_inputs import standard_INCAR_parameters, constr_INCAR_parameters, constr_INCAR_parameters_flag5
from VASP_job.code.dataclass_inputs import job_parameters, RWIGS_parameters, potential_files
from VASP_job.code.dataclass_inputs import magnetic_inputs

class io:
	"""
	To write and manage inputs and outputs
	"""

	def __init__(self,
				 cwd,
				 job_script_name  = 'job',
				 out_file_name    = 'out',
				 bfields          = True,
				 verbose          = 'normal'):

		"""
		RWIGS_parameters and potential_files are dataclasses
		containing input information for RWIGS and standard variables in INCAR, respectively.
		"""

		self.job_script_name = job_script_name
		self.out_file_name   = out_file_name
		self.bfields         = bfields
		self.initialise_magnetic_strings()
			
		###############################################################################
		# Set working directory and files
		cwd = self.add_slash(cwd)
		self.cwd = cwd
			
		###############################################################################
		# Set default inputs
		self.standard_INCAR_parameters      = standard_INCAR_parameters()
		self.constr_INCAR_parameters        = constr_INCAR_parameters()
		self.constr_INCAR_parameters_flag5  = constr_INCAR_parameters_flag5()
		self.job_parameters                 = job_parameters()
		self.RWIGS_parameters               = RWIGS_parameters()
		self.potential_files                = potential_files()
		self.magnetic_inputs                = magnetic_inputs()
		
		###############################################################################
		# Set files
		self.set_files()

		return
	
	###############################################################################
	# Auxiliary definitions
	
	def write_initialization_info(self, executable):
		print("\nYour executable is:")
		print("   "+executable)
		
		print("\nYour current working directory (cwd) is:")
		print("   "+self.cwd)
		
		print("\nYour INCAR parameters are:")
		self.write_fields(self.standard_INCAR_parameters)
			
		print("\nYour INCAR parameters for constraining fields are:")
		self.write_fields(self.constr_INCAR_parameters)
		self.write_fields(self.constr_INCAR_parameters_flag5)
		
		print("\nYour RWIGS parameters are:")
		self.write_fields(self.RWIGS_parameters)
			
		print("\nYour potentials are:")
		self.write_fields(self.potential_files)
			
		return
	
	def write_fields(self, dataclass_name):
		for field in fields(dataclass_name):
			print('   '+field.name, '=', getattr(dataclass_name, field.name))
		return

	def initialise_magnetic_strings(self):
		self._MAGMOM_string   = 'MAGMOM= '
		self._M_CONSTR_string = 'M_CONSTR= '
		self._B_CONSTR_string = 'B_CONSTR= '
		return
	
	def set_files(self):
		self.KPOINTS_file = self.cwd+'KPOINTS'
		self.POTCAR_file  = self.cwd+'POTCAR'
		self.POSCAR_file  = self.cwd+'POSCAR'
		self.INCAR_file   = self.cwd+'INCAR'
		self.job_file     = self.cwd+self.job_script_name
		self.out_file     = self.cwd+self.out_file_name
		return

	def add_slash(self, path):
		if path[-1] != '/':
			path += '/'
		return path

###############################################################################
	# main methods

	###############################################################################
	# properties
	@property
	def cwd(self):
		return self._cwd
	@cwd.setter
	def cwd(self, new_val):
		new_val = self.add_slash(new_val)
		self._cwd = new_val
		self.set_files()
		
	@property
	def number_of_atoms(self):
		return self._number_of_atoms
	@number_of_atoms.setter
	def number_of_atoms(self, new_val):
		self._number_of_atoms = new_val

	@property
	def structure(self):
		return self._structure
	@structure.setter
	def structure(self, new_val):
		self._structure = new_val

	@property
	def magnetic_inputs(self):
		return self._magnetic_inputs
	@magnetic_inputs.setter
	def magnetic_inputs(self, new_val):
		self._magnetic_inputs = new_val

	@property
	def magmoms(self):
		return self._magmoms
	@magmoms.setter
	def magmoms(self, new_val):
		self._magmoms = new_val
		

	###############################################################################
	# functionalities

	def write_inputs_and_job(self, executable, potential_path,
							 lattice_vectors, positions, mode,
							 kpoints, elements, species,
							 magmoms, B_CONSTRs):

		self.write_INCAR(species, magmoms, B_CONSTRs)
		self.write_KPOINTS(kpoints)
		self.write_POTCAR(species, potential_path)
		self.write_POSCAR(lattice_vectors, positions, elements, species, mode)
		self.write_job(executable)
		return

	###############
	# INCAR file
	def add_INCAR_parameters(self, text_file):
		for field in fields(self.standard_INCAR_parameters):
			string = field.name + "="
			string += getattr(self.standard_INCAR_parameters, field.name) 
			string += "\n"
			text_file.write(string)
		return

	def add_RWIGS_parameters(self, text_file, species):
		string = "RWIGS="
		for element in species:
			string += getattr(self.RWIGS_parameters, element) + " "
		string += "\n"
		text_file.write(string)
		return

	def add_constr_INCAR_parameters(self, text_file):
		for field in fields(self.constr_INCAR_parameters):
			string = field.name + "="
			string += getattr(self.constr_INCAR_parameters, field.name) 
			string += "\n"
			text_file.write(string)

		if self.constr_INCAR_parameters.I_CONSTRAINED == '5':
			for field in fields(self.constr_INCAR_parameters_flag5):
				string = field.name + "="
				string += getattr(self.constr_INCAR_parameters_flag5, field.name) 
				string += "\n"
				text_file.write(string)
		return

	def write_INCAR(self, species, magmoms, B_CONSTRs):
		with open(self.INCAR_file, "w") as text_file:
			self.add_INCAR_parameters(text_file)
			self.add_RWIGS_parameters(text_file, species)

			# Magnetism:
			self.initialise_magnetic_strings()

			for i, magmom in enumerate(magmoms):
				for idir in range(3):
					self._MAGMOM_string   += ' ' + '{:.7f}'.format(magmom[idir])
					if self.bfields:
						self._M_CONSTR_string += ' ' + '{:.7f}'.format(magmom[idir])
				self._MAGMOM_string   += ' '
				if self.bfields:
					self._M_CONSTR_string += ' '
			
			if self.bfields == True and self.constr_INCAR_parameters.I_CONSTRAINED == '5':
				for i, B_CONSTR in enumerate(B_CONSTRs):
					for idir in range(3):
						self._B_CONSTR_string += ' ' + '{:.7f}'.format(B_CONSTR[idir])
					self._B_CONSTR_string   += ' '

			text_file.write(self._MAGMOM_string + '\n')
			if self.bfields:
				text_file.write(self._M_CONSTR_string + '\n')
				if self.constr_INCAR_parameters.I_CONSTRAINED == "5":
					text_file.write(self._B_CONSTR_string + '\n')

			if self.bfields:
				self.add_constr_INCAR_parameters(text_file)
		return

	###############
	# KPOINTS file
	def write_KPOINTS(self, kpoints):
		with open(self.KPOINTS_file, "w") as text_file:
			text_file.write('KPOINTS created by VASP_job python class\n')
			text_file.write('0\n')
			text_file.write('Monkhorst_Pack\n')
			text_file.write(kpoints + '\n')
			text_file.write('0 0 0\n')
		return

	###############
	# POTCAR file
	def write_POTCAR(self, species, potential_path):
		with open(self.POTCAR_file, 'w') as text_file:
			for element in species:
				potential = potential_path + getattr(self.potential_files, element) + "/POTCAR"
				with open(potential) as f:
					potential_text = f.readlines()
				for i in potential_text:
					text_file.write(i)
		return

	###############
	# POSCAR file
	def write_POSCAR(self, lattice_vectors, positions, elements, species, mode="Cartesian"):
		with open(self.POSCAR_file, 'w') as text_file:
			text_file.write("Poscar file generated with python code VASP_job")
			text_file.write("\n1.0")
			text_file.write("\n")
			for lattice_vector in lattice_vectors:
				text_file.write('{:.7f}'.format(lattice_vector[0]) + " ")
				text_file.write('{:.7f}'.format(lattice_vector[1]) + " ")
				text_file.write('{:.7f}'.format(lattice_vector[2]) + "\n")
			for element in species:
				text_file.write(element + " ")
			text_file.write("\n")
			for element in species:
				text_file.write( str( elements.count(element) ) + " " )
			text_file.write("\n"+mode)
			text_file.write("\n")
			for position in positions:
				text_file.write('{:.7f}'.format(position[0]) + " ")
				text_file.write('{:.7f}'.format(position[1]) + " ")
				text_file.write('{:.7f}'.format(position[2]) + "\n")
			
		return

	###############
	# job file
	def write_job(self, executable):
		header_str = "#!/bin/bash"
		sbatch_str = "\n#SBATCH --"
		with open(self.job_file, "w") as text_file:
			text_file.write(header_str)
			for field in fields(self.job_parameters):
				string = sbatch_str
				string += field.name.replace("_", "-") + "="
				string += getattr(self.job_parameters, field.name)
				text_file.write(string)
			text_file.write("\n\nstart_time=$(date +%s)  # Record the start time")
			text_file.write("\n\nsrun "+executable+" > "+self.out_file)
			text_file.write("\n\nend_time=$(date +%s)  # Record the end time")
			text_file.write("\nduration=$((end_time - start_time))  # Calculate the duration in seconds")
			text_file.write("\n\n# Print the duration")
			text_file.write("\necho \"Job duration: $((duration/60)) minutes\"")

		return