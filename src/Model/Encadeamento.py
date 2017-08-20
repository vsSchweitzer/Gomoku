from Model.Coordenada import Coordenada
from Model.Direcao import Direcao

class Encadeamento:

	__coordenadas = None
	__aberturas = None
	__jogador = None
	__direcao = None

	def __init__(self, numJogador, direcao):
		self.__coordenadas = []
		self.__aberturas = 0
		self.__jogador = numJogador
		self.__direcao = direcao

	def addPonto(self, novaCoordenada):
		self.__coordenadas.append(novaCoordenada)

	def getPontos(self):
		return (pow(len(self.__coordenadas), 2) * self.__aberturas)