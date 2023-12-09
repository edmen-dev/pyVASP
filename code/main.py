import numpy as np
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
            ntasks_per_node = 40,
            command         = "srun",
            pyscript        = False,
            seed_mag        = "random",
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
      self.magnetism = magnetism(seed = seed_mag, verbose = self.verbose)
      
      # set ntasks per node
      self.ntasks_per_node = ntasks_per_node
      self.io.job_parameters.ntasks = str(self.ntasks_per_node)
      # set command
      self.io.command = command
      self.pyscript   = pyscript

      ###############################################################################
      # Setting executable and potential paths, and checking these exist
      self.executable_path = executable_path
      self.potential_path  = potential_path
      
      # Full executable path
      self.executable = executable_name
      
      ###############################################################################
      if self.verbose == "high":
         self.io.write_initialization_info(self.executable, self.potential_path, seed_mag)

      return
   
   ###############################################################################
   # Auxiliary definitions

###############################################################################
   # main methods

   ###############################################################################
   # properties
   @property
   def executable_path(self):
      return self._executable_path
   @executable_path.setter
   def executable_path(self, new_val):
      # Fixing "/" in the executable path if necessary
      new_val = self.io.add_slash(new_val)
      self._executable_path = new_val
      
   @property
   def potential_path(self):
      return self._potential_path
   @potential_path.setter
   def potential_path(self, new_val):
      # Fixing "/" in the executable path if necessary
      new_val = self.io.add_slash(new_val)
      self._potential_path = new_val
      assert os.path.exists(self._potential_path) is True, "\nYour potential path does not exist!\nYour potential path is:\n"+self.potential_path
      
   @property
   def executable(self):
      return self._executable
   @executable.setter
   def executable(self, new_val):
      self.executable_name = new_val
      self._executable = self.executable_path + new_val
      assert os.path.exists(self._executable) is True, "\nYour executable does not exist!\nYour executable is:\n"+self.executable
      
   @property
   def df(self):
      return self._df
   @df.setter
   def df(self, structure_ase):
      # try:
      #    structure_ase, magnetic_inputs = val
      # except ValueError:
      #    raise ValueError("Pass an iterable with two items: structure_ase (from ASE) and class.io.magnetic_inputs")
      # else:

      # First get number of magnetic atoms and set default values to magnetic_inputs.ms and magnetic.inputs.B_CONSTRs if not given
      self.io.number_of_atoms = len(structure_ase)
      structure_ase = self.magnetism.set_default_magnetic_inputs(structure_ase, self.io.number_of_atoms)

      # Get magmoms from magdirs and betahs (if ms is 1, magmom = magdir at that site)
      structure_ase = self.magnetism.set_betahs_from_ms(structure_ase, self.io.number_of_atoms)
      structure_ase = self.magnetism.set_magmoms(structure_ase, self.io.number_of_atoms)

      self._df = pd.DataFrame({
      "elements"  : structure_ase.get_chemical_symbols(),
      "positions" : [tuple(sublist) for sublist in list( structure_ase.positions )],
      "magdirs"   : [tuple(sublist) for sublist in list( structure_ase.arrays["magdirs"] )],
      "ms"        : list( structure_ase.arrays["ms"] ),
      "betahs"    : list( structure_ase.arrays["betahs"] ),
      "magmoms"   : [tuple(sublist) for sublist in list( structure_ase.arrays["magmoms"] )],
      "B_CONSTRs" : [tuple(sublist) for sublist in list( structure_ase.arrays["B_CONSTRs"] )]
      })
      # sort values to satisfy vasp
      self._df = self._df.sort_values(["elements", "magdirs", "positions"])

      self.io.structure_ase = structure_ase

      self.structure.lattice_vectors = structure_ase.cell.array
      self.structure.elements = self._df["elements"]
      species = []
      for element in self.structure.elements:
         if element not in species:
            species.append(element)
      self.structure.species = species

      return

   ###############################################################################
   # functionalities
   def run_vasp(self):
      os.chdir(self.io.cwd)
      run(self.io.command+" "+self.executable+" > "+self.io.out_file, shell=True)
      return
   
   def submit_job(self):      
      os.chdir(self.io.cwd)
      run("sbatch "+self.io.job_file, shell=True)
      return

   def prepare_bfields(self, I_CONSTRAINED_M="4", LAMBDA="1",
                       B_MIX="1.0", B_ref="0.02", N_MIX="1.0", E_PENALTY_MAX="3.8", LAMBDA_FIELD_MAX="1e-3"):
      self.io.bfields = True

      self.io.INCAR_constr.I_CONSTRAINED_M = I_CONSTRAINED_M
      self.io.INCAR_constr.LAMBDA          = LAMBDA

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

   def set_calculation(self, structure_ase, mode="Cartesian", ntasks=None, time=None, chdir=False):
      # set ntasks, if given
      if ntasks != None:
         self.set_ntasks(ntasks)

      # set time, if given
      if time != None:
         time = float(time)
         time = str(int(time))
         self.io.job_parameters.time = time

      # prepare structure and magnetism
      self.df = structure_ase

      # write files
      if chdir:
         os.chdir(self.io.cwd)
      self.io.write_inputs(self.potential_path, self.df, self.structure, mode)
      
      if not self.pyscript:
         self.io.write_job(self.executable)

      return

   def restart_from_charge(self, cwd_new=False, kpoints=False, LAMBDA=False, chdir=False):

      if cwd_new is not False:         
         if not os.path.exists(cwd_new):
            run("mkdir " + cwd_new, shell=True)
         run("cp CHGCAR CHG WAVECAR "+cwd_new, shell=True)
         self.io.cwd = cwd_new

      self.io.INCAR.ISTART = "1"
      self.io.INCAR.ICHARG = "1"

      if kpoints is not False:
         self.structure.kpoints = kpoints
      if LAMBDA is not False:
         self.io.INCAR_constr.LAMBDA = str(LAMBDA)

      # write files
      if chdir:
         os.chdir(self.io.cwd)
      self.io.write_inputs(self.potential_path, self.df, self.structure)

      return

   def set_ntasks(self, ntasks="40"):
      ntasks = float(ntasks)
      NPAR0 = round(np.sqrt(ntasks))
      NPAR = NPAR0
      res = ntasks % NPAR

      dN_list = [-1, 1]
      idN = 0
      dNf = 1
      while res != 0:
         NPAR = NPAR0 + dN_list[idN]*dNf

         idN += 1
         if idN > 1:
            idN = 0
            dNf += 1

         res = ntasks % NPAR

      if ntasks%self.ntasks_per_node == 0:
         nodes_job = str(int(ntasks/self.ntasks_per_node))
      else:
         raise ValueError("ntasks chosen is not a multiple of default ntasks per node")

      self.io.job_parameters.nodes  = nodes_job
      self.io.INCAR.NPAR = str(int(NPAR))

      return