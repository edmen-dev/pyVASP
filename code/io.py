from dataclasses import dataclass, fields
from VASP_job.code.dataclass_inputs import INCAR, INCAR_constr, INCAR_constr_flag5, INCAR_relaxation
from VASP_job.code.dataclass_inputs import job_parameters, RWIGS, potential_files

class io:
   """
   To write and manage inputs and outputs
   """

   def __init__(self,
             cwd,
             job_script_name  = 'job',
             out_file_name    = 'out',
             bfields          = False,
             relaxation       = False,
             verbose          = 'normal'):

      """
      RWIGS and INCAR are dataclasses
      containing input information for RWIGS and standard variables in INCAR, respectively.
      """

      self.job_script_name = job_script_name
      self.out_file_name   = out_file_name
      self.bfields         = bfields
      self.relaxation      = relaxation
      self.initialise_magnetic_strings()
         
      ###############################################################################
      # Set working directory and files
      self.cwd = cwd
         
      ###############################################################################
      # Set default inputs
      self.INCAR               = INCAR()
      self.INCAR_constr        = INCAR_constr()
      self.INCAR_constr_flag5  = INCAR_constr_flag5()
      self.INCAR_relaxation    = INCAR_relaxation()
      self.job_parameters      = job_parameters()
      self.RWIGS               = RWIGS()
      self.potential_files     = potential_files()
      
      ###############################################################################
      # Set files
      self.set_files()

      return
   
   ###############################################################################
   # Auxiliary definitions
   
   def write_initialization_info(self, executable, potential_path, seed_mag):
      print("\nYour executable is:")
      print("   "+executable)
      
      print("\nYour potential path is:")
      print("   "+potential_path)
      
      print("\nYour current working directory (cwd) is:")
      print("   "+self.cwd)
      
      print("\nYour bfields and relaxation flags are:")
      print("   bfields = "+str(self.bfields))
      print("   relaxation = "+str(self.relaxation))
      
      print("\nYour seed_mag for DLM approach is:")
      print("   seed_mag = "+str(seed_mag))
      
      print("\nYour default INCAR parameters are:")
      self.write_fields(self.INCAR)
         
      print("\nYour default INCAR parameters for constraining fields are:")
      self.write_fields(self.INCAR_constr)
      self.write_fields(self.INCAR_constr_flag5)
         
      print("\nYour default INCAR parameters for relaxation are:")
      self.write_fields(self.INCAR_relaxation)
      
      print("\nYour default RWIGS parameters are:")
      self.write_fields(self.RWIGS)
         
      print("\nYour default potentials are:")
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
   def structure_ase(self):
      return self._structure_ase
   @structure_ase.setter
   def structure_ase(self, new_val):
      self._structure_ase = new_val
      

   ###############################################################################
   # functionalities

   def write_inputs(self, potential_path, df, structure, mode="Cartesian"):

      elements  = df["elements"].tolist()
      positions = df["positions"].tolist()
      magmoms   = df["magmoms"].tolist()
      B_CONSTRs = df["B_CONSTRs"].tolist()
      
      kpoints         = structure.kpoints
      lattice_vectors = structure.lattice_vectors
      species         = structure.species

      self.write_INCAR(species, magmoms, B_CONSTRs)
      self.write_KPOINTS(kpoints)
      self.write_POTCAR(species, potential_path)
      self.write_POSCAR(lattice_vectors, positions, elements, species, mode)
      return

   ###############
   # INCAR file
   def add_INCAR_parameters(self, text_file):
      for field in fields(self.INCAR):
         string = field.name + "="
         string += getattr(self.INCAR, field.name) 
         string += "\n"
         text_file.write(string)
      return

   def add_RWIGS_parameters(self, text_file, species):
      string = "RWIGS="
      for element in species:
         string += getattr(self.RWIGS, element) + " "
      string += "\n"
      text_file.write(string)
      return

   def add_relaxation_parameters(self, text_file):
      for field in fields(self.INCAR_relaxation):
         string = field.name + "="
         string += getattr(self.INCAR_relaxation, field.name) 
         string += "\n"
         text_file.write(string)
      return

   def add_constr_INCAR_parameters(self, text_file):
      for field in fields(self.INCAR_constr):
         string = field.name + "="
         string += getattr(self.INCAR_constr, field.name) 
         string += "\n"
         text_file.write(string)

      if self.INCAR_constr.I_CONSTRAINED_M == '5':
         for field in fields(self.INCAR_constr_flag5):
            string = field.name + "="
            string += getattr(self.INCAR_constr_flag5, field.name) 
            string += "\n"
            text_file.write(string)
      return

   def write_INCAR(self, species, magmoms, B_CONSTRs):
      with open(self.INCAR_file, "w") as text_file:
         self.add_INCAR_parameters(text_file)
         self.add_RWIGS_parameters(text_file, species)

         # Relaxation:
         if self.relaxation:
            self.add_relaxation_parameters(text_file)

         # Magnetism:
         if self.bfields:
            self.add_constr_INCAR_parameters(text_file)

         self.initialise_magnetic_strings()

         for i, magmom in enumerate(magmoms):
            for idir in range(3):
               self._MAGMOM_string   += ' ' + '{:.7f}'.format(magmom[idir])
               if self.bfields:
                  self._M_CONSTR_string += ' ' + '{:.7f}'.format(magmom[idir])
            self._MAGMOM_string   += ' '
            if self.bfields:
               self._M_CONSTR_string += ' '
         
         if self.bfields == True and self.INCAR_constr.I_CONSTRAINED_M == '5':
            for i, B_CONSTR in enumerate(B_CONSTRs):
               for idir in range(3):
                  self._B_CONSTR_string += ' ' + '{:.7f}'.format(B_CONSTR[idir])
               self._B_CONSTR_string   += ' '

         text_file.write(self._MAGMOM_string + '\n')
         if self.bfields:
            text_file.write(self._M_CONSTR_string + '\n')
            if self.INCAR_constr.I_CONSTRAINED_M == "5":
               text_file.write(self._B_CONSTR_string + '\n')
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
         text_file.write("\n\n"+self.command+" "+executable+" > "+self.out_file)
         text_file.write("\n\nend_time=$(date +%s)  # Record the end time")
         text_file.write("\nduration=$((end_time - start_time))  # Calculate the duration in seconds")
         text_file.write("\n\n# Print the duration")
         text_file.write("\necho \"Job duration: $((duration/60)) minutes\"")

      return