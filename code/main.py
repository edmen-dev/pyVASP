import os
from VASP_job.code.dataclass_inputs import standard_INCAR_parameters, constr_INCAR_parameters, constr_INCAR_parameters_flag5
from VASP_job.code.structure import structure
from dataclasses import dataclass, fields

class VASP_job:
    """
    Main functionality of the module.
    """

    def __init__(self,
                cwd = os.getcwd(),
                executable_path = '/u/edmen/workbench/devel/VASP/vasp.5.4.4-flag4/bin',
                executable_name = 'vasp_ncl',
                potential_path  = '/u/edmen/workbench/devel/VASP/potentials/potpaw_PBE',
                output_file_name='out',
                verbose='normal'):
    
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
        
        ###############################################################################
        if self.verbose == "high":
            self.write_initialization_info()
        
        ###############################################################################
        # Initialising external classes
        self.structure = structure(self.cwd, self.potential_path, self.verbose)

            
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