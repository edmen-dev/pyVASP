import os
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

    def run_vasp(self):
        os.chdir(self.io.cwd)
        run("sbatch "+self.job_file, shell=True)
        return

    def prepare_calculation(self, atoms):
        # first sort atoms by elements
        atoms = atoms.sort_values("elements")

        # prepare structure
        self.structure.prepare_structure(atoms)
        # prepare magnetism
        self.magnetism.prepare_magnetism(atoms)

        # write files
        self.io.write_inputs_and_job(self.executable, self.potential_path,
                                     self.magnetism.magmoms, self.magnetism.B_CONSTRs,
							         self.structure.kpoints, self.structure.elements)

        return