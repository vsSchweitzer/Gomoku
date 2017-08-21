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
		self.__view.setJogadorDaVez(self.__view.getJogadorInicial())

		tipoAdversario = Adversario(self.__view.getTipoAdversario())
		self.__model.setAdversario(tipoAdversario)

		print("Jogo Começou")

	def CB_clicarTabuleiro(self, x, y):
		print("O espaço do tabuleiro na posição", x, y, "foi clicado")
		self.__model.jogar(x, y)

		vencedor = self.__model.getVencedor()
		if vencedor != None:
			self.__view.mostrarAreaVencedor(vencedor.value)

		jogadorDaVez = self.__model.getJogadorDaVez()
		self.__view.setJogadorDaVez(jogadorDaVez)

		pontuacao = self.__model.getPontuacao()
		self.__view.setPontuacao(pontuacao[0], 1)
		self.__view.setPontuacao(pontuacao[1], 2)

		self.__view.drawBoard(self.__model.getMatriz())
