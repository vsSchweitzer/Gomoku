import math
import time
from Model.Jogador import Jogador
from Model.Coordenada import Coordenada


class Computador():

	# Quanto maior a dificuldade mais niveis da arvore serão explorados
	__dificuldade = None
	__jogador = None

	__numIteracoes = None
	__tempoUltimaJogada = None

	def __init__(self, dificuldade=2, jogador=Jogador.DOIS):
		self.__dificuldade = dificuldade
		self.__jogador = jogador

	def getProximaJogada(self, tabuleiroAtual):
		self.__numIteracoes = 0
		tempoInicial = time.time()
		coord = self.alpha_beta(tabuleiroAtual, self.__dificuldade)[0]
		self.__tempoUltimaJogada = round(time.time() - tempoInicial, 3)
		return coord

	def alpha_beta(self, tabuleiro, profundidade, eJogadorMax=True, alpha=(-math.inf), beta=math.inf):
		self.__numIteracoes += 1
		#melhorValor = None
		jogada = None

		if profundidade == 0 or tabuleiro.getFimDeJogo():
			#print("Volta")
			return (None ,self.getPontuacao(tabuleiro))
		else:
			if eJogadorMax:
				melhorValor = alpha

				listaJogadasPossiveis = tabuleiro.getJogadasPossiveis()
				for coord in listaJogadasPossiveis:

					estadoJogo = tabuleiro.getFimDeJogo()
					tabuleiro.adicionarPeca(coord, self.__jogador)

					valorFilho = self.alpha_beta(tabuleiro, profundidade - 1, False, melhorValor, beta)[1]

					tabuleiro.removerPeca(coord)
					tabuleiro.setFimDeJogo(estadoJogo)

					if melhorValor < valorFilho:
						melhorValor = valorFilho
						jogada = coord

					if beta <= melhorValor:
						break
			else:
				melhorValor = beta

				listaJogadasPossiveis = tabuleiro.getJogadasPossiveis()
				for coord in listaJogadasPossiveis:

					estadoJogo = tabuleiro.getFimDeJogo()
					tabuleiro.adicionarPeca(coord, self.__jogador.jogadorOposto())

					valorFilho = self.alpha_beta(tabuleiro, profundidade - 1, True, alpha, melhorValor)[1]

					tabuleiro.removerPeca(coord)
					tabuleiro.setFimDeJogo(estadoJogo)

					if melhorValor > valorFilho:
						melhorValor = valorFilho
						jogada = coord

					if melhorValor <= beta:
						break

		return (jogada, melhorValor)

	def getIteracoes(self):
		return self.__numIteracoes

	def getTempo(self):
		return self.__tempoUltimaJogada

	def getPontuacao(self, tabuleiro):
		if tabuleiro.getFimDeJogo():
			utilidade = 999999999
			if tabuleiro.getVencedor() is not self.__jogador:
				utilidade *= -1
			return utilidade
		else:
			pontuacaoP1, pontuacaoP2 = tabuleiro.getPontuacao()
			heuristica = pontuacaoP1 - pontuacaoP2
			if self.__jogador is not Jogador.UM:
				heuristica *= -1
			return heuristica

	def setDificuldade(self, dificuldade):
		self.__dificuldade = dificuldade