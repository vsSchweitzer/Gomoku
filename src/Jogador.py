from abc import abstractmethod


# Classe Abstrata jogador.
class Jogador:

	@abstractmethod
	def jogar(self, tabuleiroAtual):
		pass
