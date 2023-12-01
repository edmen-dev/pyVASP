from VASP_job.code.dataclass_inputs import RWIGS_parameters, potential_files
from dataclasses import dataclass, fields

class structure:
    """
    Class to set properties of the crystal structure.
    """

    def __init__(self,
                 potential_path,
                 KPOINTS_file,
                 POTCAR_file,
                 POSCAR_file,
                 verbose):
        """
        RWIGS_parameters and potential_files are dataclasses
        containing input information for RWIGS and standard variables in INCAR, respectively.
        """
        
        self.potential_path = potential_path
        self.KPOINTS_file   = KPOINTS_file
        self.POTCAR_file    = POTCAR_file
        self.POSCAR_file    = POSCAR_file
        self.verbose        = verbose
        
        ###############################################################################
        # Set default inputs

        # dataclasses
        self.RWIGS_parameters = RWIGS_parameters()
        self.potential_files  = potential_files()

        # properties
        self._kpoints = "1x1x1"
        self._elements = []

        ###############################################################################
        if self.verbose == "high":
            self.write_initialization_info()

        return

###############################################################################
    # Auxiliary methods for init
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
    
###############################################################################
    # main methods

    ###############################################################################
    # properties
    @property
    def kpoints(self):
        return self._kpoints
    @kpoints.setter
    def kpoints(self, new_val):
        self._kpoints = new_val

    @property
    def elements(self):
        return self._elements
    @elements.setter
    def elements(self, new_val):
        self._elements = new_val

    ###############################################################################
    # functionalities

    def prepare_structure(self, atoms):
        self.elements  = atoms["elements"].tolist()
        self.positions = atoms["positions"].tolist()
        self.elements = atoms["elements"].tolist()
        return

    def write_KPOINTS(self):
        with open(self.KPOINTS_file, "w") as text_file:
            text_file.write('KPOINTS created by VASP_job python class\n')
            text_file.write('0\n')
            text_file.write('Monkhorst_Pack\n')
            text_file.write(self._kpoints + '\n')
            text_file.write('0 0 0\n')
        return

    def write_POTCAR(self):
        with open(self.POTCAR_file, 'w') as text_file:
            for element in self._elements:
                potential = self.potential_path + getattr(self.potential_files, element) + "/POTCAR"
                with open(potential) as f:
                    potential_text = f.readlines()
                for i in potential_text:
                    text_file.write(i)
        return

    def write_POSCAR(self):
        with open(self.POSCAR_file, 'w') as text_file:
            text_file.write("TODO")
        return