from Model.Tabuleiro import Tabuleiro
from Model.Adversario import Adversario
from Model.Jogador import Jogador
from Model.Coordenada import Coordenada


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

	def jogar(self, x, y):
		coord = Coordenada(x, y)
		if self.__tabuleiroAtual.espacoVazio(coord):
			if ((self.__adversario == Adversario.HUMANO) or (self.__adversario == Adversario.COMPUTADOR and self.__jogadorDaVez == Jogador.UM)) and (not self.__tabuleiroAtual.getFimDeJogo()):
				self.__tabuleiroAtual.adicionarPeca(coord, self.__jogadorDaVez)
				self.passaVez()

			if (self.__adversario == Adversario.COMPUTADOR) and (not self.__tabuleiroAtual.getFimDeJogo()):
				#self.__computador.jogar(self.__tabuleiroArual)
				self.passaVez()

	def getVencedor(self):
		if self.__tabuleiroAtual.getFimDeJogo():
			return self.__tabuleiroAtual.getVencedor()
		else:
			return None

	def passaVez(self):
		self.__jogadorDaVez = Jogador.jogadorOposto(self.__jogadorDaVez)

	def getMatriz(self):
		return self.__tabuleiroAtual.getMatriz()

	def getJogadorDaVez(self):
		return self.__jogadorDaVez.value

	def getPontuacao(self):
		return self.__tabuleiroAtual.getPontuacao()
