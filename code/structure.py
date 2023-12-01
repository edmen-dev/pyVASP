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
        self._elements_reduced = []

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

    @property
    def elements_reduced(self):
        return self._elements_reduced
    @elements_reduced.setter
    def elements_reduced(self, new_val):
        self._elements_reduced = new_val

    ###############################################################################
    # functionalities

    def prepare_structure(self, lattice, atoms):
        self.lattice_vectors = []
        self.lattice_vectors.append(lattice["avec"])
        self.lattice_vectors.append(lattice["bvec"])
        self.lattice_vectors.append(lattice["cvec"])

        self.elements  = atoms["elements"].tolist()
        self.positions = atoms["positions"].tolist()
        elements_reduced_buf = []
        for element_reduced in list(dict.fromkeys(self.elements)):
            elements_reduced_buf.append([element_reduced, self.elements.count(element_reduced)])
        self.elements_reduced = elements_reduced_buf.copy()
        return