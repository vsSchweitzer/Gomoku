from Jogador import Jogador


# Classe Computador que é um tipo de jogador.
class Computador(Jogador):

	# Quanto maior a dificuldade mais niveis da arvore serão explorados
	__dificuldade = 3

	def __init__(self, dificuldade):
		__dificuldade = dificuldade

	def jogar(self, tabuleiroAtual):
		# self.alpha_beta(tabuleiro_atual, dificuldade, true)
		pass
