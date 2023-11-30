# dataclasses to describe VASP's parameters
from dataclasses import dataclass, field


###############################################################################
# INCAR-related

# standard_INCAR_parameters
@dataclass(frozen=False)
class standard_INCAR_parameters:
    SYSTEM:        str = 'my material #jobname'
    PREC:          str = 'Accurate'
    ALGO:          str = 'Fast'
    NPAR:          str = '8'
    LREAL:         str = '.FALSE.'
    LWAVE:         str = '.FALSE.'
    LCHARG:        str = '.TRUE.'
    LORBIT:        str = '10'
    ISMEAR:        str = '1'
    SIGMA:         str = '0.03'
    ISTART:        str = '0'
    ICHARG:        str = '2'
    ISPIN:         str = '2'
    ENCUT:         str = '500'
    EDIFF:         str = '1e-6'
    NELM:          str = '200'
    LMAXMIX:       str = '6'
    LNONCOLLINEAR: str = '.TRUE.'
    # ISYM:   str = '0'

# constr_INCAR_parameters
@dataclass(frozen=False)
class constr_INCAR_parameters:
    I_CONSTRAINED: str = '2'
    LAMBDA:        str = '1'

# constr_INCAR_parameters_flag5
@dataclass(frozen=False)
class constr_INCAR_parameters_flag5:
    B_MIX:            str = '1.0'
    B_ref:            str = '0.02'
    N_MIX:            str = '4'
    E_PENALTY_MAX:    str = '3.8'
    LAMBDA_FIELD_MAX: str = '1e-3'


###############################################################################
# Structure-related

# RWIGS_parameters
@dataclass(frozen=False)
class RWIGS_parameters:
    Mn: str = '1.323'
    N:  str = '0.979'
    Ga: str = '1.058'
    Ni: str = '1.058'
    
# potential_files
@dataclass(frozen=False)
class potential_files:
    Mn: str = 'Mn_pv'
    N:  str = 'N'
    Ga: str = 'Ga_d'
    Ni: str = 'Ni_pv'

    # # 'ISYM'    : '0',
    # 'IBRION'  : '-1'
    # })


###############################################################################
# job-related

# job_script_parameters
@dataclass(frozen=False)
class job_parameters:
    job_name:     str = 'job'
    partition:    str = 'p.cmfe'
    nodes:        str = '1'
    ntasks:       str = '40'
    constraint:   str = '\'[swi1|swi2|swi3|swi4|swi5|swi6|swi7|swe1|swe2|swe3|swe4|swe5|swe6|swe7]\''
    time:         str = '180'
    mem_per_cpu:  str = '3GB'
    output:       str = 'mpi-out.%j'
    error:        str = 'mpi-err.%j'
    get_user_env: str = 'L'