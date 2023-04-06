from VASP_job.dataclass_inputs import RWIGS_parameters, standard_INCAR_parameters, constr_INCAR_parameters, constr_INCAR_parameters_flag5

class set_inputs:
    """
    Class to set different VASP inputs.
    """

    def __init__(self, dictionary_RWIGS, dictionary_standard_INCAR_parameters):
        """
        dictionary_RWIGS and dictionary_standard_INCAR_parameters are dictionaries
        containing input information for RWIGS and standard variables in INCAR, respectively.
        """
        # property: automatically calls getters and setters accordingly 
        self._dictionary_RWIGS = dictionary_RWIGS.copy()
        self._dictionary_standard_INCAR_parameters = dictionary_standard_INCAR_parameters.copy()
        return

    @property
    def dictionary_RWIGS(self):
        return self._dictionary_RWIGS

    @property
    def dictionary_standard_INCAR_parameters(self):
        return self._dictionary_standard_INCAR_parameters