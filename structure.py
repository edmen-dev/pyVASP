class structure:
    """
    Class to set the crystal structure.
    """

    def __init__(self,
                 potential_path,
                 potential_files,
                 POTCAR_file):
        """
        dictionary_RWIGS and dictionary_standard_INCAR_parameters are dictionaries
        containing input information for RWIGS and standard variables in INCAR, respectively.
        """
        
        self.potential_path  = potential_path
        self.potential_files = potential_files
        self.POTCAR_file = POTCAR_file
        
        
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