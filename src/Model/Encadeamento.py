from Model.Coordenada import Coordenada
from Model.Direcao import Direcao

class Encadeamento:

	__coordenadas = None
	__aberturas = None
	__jogador = None
	__direcao = None

	def __init__(self, numJogador, direcao, coordenadaInicial=None):
		self.__coordenadas = []
		if (coordenadaInicial is not None):
			self.__coordenadas.append(coordenadaInicial)
		self.__aberturas = 0
		self.__jogador = numJogador
		self.__direcao = direcao

	def adicionaCoordenada(self, novaCoordenada):
		self.__coordenadas.append(novaCoordenada)

	def getCoordenadas(self):
		return self.__coordenadas

	def getDirecao(self):
		return self.__direcao

	def getJogador(self):
		return self.__jogador

	def getPontuacao(self):
		if self.getComprimento() < 5:
			return (pow(self.getComprimento(), self.getComprimento()) * self.__aberturas)
		else:
			return 6250

	def getComprimento(self):
		return len(self.__coordenadas)

	def incrementarAberturas(self, quant=1):
		self.__aberturas += quant

	def reduzirAberturas(self, quant=1):
		self.__aberturas -= quant

	def setAberturas(self, aberturas):
		self.__aberturas = aberturas

	def getAberturas(self):
		return self.__aberturas

	def mesclaEncadeamento(self, encadeamento):
		self.__coordenadas = self.__coordenadas + encadeamento.getCoordenadas()
