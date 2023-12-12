# dataclasses to describe VASP's parameters
from dataclasses import dataclass, field


###############################################################################
# INCAR-related

# INCAR parameters
@dataclass(frozen=False)
class INCAR:
    SYSTEM:        str = 'job'
    PREC:          str = 'Accurate'
    ALGO:          str = 'Fast'
    ISTART:        str = '0'
    ICHARG:        str = '2'
    LREAL:         str = '.FALSE.'
    LWAVE:         str = '.FALSE.'
    LCHARG:        str = '.TRUE.'
    LORBIT:        str = '11'
    ISMEAR:        str = '1'
    SIGMA:         str = '0.03'
    ISPIN:         str = '2'
    ENCUT:         str = '500'
    EDIFF:         str = '1e-5'
    NELM:          str = '200'
    LMAXMIX:       str = '6'
    LNONCOLLINEAR: str = '.TRUE.'
    NPAR:          str = '5'
    ISYM:          str = '2'

# INCAR_constr parameters
@dataclass(frozen=False)
class INCAR_constr:
    I_CONSTRAINED_M: str = '4'
    LAMBDA:          str = '1'

# INCAR_constr_flag5 parameters
@dataclass(frozen=False)
class INCAR_constr_flag5:
    B_MIX:            str = '1.0'
    B_ref:            str = '0.02'
    N_MIX:            str = '4'
    E_PENALTY_MAX:    str = '3.8'
    LAMBDA_FIELD_MAX: str = '1e-3'

# INCAR_relaxation parameters
@dataclass(frozen=False)
class INCAR_relaxation:
    IBRION: str = '2'
    ISIF:   str = '3'
    NSW:    str = '100'
    EDIFFG: str = '-0.01'

###############################################################################
# Structure-related

# RWIGS parameters
@dataclass(frozen=False)
class RWIGS:
    N:  str = '0.979'
    Mn: str = '1.323'
    Fe: str = '1.164'
    Ni: str = '1.058'
    Ga: str = '1.217'
    
# potential_files
@dataclass(frozen=False)
class potential_files:
    N:  str = 'N'
    Mn: str = 'Mn_pv'
    Fe: str = 'Fe_pv'
    Ni: str = 'Ni_pv'
    Ga: str = 'Ga_d'


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



#deprecated

# ###############################################################################
# # MAGNETIC INPUTS: MAGDIRS / BETAHS / BCONSTR

# # job_script_parameters
# @dataclass(frozen=False)
# class magnetic_inputs:
#     """
#     You should provide:
#     - magdirs (list of vectors)
#     - betahs (list of floats (use False or None to deactivate DLM mode at a specific site))
#     - B_CONSTRs (list of vectors, only for flag 5)
#     """
#     magdirs:   bool = False
#     ms:        bool = False
#     betahs:    bool = False
#     B_CONSTRs: bool = False