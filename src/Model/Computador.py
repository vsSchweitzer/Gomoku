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

	def __init__(self, dificuldade=3, jogador=Jogador.DOIS):
		self.__dificuldade = dificuldade
		self.__jogador = jogador

	def getProximaJogada(self, tabuleiroAtual):
		self.__numIteracoes = 0
		tempoInicial = time.time()
		coord = self.alpha_beta(tabuleiroAtual, self.__dificuldade)[0]
		self.__tempoUltimaJogada = round(time.time() - tempoInicial, 2)
		return coord

	def alpha_beta(self, tabuleiro, profundidade, eJogadorMax=True, alpha=(-math.inf), beta=math.inf):
		self.__numIteracoes += 1
		melhorValor = None
		jogada = None

		if profundidade == 0:
			#print("Volta")
			return (None ,tabuleiro.getHeuristica())
		else:
			if eJogadorMax:
				melhorValor = alpha

				listaJogadasPossiveis = tabuleiro.getJogadasPossiveis()
				for coord in listaJogadasPossiveis:
					#if self.__numIteracoes >= 3125:
					#	print("Agora")
					tabuleiro.adicionarPeca(coord, self.__jogador)

					#novoEstado = tabuleiro.getFilho(coord, self.__jogador)

					valorFilho = self.alpha_beta(tabuleiro, profundidade - 1, False, melhorValor, beta)[1]

					tabuleiro.removerPeca(coord)

					if melhorValor < valorFilho:
						melhorValor = valorFilho
						jogada = coord

					if beta <= melhorValor:
						break
			else:
				melhorValor = beta

				listaJogadasPossiveis = tabuleiro.getJogadasPossiveis()
				for coord in listaJogadasPossiveis:
					tabuleiro.adicionarPeca(coord, self.__jogador.jogadorOposto())

					#novoEstado = tabuleiro.getFilho(coord, self.__jogador.jogadorOposto())

					valorFilho = self.alpha_beta(tabuleiro, profundidade - 1, True, alpha, melhorValor)[1]

					tabuleiro.removerPeca(coord)

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
