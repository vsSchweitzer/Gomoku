from enum import Enum

class Direcao(Enum):
	DESALINHADA = -1           # Nao possui nenhuma dessas relações
	HORIZONTAL = 0             # -
	VERTICAL = 1               # |
	DIAGONAL_BARRA = 2         # /
	DIAGONAL_CONTRA_BARRA = 3  # \

	@staticmethod
	def getDirecao(coordA, coordB):
		if coordA.x == coordB.x:
			direcao = Direcao.VERTICAL
		elif coordA.y == coordB.y:
			direcao = Direcao.HORIZONTAL
		elif (coordA.x - coordA.y) == (coordB.x - coordB.y):
			direcao = Direcao.DIAGONAL_CONTRA_BARRA
		elif -(coordA.x - coordB.x) == (coordA.y - coordB.y):
			direcao = Direcao.DIAGONAL_BARRA
		else:
			direcao = Direcao.DESALINHADA
		return direcao