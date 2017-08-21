class Coordenada:

	x = None
	y = None

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def adjacenteA(self, coord):
		return (abs(self.x - coord.x) <= 1) and (abs(self.y - coord.y) <= 1)

	# Sobrecarga do operador ==
	def __eq__(self, other):
		if isinstance(other, Coordenada):
			return ((self.x == other.x) and (self.y == other.y))
		else:
			return NotImplemented

	# Sobrecarga do operador !=
	def __ne__(self, other):
		eq = self.__eq__(other)
		if eq == NotImplemented:
			return eq
		else:
			return not eq