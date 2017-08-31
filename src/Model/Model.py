from Model.Tabuleiro import Tabuleiro
from Model.Adversario import Adversario
from Model.Jogador import Jogador
from Model.Coordenada import Coordenada
from Model.Computador import Computador


# Fachada para o modelo
class Model:

	__tabuleiroAtual = None
	__jogadorDaVez = None  # P1 ou P2
	__adversario1 = None  # Humano ou Computador
	__adversario2 = None  # Humano ou Computador
	__computador1 = None
	__computador2 = None

	def __init__(self, numLinhas, numColunas):
		self.__tabuleiroAtual = Tabuleiro(numLinhas, numColunas)
		self.__computador1 = Computador()
		self.__computador2 = Computador(jogador=Jogador.DOIS)

	def setAdversarios(self, adversario1, adversario2):
		self.__adversario1 = adversario1
		self.__adversario2 = adversario2

	def setJogadorDaVez(self, novoJogador):
		self.__jogadorDaVez = novoJogador

	def setDificuldade(self, dificuldade):
		self.__computador1.setDificuldade(dificuldade)
		self.__computador2.setDificuldade(dificuldade)

	def jogarHumano(self, x, y):
		coord = Coordenada(x, y)

		if self.adversarioDaVez() == Adversario.HUMANO and self.__tabuleiroAtual.espacoVazio(coord) and (not self.__tabuleiroAtual.getFimDeJogo()):
			self.__tabuleiroAtual.adicionarPeca(coord, self.__jogadorDaVez)
			self.passaVez()

	def jogarComputador(self):
		if self.adversarioDaVez() == Adversario.COMPUTADOR and (not self.__tabuleiroAtual.getFimDeJogo()):
			if self.__jogadorDaVez == Jogador.UM:
				jogadaPC = self.__computador1.getProximaJogada(self.__tabuleiroAtual)
			else:
				jogadaPC = self.__computador2.getProximaJogada(self.__tabuleiroAtual)

			self.__tabuleiroAtual.adicionarPeca(jogadaPC, self.__jogadorDaVez)
			self.passaVez()

	def adversarioDaVez(self):
		if self.__jogadorDaVez == Jogador.UM:
			adversariodaVez = self.__adversario1
		else:
			adversariodaVez = self.__adversario2
		return adversariodaVez

	def remover(self, x, y):
		coord = Coordenada(x, y)
		if not self.__tabuleiroAtual.espacoVazio(coord):
			self.__tabuleiroAtual.removerPeca(coord)

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

	def getStatusComputador(self):
		valor = 0 if self.__adversario1 == Adversario.HUMANO else 1
		valor += 0 if self.__adversario2 == Adversario.HUMANO else 1

		if valor == 0:  # Humano vs Humano
			iteracoes = 0
			tempo = 0
		elif valor == 1:  # Humano vs Computador
			if self.__adversario1 == Adversario.COMPUTADOR:
				iteracoes = self.__computador1.getIteracoes()
				tempo = self.__computador1.getTempo()
			else:
				iteracoes = self.__computador2.getIteracoes()
				tempo = self.__computador2.getTempo()

		else:  # Computador vs Computador
			if self.__jogadorDaVez.jogadorOposto() == Jogador.UM:
				iteracoes = self.__computador1.getIteracoes()
				tempo = self.__computador1.getTempo()
			else:
				iteracoes = self.__computador2.getIteracoes()
				tempo = self.__computador2.getTempo()

		return iteracoes, tempo

	def getFimDeJogo(self):
		return self.__tabuleiroAtual.getFimDeJogo()
