from Model.Coordenada import Coordenada
from Model.Direcao import Direcao

class Encadeamento:

	__coordenadas = None
	__aberturas = None
	__jogador = None
	__direcao = None

	def __init__(self, numJogador, direcao, coordenadaInicial):
		self.__coordenadas = []
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
		return (pow(len(self.__coordenadas), 2) * self.__aberturas)

	def getComprimento(self):
		return len(self.__coordenadas)

	def reduzirAberturas(self, quant=1):
		self.__aberturas -= quant

	def setAberturas(self, aberturas):
		self.__aberturas = aberturas

	def mesclaEncadeamento(self, encadeamento):
		self.__coordenadas = self.__coordenadas + encadeamento.getCoordenadas()
