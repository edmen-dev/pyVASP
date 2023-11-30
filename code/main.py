import os
from subprocess import run
from dataclasses import dataclass, fields
from VASP_job.code.dataclass_inputs import standard_INCAR_parameters, constr_INCAR_parameters, constr_INCAR_parameters_flag5, job_parameters
from VASP_job.code.structure import structure

class VASP_job:
    """
    Main functionality of the module.
    """

    def __init__(self,
                cwd = os.getcwd(),
                executable_path  = '/u/edmen/workbench/devel/VASP/vasp.5.4.4-flag4/bin',
                executable_name  = 'vasp_ncl',
                potential_path   = '/u/edmen/workbench/devel/VASP/potentials/potpaw_PBE',
                job_script_name  = 'job',
                out_file         = 'out',
                verbose          = 'normal'):
    
        self.job_script_name = job_script_name
        self.out_file        = out_file

        ###############################################################################
        # Check on chosen verbose
        if verbose != 'low' and verbose != 'normal' and verbose != 'high':
            print('WARNING: be aware that you have not selected an available value for verbose.')
            self.verbose = 'normal'
            print('verbose has been set to default: normal')
        else:
            self.verbose = verbose
            
        ###############################################################################
        # Set working directory and files
        cwd = self.add_slash(cwd)
        self.cwd = cwd
        
        ###############################################################################
        # Set files
        self.set_files()

        ###############################################################################
        # Checking executable and potential paths
        # Fixing "/" in the executable path if necessary
        executable_path = self.add_slash(executable_path)
        potential_path  = self.add_slash(potential_path)
        self.executable_path = executable_path
        self.potential_path  = potential_path
        
        # Full executable path
        self.executable_name = executable_name
        self.executable = self.executable_path + self.executable_name
            
        assert os.path.exists(self.executable)     is True, "\nYour executable does not exist!\nYour executable is:\n"+self.executable
        assert os.path.exists(self.potential_path) is True, "\nYour potential path does not exist!\nYour potential path is:\n"+self.potential_path
            
        ###############################################################################
        # Set default inputs
        self.standard_INCAR_parameters      = standard_INCAR_parameters()
        self.constr_INCAR_parameters        = constr_INCAR_parameters()
        self.constr_INCAR_parameters_flag5  = constr_INCAR_parameters_flag5()
        self.job_parameters                 = job_parameters()
        
        ###############################################################################
        if self.verbose == "high":
            self.write_initialization_info()
        
        ###############################################################################
        # Initialising external classes
        self.structure = structure(self.potential_path,
                                   self.KPOINTS_file,
                                   self.POTCAR_file,
                                   self.POSCAR_file,
                                   self.verbose)

        return
    
    ###############################################################################
    # Auxiliary definitions

    def add_slash(self, path):
        if path[-1] != '/':
            path += '/'
        return path
    
    def write_initialization_info(self):
        print("\nYour executable is:")
        print("   "+self.executable)
        
        print("\nYour current working directory (cwd) is:")
        print("   "+self.cwd)
        
        print("\nYour INCAR parameters are:")
        self.write_fields(self.standard_INCAR_parameters)
            
        print("\nYour INCAR parameters for constraining fields are:")
        self.write_fields(self.constr_INCAR_parameters)
        self.write_fields(self.constr_INCAR_parameters_flag5)
            
        return
    
    def write_fields(self, dataclass_name):
        for field in fields(dataclass_name):
            print('   '+field.name, '=', getattr(dataclass_name, field.name))
        return
    
    def set_files(self):
        self.KPOINTS_file = self.cwd+'KPOINTS'
        self.POTCAR_file  = self.cwd+'POTCAR'
        self.POSCAR_file  = self.cwd+'POSCAR'
        self.INCAR_file   = self.cwd+'INCAR'
        self.job_file     = self.cwd+self.job_script_name
        return

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

    ###############################################################################
    # functionalities

    def add_INCAR_parameters(self, text_file):
        for field in fields(self.standard_INCAR_parameters):
            string = field.name + "="
            string += getattr(self.standard_INCAR_parameters, field.name) 
            string += "\n"
            text_file.write(string)
        return

    def write_INCAR(self):
        with open(self.INCAR_file, "w") as text_file:
            self.add_INCAR_parameters(text_file)

            # # Creating strings for INCAR for MAGMOMS and M_CONSTR
            # MAGMOM_string = 'MAGMOM= '
            # M_CONSTR_string = 'M_CONSTR= '
            # B_CONSTR_string = 'B_CONSTR= '
            # for i, orientation in enumerate(orientations):
            #     for idir in range(3):
            #         MAGMOM_string += ' ' + '{:.7f}'.format(orientation[idir])
            #         M_CONSTR_string += ' ' + '{:.7f}'.format(orientation[idir])
            #     MAGMOM_string += ' '
            #     M_CONSTR_string += ' '
            # # for i, B_CONSTR_value in enumerate(B_CONSTR_initial_values):
            # #     for idir in range(3):
            # #         B_CONSTR_string += ' ' + '{:.7f}'.format(B_CONSTR_value[idir])
            # #     B_CONSTR_string += ' '

            # text_file.write(MAGMOM_string + '\n')
        return

    def write_job(self):
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
            text_file.write("\n\nsrun "+self.executable+" > "+self.out_file)
            text_file.write("\n\nend_time=$(date +%s)  # Record the end time")
            text_file.write("\nduration=$((end_time - start_time))  # Calculate the duration in seconds")
            text_file.write("\n\n# Print the duration")
            text_file.write("\necho \"Job duration: $((duration/60)) minutes\"")

        return

    def write_inputs_and_job(self):
        self.write_INCAR()
        self.structure.write_KPOINTS()
        self.structure.write_POTCAR()
        self.structure.write_POSCAR()
        self.write_job()
        return

    def run_vasp(self):
        os.chdir(self.cwd)
        run("sbatch "+self.job_file, shell=True)
        return