class Tabuleiro:

	__tabuleiro = None
	__encadeamentos = None

	def __init__(self, numLinhas, numColunas):
		self.__tabuleiro = []
		for i in range(numLinhas):
			self.__tabuleiro.append([])
			for j in range(numColunas):
				self.__tabuleiro[i].append(0)
		self.__encadeamentos = []

	def adicionarPeca(self, x, y, jogador):
		self.__tabuleiro[x][y] = jogador

	def getMatriz(self):
		return self.__tabuleiro

	def getValor(self, x, y):
		if x > len(self.__tabuleiro) or y > len(self.__tabuleiro[0]):
			return -1
		else:
			return self.__tabuleiro[x][y]

	def espacoVazio(self, x, y):
		return (self.__tabuleiro[x][y] == 0)

	def fimDeJogo(self):
		for enc in self.__encadeamentos:
			if enc.getComprimento() >= 5:
				return True
		return False
