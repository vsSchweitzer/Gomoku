from tkinter import *
import math
from Model.Adversario import Adversario



class View:

	__controller = None

	__root = None
	__frame_menuPrincipal = None
	__frame_jogo = None
	__canvas_tabuleiro = None

	__horSpaces = None
	__vertSpaces = None

	__opcaoAdversario = None
	__opcaoPrimeiro = None

	def __init__(self, controller, horSpaces, vertSpaces):
		self.__controller = controller
		self.__horSpaces = horSpaces
		self.__vertSpaces = vertSpaces

		self.__root = Tk()
		self.__root.title("Gomoku - Dunia e Vinicius")
		self.__root.resizable(width=False, height=False)
		self.__root.minsize(width=800, height=600)

		self.initializeMainMenu()
		self.initializeGameMenu()


		self.displayMainMenu(True)
		self.displayGameMenu(False)
		'''
		self.displayMainMenu(False)
		self.displayGameMenu(True)
		'''

	def mainLoop(self):
		self.__root.mainloop()

	def initializeMainMenu(self):
		separatorSpace = 10
		self.__frame_menuPrincipal = Frame(self.__root)

		frame_titulo = Frame(self.__frame_menuPrincipal)
		frame_titulo.grid(row=0)
		Label(frame_titulo, text="Gomoku").grid(row=0)
		Label(frame_titulo, text="Por: Dunia Marchiori e Vinicius Steffani Schweitzer").grid(row=1)

		Frame(self.__frame_menuPrincipal).grid(row=1, pady=separatorSpace) # Separator

		frame_escolhaOponente = Frame(self.__frame_menuPrincipal)
		frame_escolhaOponente.grid(row=2)
		self.__opcaoAdversario = IntVar()
		Label(frame_escolhaOponente, text="Você é o Jogador 1").grid(row=0, columnspan=2)
		Label(frame_escolhaOponente, text="Escolha o Jogador 2:").grid(row=1, columnspan=2)
		radio_pvp = Radiobutton(frame_escolhaOponente, text="Outro Jogador", var=self.__opcaoAdversario, value=0)
		radio_pvp.grid(row=2, column=0)
		radio_pvpc = Radiobutton(frame_escolhaOponente, text="PC", var=self.__opcaoAdversario, value=1, state=DISABLED)  # DISABLED para primeira versão
		radio_pvpc.grid(row=2, column=1)

		Frame(self.__frame_menuPrincipal).grid(row=3, pady=separatorSpace)  # Separator

		frame_escolhaPrimeiro = Frame(self.__frame_menuPrincipal)
		frame_escolhaPrimeiro.grid(row=4)
		self.__opcaoPrimeiro = IntVar()
		Label(frame_escolhaPrimeiro, text="Escolha quem sera o primeiro:").grid(row=0, columnspan=2)
		radio_pvp = Radiobutton(frame_escolhaPrimeiro, text="Jogador 1", var=self.__opcaoPrimeiro, value=0)
		radio_pvp.grid(row=1, column=0)
		radio_pvpc = Radiobutton(frame_escolhaPrimeiro, text="Jogador 2", var=self.__opcaoPrimeiro, value=1)
		radio_pvpc.grid(row=1, column=1)

		Frame(self.__frame_menuPrincipal).grid(row=5, pady=separatorSpace)  # Separator

		frame_comecarJogo = Frame(self.__frame_menuPrincipal)
		frame_comecarJogo.grid(row=6)
		btn_comecar = Button(frame_comecarJogo, text="Começar Jogo")
		btn_comecar.bind("<Button-1>", self.__controller.CB_botaoComecarJogo)
		btn_comecar.grid()

	def displayMainMenu(self, doDisplay):
		if doDisplay:
			self.__frame_menuPrincipal.pack(expand=True)
		else:
			self.__frame_menuPrincipal.pack_forget()

	def initializeGameMenu(self):
		separatorSpace = 10
		self.__frame_jogo = Frame(self.__root)

		frame_tabuleiro = Frame(self.__frame_jogo)
		frame_tabuleiro.grid(row=0, column=0)
		self.__canvas_tabuleiro = Canvas(frame_tabuleiro, width=525, height=525, bg="lemon chiffon")
		self.__canvas_tabuleiro.bind("<Button-1>", self.boardClick)
		self.__canvas_tabuleiro.grid()

		Frame(self.__frame_jogo).grid(row=0, column=1, padx=separatorSpace)  # Separator

		frame_info = Frame(self.__frame_jogo)
		frame_info.grid(row=0, column=2)
		Label(frame_info, text="Pontuação:").grid()

		self.drawGrid(thck=2)

	def displayGameMenu(self, doDisplay):
		if doDisplay:
			self.__frame_jogo.pack(expand=True)
		else:
			self.__frame_jogo.pack_forget()

	def drawGrid(self, thck=2):
		lineColor = "LemonChiffon4"
		larguraCanvas = int(self.__canvas_tabuleiro.cget("width"))
		espacoHorizontal = larguraCanvas / self.__horSpaces
		quantHorizontais = self.__horSpaces - 1

		larguraCanvas = int(self.__canvas_tabuleiro.cget("height"))
		espacoVertical = larguraCanvas / self.__vertSpaces
		quantVerticais = self.__vertSpaces - 1

		for i in range(quantHorizontais):
			posXLinha = espacoHorizontal * (i+1)
			self.__canvas_tabuleiro.create_line(posXLinha, 0, posXLinha, larguraCanvas + 10, width=thck, fill=lineColor)

		for i in range(quantVerticais):
			posYLinha = espacoVertical * (i+1)
			self.__canvas_tabuleiro.create_line(0, posYLinha, larguraCanvas + 10, posYLinha, width=thck, fill=lineColor)

	def drawBoard(self, matrix):
		stepX = int(self.__canvas_tabuleiro.cget("width")) / self.__horSpaces
		offsetX = stepX / 2

		stepY = int(self.__canvas_tabuleiro.cget("height")) / self.__vertSpaces
		offsetY = stepY / 2

		pieceRadius = (min(stepX, stepY) / 2) - 5

		self.__canvas_tabuleiro.delete("all")
		for i in range(len(matrix[0])):
			for j in range(len(matrix)):
				if matrix[i][j] == 1:
					# Pinta Branco
					posX = i * stepX + offsetX
					posY = j * stepY + offsetY
					self.drawCircle(posX, posY, pieceRadius, "white")
				elif matrix[i][j] == 2:
					# Pinta Preto
					posX = i * stepX + offsetX
					posY = j * stepY + offsetY
					self.drawCircle(posX, posY, pieceRadius, "black")
		self.drawGrid()

	def drawCircle(self, x, y, radius, color):
		self.__canvas_tabuleiro.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)

	def boardClick(self, event,):
		pxSquareWidth = int(self.__canvas_tabuleiro.cget("width"))/self.__horSpaces
		pxSquareHeight = int(self.__canvas_tabuleiro.cget("height"))/self.__vertSpaces
		casaX = max(0, min(math.floor(event.x / pxSquareWidth), self.__horSpaces - 1))
		casaY = max(0, min(math.floor(event.y / pxSquareHeight), self.__vertSpaces - 1))
		self.__controller.CB_posicaoTabuleiro(casaX, casaY)

	def getJogadorInicial(self):
		return (self.__opcaoPrimeiro.get() + 1)

	def getTipoAdversario(self):
		return Adversario(self.__opcaoAdversario.get())

	def irParaJogo(self):
		self.displayMainMenu(False)
		self.displayGameMenu(True)
