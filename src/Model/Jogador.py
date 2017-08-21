from enum import Enum

class Jogador(Enum):
	UM = 1
	DOIS = 2

	def jogadorOposto(self):
		if self == Jogador.UM:
			return Jogador.DOIS
		else:
			return Jogador.UM
