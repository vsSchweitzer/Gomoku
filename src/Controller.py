from View.View import *
from Model.Model import *


class Controller:

	__model = None
	__view = None
	__callbacks = None

	def __init__(self, numLinhas, numColunas):
		self.__view = View(self, numLinhas, numColunas)
		self.__model = Model(numLinhas, numColunas)
		self.__view.mainLoop()

	# View Callbacks:
	def CB_botaoComecarJogo(self, event):
		self.__view.irParaJogo()

		jogadorInicial = Jogador(self.__view.getJogadorInicial())
		self.__model.setJogadorDaVez(jogadorInicial)
		isIA = (self.__model.adversarioDaVez() == Adversario.COMPUTADOR)
		self.__view.setJogadorDaVez(self.__view.getJogadorInicial(), isIA)

		tipoAdversario1, tipoAdversario2 = self.__view.getTipoAdversarios()
		tipoAdversario1 = Adversario(tipoAdversario1)
		tipoAdversario2 = Adversario(tipoAdversario2)
		self.__model.setAdversarios(tipoAdversario1, tipoAdversario2)

		profundidade = self.__view.getProfundidade()
		self.__model.setDificuldade(profundidade)

		if tipoAdversario1 == Adversario.HUMANO and tipoAdversario2 == Adversario.HUMANO:
			self.__view.hideIAStats()
		else:
			self.atualizaJogo()
			self.jogarIA()

		print("Jogo Começou")

	def CB_clicarTabuleiro(self, x, y):
		print("O espaço do tabuleiro na posição", x, y, "foi clicado")
		self.jogarHumano(x, y)

	def CB_remover(self, x, y):
		print("O espaço do tabuleiro na posição", x, y, "foi clicado com o botão direito")
		self.__model.remover(x, y)
		self.atualizaJogo()

	def jogarHumano(self, x, y):
		self.__model.jogarHumano(x, y)
		self.atualizaJogo()
		if self.__model.adversarioDaVez() == Adversario.COMPUTADOR:
			self.jogarIA()

	def jogarIA(self):
		self.__model.jogarComputador()
		self.atualizaJogo()
		if self.__model.adversarioDaVez() == Adversario.COMPUTADOR and not self.__model.getFimDeJogo():
			self.jogarIA()

	def atualizaJogo(self):
		self.__view.drawBoard(self.__model.getMatriz())

		vencedor = self.__model.getVencedor()
		if vencedor != None:
			self.__view.mostrarAreaVencedor(vencedor.value)

		jogadorDaVez = self.__model.getJogadorDaVez()
		isIA = (self.__model.adversarioDaVez() == Adversario.COMPUTADOR)
		isPensando = isIA and not self.__model.getFimDeJogo()
		self.__view.setJogadorDaVez(jogadorDaVez, isPensando)

		pontuacaoP1, pontuacaoP2 = self.__model.getPontuacao()
		self.__view.setPontuacao(pontuacaoP1, 1)
		self.__view.setPontuacao(pontuacaoP2, 2)

		iteracoes = self.__model.getStatusComputador()[0]
		self.__view.setIteracoesMinMax(iteracoes)

		tempo = self.__model.getStatusComputador()[1]
		self.__view.setTempoMinMax(tempo)

		self.__view.updateGame()
