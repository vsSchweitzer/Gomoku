from View.View import View
from Model.Model import Model


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
		self.__model.setJogadorDaVez(self.__view.getJogadorInicial())
		self.__model.setAdversario(self.__view.getTipoAdversario())
		print("Jogo Começou")

	def CB_posicaoTabuleiro(self, x, y):
		print("O espaço do tabuleiro na posição", x, y, "foi clicado")
		self.__model.jogar(x, y)
		self.__view.drawBoard(self.__model.getMatriz())
