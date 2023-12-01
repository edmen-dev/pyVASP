import numpy as np
from scipy.optimize import minimize_scalar

class magnetism:
	"""
	Class to set magnetic properties.
	"""

	def __init__(self,
				 verbose,
				 default_magmom   = np.array([0, 0, 3]),
				 default_B_CONSTR = np.array([0, 0, 0])):
	  
		self.verbose = verbose

		# properties (set default values)
		self._number_atoms = 1
		self._magmoms  = []
		self._betahs = []
		self._B_CONSTRs = []
		for i in range(self._number_atoms):
			self._magmoms.append( default_magmom )
			self._betahs.append( False )
			self._B_CONSTRs.append( default_B_CONSTR )
	  
		return

###############################################################################
	# main methods

	###############################################################################
	# properties
	
	@property
	def number_atoms(self):
		return self._number_atoms
	@number_atoms.setter
	def number_atoms(self, new_val):
		self._number_atoms = new_val
	
	@property
	def magmoms(self):
		return self._magmoms
	@magmoms.setter
	def magmoms(self, new_val):
		self._magmoms = new_val
	
	@property
	def betahs(self):
		return self._betahs
	@betahs.setter
	def betahs(self, new_val):
		self._betahs = new_val
	
	@property
	def B_CONSTRs(self):
		return self._B_CONSTRs
	@B_CONSTRs.setter
	def B_CONSTRs(self, new_val):
		self._B_CONSTRs = new_val


	###############################################################################
	# functionalities

	def prepare_magnetism(self, atoms):
		self.number_atoms = len(atoms["elements"].tolist())

		self.magmoms   = atoms["magmoms"].tolist()
		self.betahs    = atoms["betahs"].tolist()
		self.B_CONSTRs = atoms["B_CONSTRs"].tolist()
		return

	def set_magmoms(self):
		self._magmoms = []
		for i in range(self._number_atoms):
			if i < self._number_magnetic_atoms:
				random_number = np.random.random()
				theta = self.get_theta_mag(random_number, self.betah)
				phi   = np.random.random() * 2*np.pi

				mux = np.sin(theta) * np.cos(theta) * self._mu
				muy = np.sin(theta) * np.sin(theta) * self._mu
				muz = np.cos(theta) * self._mu
				mu_dir = np.array( [mux, muy, muz] ) 
				self._magmoms.append( mu_dir )
			else:
				self._magmoms.append( np.array( [0, 0, 0] ) )

		return self._magmoms

	def get_theta_mag(self, random_number, betah, tol=1e-5):
		if betah > tol:
			return np.arccos(np.log(np.exp(betah)-2*random_number*np.sinh(betah))/betah)
		else:
			# GET RIGHT FORMULA!
			return np.arccos(np.log(np.exp(betah)-2*random_number*np.sinh(betah))/betah)


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

	def get_betah_from_order_parameter(self, order_parameter, maximum_value_of_betah = 1000, tolerance_of_order_parameter_for_inversion=1e-2):
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