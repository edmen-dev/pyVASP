# VASP_job
Python code to set inputs of VASP (DFT) jobs and manage outputs

# TODO
- Perhaps make a mixing for a class that interacts with pyiron
- use elements for input for magnetism and somehow synergise it
- Use default values if not defined in atoms: FOR EXAMPLE, IF BETAHS ARE NOT INTRUDUCED, THEY SHOULD BE FALSE
- Mix ase with magmoms?
- Add about crystal relaxation
- fill RWIGS and potential_list
- think about incorporation of betahs
- Everything scales well with supercell?
- Functions that you write to get magmoms, betahs, etc have them in vasp.magmoms
- the df should have magdirs instead of magmoms?
- Have rotations to get final magmom
- Final magmoms should be obtained for df!