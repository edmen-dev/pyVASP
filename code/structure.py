class structure:
    """
    Class to set properties of the crystal structure.
    """

    def __init__(self, verbose):

        self.verbose = verbose
        
        ###############################################################################
        # Set default inputs

        # properties
        self._kpoints  = "12 12 12"
        self._species  = [] # all species (without repetition)
        self._elements = [] # all atoms

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
    def species(self):
        return self._species
    @species.setter
    def species(self, new_val):
        self._species = new_val

    @property
    def elements(self):
        return self._elements
    @elements.setter
    def elements(self, new_val):
        self._elements = new_val

    ###############################################################################
    # functionalities