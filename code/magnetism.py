import numpy as np
from scipy.optimize import minimize_scalar

class magnetism:
   """
   Class to set magnetic properties.
   """

   def __init__(self,
             default_magdir   = np.array([0, 0, 1]),
             default_m        = 1.0, # No DLM is applied
             default_B_CONSTR = np.array([0, 0, 0]),
             verbose = "low"):

      self.default_magdir   = default_magdir
      self.default_m        = default_m
      self.default_B_CONSTR = default_B_CONSTR
      self.verbose = verbose
     
      return

###############################################################################
   # main methods

   ###############################################################################
   # properties


   ###############################################################################
   # functionalities

   def set_default_magnetic_inputs(self, structure_ase, number_of_atoms):
      
      if not "magdirs" in structure_ase.arrays:
         magdirs = []
         for i in range(number_of_atoms):
            magdirs.append(self.default_magdir)
         structure_ase.new_array("magdirs", magdirs, dtype=float)
      
      if not "ms" in structure_ase.arrays:
         ms = []
         for i in range(number_of_atoms):
            ms.append(self.default_m)
         structure_ase.new_array("ms", ms, dtype=float)
      
      if not "B_CONSTRs" in structure_ase.arrays:
         B_CONSTRs = []
         for i in range(number_of_atoms):
            B_CONSTRs.append(self.default_B_CONSTR)
         structure_ase.new_array("B_CONSTRs", B_CONSTRs, dtype=float)

      return structure_ase

   def set_betahs_from_ms(self, structure_ase, number_of_atoms):
      betahs = []
      ms = structure_ase.arrays["ms"]
      for i in range(number_of_atoms):
         if ms[i] == 1 or ms[i] is False or ms[i] is None:
            betahs.append( np.inf )
         else:
            betahs.append( self.get_betah_from_m( ms[i] ) )

      structure_ase.new_array("betahs", betahs, dtype=float)
      
      return structure_ase

   def set_magmoms(self, structure_ase, number_of_atoms):
      magmoms = []
      for i in range(number_of_atoms):
         this_m      = structure_ase.arrays["ms"][i]
         this_betah  = structure_ase.arrays["betahs"][i]
         this_magdir = structure_ase.arrays["magdirs"][i]

         if this_m is False or this_m is None or this_m==1:
            magmoms.append( this_magdir )
         else:
            random_number = np.random.random()
            theta = self.get_theta_mag(random_number, this_betah)
            phi   = np.random.random() * 2*np.pi

            mod = np.linalg.norm( this_magdir )
            mux = np.sin(theta) * np.cos(phi)
            muy = np.sin(theta) * np.sin(phi)
            muz = np.cos(theta)
            mu = mod * np.array( [mux, muy, muz] ) 

            # now rotate magmom:
            mu = self.rotate_magmom(mu, this_magdir)

            magmoms.append( mu )

      structure_ase.new_array("magmoms", magmoms, dtype=float)

      return structure_ase

   def get_theta_mag(self, random_number, betah, tol=1e-4):
      if betah > tol:
         return np.arccos(np.log(np.exp(betah)-2*random_number*np.sinh(betah))/betah)
      else:
         return np.arccos(1 - 2*random_number - 2*(random_number-1)*random_number*betah)

   def rotate_magmom(self, mu, magdir):
      mod = np.linalg.norm(magdir)
      theta = np.arccos(magdir[2]/mod)
      phi = np.arctan2(magdir[1], magdir[0])

      Rtheta = self.get_Rtheta(theta)
      Rphi = self.get_Rphi(phi)

      mu_rotated = np.dot(Rtheta, mu)
      mu_rotated = np.dot(Rphi, mu_rotated)

      return mu_rotated
   
   def get_Rtheta(self, angle):
      """
      rotation about y-axis
      """
      R = np.zeros((3,3))
      R[0,0] = np.cos(angle)
      R[0,2] = np.sin(angle)
      R[2,0] = -np.sin(angle)
      R[2,2] = np.cos(angle)
      R[1,1] = 1
      return R

   def get_Rphi(self, angle):
      """
      rotation about z-axis
      """
      R = np.zeros((3,3))
      R[0,0] = np.cos(angle)
      R[0,1] = -np.sin(angle)
      R[1,0] = np.sin(angle)
      R[1,1] = np.cos(angle)
      R[2,2] = 1
      return R


   ###############################################################################
   # DLM methods

   def get_magnetic_entropy(self, betah, kB=1, tol=1e-5):
      if abs(betah)<tol:
         return kB * (np.log(4*np.pi) - betah**2 /6 )
      else:
         return kB * (1 + np.log(4*np.pi*np.sinh(betah)/betah) - betah/np.tanh(betah))

   def get_m_from_betah(self, betah, tol=1e-5):
      if abs(betah)<tol:
         return betah/3
      else:
         return -1/betah + 1/np.tanh(betah)

   def get_betah_from_m(self, order_parameter, maximum_value_of_betah = 1000, tolerance_of_order_parameter_for_inversion=1e-2):
      def f(x, order_parameter):
         return ( 1 + x*( order_parameter-1/np.tanh(x) ) )**2

      if abs(order_parameter) < tolerance_of_order_parameter_for_inversion:
         betah = 3*order_parameter
      else:
         if order_parameter > 0:
            res = minimize_scalar(f, bounds=(0, maximum_value_of_betah),
                              args=(order_parameter), method='bounded')
            # res = minimize_scalar(f, args=(order_parameter), method='golden')
         else:
            res = minimize_scalar(f, bounds=(-maximum_value_of_betah, 0),
                              args=(order_parameter), method='bounded')
         betah = res.x

      return betah