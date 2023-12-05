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
            bfields         = False,
            relaxation      = False,
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
      self.io        = io(os.getcwd(), job_script_name, out_file, bfields, relaxation, self.verbose)
      self.structure = structure(self.verbose)
      self.magnetism = magnetism(verbose = self.verbose)

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
         structure_ase, magnetic_inputs = val
      except ValueError:
         raise ValueError("Pass an iterable with two items: structure_ase (from ASE) and class.io.magnetic_inputs")
      else:

         # First get number of magnetic atoms and set default values to magnetic_inputs.ms and magnetic.inputs.B_CONSTRs if not given
         self.io.number_of_atoms = len(structure_ase)
         magnetic_inputs = self.magnetism.set_default_magnetic_inputs(magnetic_inputs, self.io.number_of_atoms)

         # Get magmoms from magdirs and betahs (if betah is False, magmom = magdir at that site)
         magnetic_inputs.betahs = self.magnetism.set_betahs_from_ms(magnetic_inputs.ms, self.io.number_of_atoms)
         magmoms = self.magnetism.set_magmoms(magnetic_inputs, self.io.number_of_atoms)

         self._df = pd.DataFrame({
         "elements"  : structure_ase.get_chemical_symbols(),
         "positions" : list( structure_ase.positions ),
         "magdirs"   : magnetic_inputs.magdirs,
         "ms"        : magnetic_inputs.ms,
         "betahs"    : magnetic_inputs.betahs,
         "magmoms"   : magmoms,
         "B_CONSTRs" : magnetic_inputs.B_CONSTRs
         })

      self.io.structure = structure_ase
      self.io.magnetic_inputs = magnetic_inputs
      self.io.magmoms = magmoms

      self.structure.lattice_vectors = structure_ase.cell.array

      return

   ###############################################################################
   # functionalities
   def run_vasp(self):
      os.chdir(self.io.cwd)
      run("sbatch "+self.job_file, shell=True)
      return

   def prepare_bfields(self, I_CONSTRAINED="4", LAMBDA="1",
                       B_MIX="1.0", B_ref="0.02", N_MIX="1.0", E_PENALTY_MAX="3.8", LAMBDA_FIELD_MAX="1e-3"):
      self.io.bfields = True

      self.io.INCAR_constr.I_CONSTRAINED = I_CONSTRAINED
      self.io.INCAR_constr.LAMBDA        = LAMBDA

      self.io.INCAR_constr_flag5.B_MIX            = B_MIX
      self.io.INCAR_constr_flag5.B_ref            = B_ref
      self.io.INCAR_constr_flag5.N_MIX            = N_MIX
      self.io.INCAR_constr_flag5.E_PENALTY_MAX    = E_PENALTY_MAX
      self.io.INCAR_constr_flag5.LAMBDA_FIELD_MAX = B_MIX

      return

   def prepare_relaxation(self, IBRION="2", ISIF="3", NSW="100", EDIFFG="-0.01", ISYM="2"):
      self.io.relaxation = True

      self.io.INCAR_relaxation.IBRION = IBRION
      self.io.INCAR_relaxation.ISIF   = ISIF
      self.io.INCAR_relaxation.NSW    = NSW
      self.io.INCAR_relaxation.EDIFFG = EDIFFG
      self.io.INCAR.ISYM              = ISYM
      return

   def set_calculation(self, structure_ase, magnetic_inputs, mode="Cartesian"):

      # prepare structure and magnetism
      self.df = [structure_ase, magnetic_inputs]

      # write files
      species = list( structure_ase.symbols.species() )
      self.io.write_inputs_and_job(self.executable, self.potential_path,
                                   self.df, self.structure, species, mode)

      return


# Deprecated:


      # self.structure.prepare_structure(self.io.structure)
      # self.magnetism.prepare_magnetism(self.df)

      # first sort atoms by elements
      # atoms = atoms.sort_values("elements")

         # "magmoms"   : magnetic_info[0],
         # "betahs"    : magnetic_info[1],
         # "B_CONSTRs" : magnetic_info[2]

         
      # self.io.magnetic_info = magnetic_info