from Model.Jogador import Jogador


class Computador(Jogador):

	# Quanto maior a dificuldade mais niveis da arvore serão explorados
	__dificuldade = None

	def __init__(self, dificuldade):
		__dificuldade = dificuldade

	def jogar(self, tabuleiroAtual):
		# self.alpha_beta(tabuleiro_atual, dificuldade, true)
		pass
