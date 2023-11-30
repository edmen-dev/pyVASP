from VASP_job.code.dataclass_inputs import RWIGS_parameters, potential_files
from dataclasses import dataclass, fields

class structure:
    """
    Class to set the crystal structure.
    """

    def __init__(self,
                 cwd,
                 potential_path,
                 verbose):
        """
        dictionary_RWIGS and dictionary_standard_INCAR_parameters are dictionaries
        containing input information for RWIGS and standard variables in INCAR, respectively.
        """
        
        self.cwd  = cwd
        self.potential_path  = potential_path
        self.verbose  = verbose
        
        ###############################################################################
        # Set files
        self.set_files()
        
        ###############################################################################
        # Set default inputs
        self.RWIGS_parameters = RWIGS_parameters()
        self.potential_files  = potential_files()

        ###############################################################################
        if self.verbose == "high":
            self.write_initialization_info()

        return

###############################################################################
    # Auxiliary definitions
    def write_initialization_info(self):
        print("\nYour RWIGS parameters are:")
        self.write_fields(self.RWIGS_parameters)
            
        print("\nYour potentials are:")
        self.write_fields(self.potential_files)
            
        return
    
    def write_fields(self, dataclass_name):
        for field in fields(dataclass_name):
            print('   '+field.name, '=', getattr(dataclass_name, field.name))
        return
    
    def set_files(self):
        self.POTCAR_file  = self.cwd+'POTCAR'
        self.POSCAR_file  = self.cwd+'POSCAR'
        self.KPOINTS_file = self.cwd+'KPOINTS'
        return
    
    ###############################################################################
    def set_elements(self, elements):
        self.elements = elements
        return

    def write_POTCAR(self):
        with open(self.POTCAR_file, 'w') as text_file:
            for element in self.elements:
                potential = self.potential_path + getattr(self.potential_files, element) + "/POTCAR"
                with open(potential) as f:
                    potential_text = f.readlines()
                for i in potential_text:
                    text_file.write(i)
        return