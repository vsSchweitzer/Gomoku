from Model.Tabuleiro import Tabuleiro
from Model.Adversario import Adversario


# Fachada para o modelo
class Model:

	__tabuleiroAtual = None
	__jogadorDaVez = None  # P1 ou P2
	__adversario = None  # Humano ou Computador

	def __init__(self, numLinhas, numColunas):
		self.__tabuleiroAtual = Tabuleiro(numLinhas, numColunas)

	def setJogadorDaVez(self, novoJogador):
		self.__jogadorDaVez = novoJogador

	def setAdversario(self, adversario):
		self.__adversario = adversario

	def processaTurno(self):
		if self.__adversario == Adversario.COMPUTADOR and self.__jogadorDaVez == 2:
			pass

	def jogar(self, x, y):
		if self.__tabuleiroAtual.espacoVazio(x,y):
			if (self.__adversario == Adversario.HUMANO) or (self.__adversario == Adversario.COMPUTADOR and self.__jogadorDaVez == 1):
				self.__tabuleiroAtual.adicionarPeca(x, y, self.__jogadorDaVez)
				self.passaVez()

			if self.__adversario == Adversario.COMPUTADOR:
				#self.__computador.jogar()
				self.passaVez()

	def passaVez(self):
		self.__jogadorDaVez = self.__jogadorDaVez + 1
		if self.__jogadorDaVez == 3:
			self.__jogadorDaVez = 1

	def getMatriz(self):
		return self.__tabuleiroAtual.getMatriz()