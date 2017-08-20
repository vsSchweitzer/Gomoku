from View.View import View
from Model.Model import Model

class Controller:

	__model = None
	__view = None
	__callbacks = None

	def __init__(self, horSpaces, vertSpaces):
		self.__model = Model()
		self.__view = View(self, horSpaces, vertSpaces)

	def mainLoop(self):
		# PvP ou PvPC?

		# P1 começa?

		# Inicializa valores

		# ciclo principal do jogo
		pass

	# View Callbacks
	def CB_botaoComecarJogo(self, event):
		print("Jogo Começou")

	def CB_posicaoTabuleiro(self, x, y):
		print("O espaço do tabuleiro na posição", x, y, "foi clicado")
