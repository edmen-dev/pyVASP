import os
from VASP_job.set_inputs import set_inputs

class VASP_job:
    """
    Main functionality of the module.
    """

    def __init__(self,
                executable_path=os.path.expanduser('~') + '/workbench/devel/codes/VASP/vasp.5.4.4/bin/',
                executable_name='vasp_ncl',
                output_file_name='out',
                verbose='normal'):
    
        # Check on chosen verbose
        if verbose != 'low' and verbose != 'normal' and verbose != 'high':
            print('WARNING: be aware that you have not selected an available value for verbose.')
            self._verbose = 'normal'
            print('verbose has been set to default: normal')
        else:
            self._verbose = verbose

        # Checking path for the executables
        # Fixing "/" in the executable path if necessary
        if executable_path[-1] != '/':
            self._executable_path = executable_path + '/'
        else:
            self._executable_path = executable_path