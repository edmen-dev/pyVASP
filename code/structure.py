class structure:
    """
    Class to set properties of the crystal structure.
    """

    def __init__(self, verbose):

        self.verbose = verbose
        
        ###############################################################################
        # Set default inputs

        # properties
        self._kpoints = "12 12 12"
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

    

# Deprecated:

    # @property
    # def cell(self):
    #     return self._cell
    # @cell.setter
    # def cell(self, new_val):
    #     self._cell = new_val

    # def prepare_structure(self, structure):

    #     self.elements  = structure.get_chemical_symbols()
    #     self.species   = list( structure.symbols.species() )
    #     self.positions = structure.positions

    #     return


        # self.cell = structure.cell.array
        
        # elements_reduced_buf = []
        # for element_reduced in list(dict.fromkeys(self.elements)):
        #     elements_reduced_buf.append([element_reduced, self.elements.count(element_reduced)])
        # self.elements_reduced = elements_reduced_buf.copy()