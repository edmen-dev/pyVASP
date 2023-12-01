class structure:
    """
    Class to set properties of the crystal structure.
    """

    def __init__(self, verbose):

        self.verbose = verbose
        
        ###############################################################################
        # Set default inputs

        # properties
        self._kpoints = "1x1x1"
        self._elements = []

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
        return