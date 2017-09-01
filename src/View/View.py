from tkinter import *
import math


class View:

	__controller = None

	__root = None
	__frame_menuPrincipal = None
	__frame_jogo = None
	__canvas_tabuleiro = None

	__horSpaces = None
	__vertSpaces = None

	__frameIteracoes = None

	__opcaoAdversario1 = None
	__opcaoAdversario2 = None
	__opcaoPrimeiro = None
	__textoJogadorDaVez = None
	__scoreJ1 = None
	__scoreJ2 = None
	__iteracoesMinMax = None
	__tempoMinMax = None
	__profundidade = None
	__tempoEsperado = None

	def __init__(self, controller, horSpaces, vertSpaces):
		self.__controller = controller
		self.__horSpaces = horSpaces
		self.__vertSpaces = vertSpaces

		self.__root = Tk()
		self.__root.title("Gomoku - Dunia e Vinicius")
		self.__root.resizable(width=False, height=False)
		self.__root.minsize(width=800, height=600)

		self.__opcaoAdversario1 = IntVar()
		self.__opcaoAdversario2 = IntVar()
		self.__opcaoAdversario2.set(1)
		self.__opcaoPrimeiro = IntVar()
		self.__textoJogadorDaVez = StringVar()
		self.__scoreJ1 = IntVar()
		self.__scoreJ2 = IntVar()
		self.__iteracoesMinMax = IntVar()
		self.__tempoMinMax = IntVar()
		self.__profundidade = IntVar()
		self.__profundidade.set(2)
		self.__tempoEsperado = StringVar()
		self.updateTempoEsperado()

		self.initializeMainMenu()
		self.initializeGameMenu()

		self.displayMainMenu(True)
		self.displayGameMenu(False)

	def mainLoop(self):
		self.__root.mainloop()

	def initializeMainMenu(self):
		separatorSpace = 10
		self.__frame_menuPrincipal = Frame(self.__root)

		frame_titulo = Frame(self.__frame_menuPrincipal)
		frame_titulo.grid(row=0)
		Label(frame_titulo, text="Gomoku").grid(row=0)
		Label(frame_titulo, text="Por: Dúnia Marchiori e Vinicius Steffani Schweitzer").grid(row=1)

		Frame(self.__frame_menuPrincipal).grid(row=1, pady=separatorSpace) # Separator

		frame_escolhaJogadores = Frame(self.__frame_menuPrincipal)
		frame_escolhaJogadores.grid(row=2)

		#Label(frame_escolhaOponente, text="Você é o Jogador 1").grid(row=0, columnspan=2)
		Label(frame_escolhaJogadores, text="Escolha o Jogador 1:").grid(row=1, columnspan=2)
		radio_p1H = Radiobutton(frame_escolhaJogadores, text="Humano", var=self.__opcaoAdversario1, value=0)
		radio_p1H.grid(row=2, column=0)
		radio_p1PC = Radiobutton(frame_escolhaJogadores, text="Computador", var=self.__opcaoAdversario1, value=1)
		radio_p1PC.grid(row=2, column=1)

		Label(frame_escolhaJogadores, text="Escolha o Jogador 2:").grid(row=3, columnspan=2)
		radio_p1H = Radiobutton(frame_escolhaJogadores, text="Humano", var=self.__opcaoAdversario2, value=0)
		radio_p1H.grid(row=4, column=0)
		radio_p1PC = Radiobutton(frame_escolhaJogadores, text="Computador", var=self.__opcaoAdversario2, value=1)
		radio_p1PC.grid(row=4, column=1)

		Frame(self.__frame_menuPrincipal).grid(row=3, pady=separatorSpace)  # Separator

		frame_escolhaPrimeiro = Frame(self.__frame_menuPrincipal)
		frame_escolhaPrimeiro.grid(row=4)

		Label(frame_escolhaPrimeiro, text="Escolha quem será o primeiro:").grid(row=0, columnspan=2)
		radio_1Comeca = Radiobutton(frame_escolhaPrimeiro, text="Jogador 1", var=self.__opcaoPrimeiro, value=0)
		radio_1Comeca.grid(row=1, column=0)
		radio_2Comeca = Radiobutton(frame_escolhaPrimeiro, text="Jogador 2", var=self.__opcaoPrimeiro, value=1)
		radio_2Comeca.grid(row=1, column=1)

		Frame(self.__frame_menuPrincipal).grid(row=5, pady=separatorSpace)  # Separator

		frame_profundidade = Frame(self.__frame_menuPrincipal)
		frame_profundidade.grid(row=6)
		opcoesProfundidade = 4
		Label(frame_profundidade, text="Escolha a profundidade da busca da IA (Recomendado: 2):").grid(row=0, columnspan=opcoesProfundidade)
		for i in range(1, opcoesProfundidade+1):
			radio_prof = Radiobutton(frame_profundidade, text=str(i), var=self.__profundidade, value=i, command=self.updateTempoEsperado)
			radio_prof.grid(row=1, column=i-1)

		frame_tempoEsperado = Frame(frame_profundidade)
		frame_tempoEsperado.grid(row=2, columnspan=opcoesProfundidade)
		Label(frame_tempoEsperado, text="Tempo esperado:").grid(row=0, column=0)
		Label(frame_tempoEsperado, textvariable=self.__tempoEsperado).grid(row=0, column=1)

		Frame(self.__frame_menuPrincipal).grid(row=7, pady=separatorSpace)  # Separator

		frame_comecarJogo = Frame(self.__frame_menuPrincipal)
		frame_comecarJogo.grid(row=8)
		btn_comecar = Button(frame_comecarJogo, text="Começar o Jogo")
		btn_comecar.bind("<Button-1>", self.__controller.CB_botaoComecarJogo)
		btn_comecar.grid()

	def displayMainMenu(self, doDisplay):
		if doDisplay:
			self.__frame_menuPrincipal.pack(expand=True)
		else:
			self.__frame_menuPrincipal.pack_forget()

	def initializeGameMenu(self):
		separatorSpace = 20
		self.__frame_jogo = Frame(self.__root)

		frame_tabuleiro = Frame(self.__frame_jogo, bd=5, relief=SUNKEN)
		frame_tabuleiro.grid(row=0, column=0, rowspan=2, sticky=N+S+E+W)
		self.__canvas_tabuleiro = Canvas(frame_tabuleiro, width=525, height=525, bg="lemon chiffon")
		self.__canvas_tabuleiro.bind("<Button-1>", self.boardClick)
		#self.__canvas_tabuleiro.bind("<Button-3>", self.boardClickR)  # Metodo de debug, permite remover peças com o botão direito
		self.__canvas_tabuleiro.grid()

		Frame(self.__frame_jogo).grid(row=0, column=1, padx=10)  # Separator

		frame_info = Frame(self.__frame_jogo, bd=5, relief=SUNKEN)
		frame_info.grid(row=0, column=2, sticky=N)
		Label(frame_info, text="Jogador da vez:").grid(row=0, column=0, columnspan=2)
		Label(frame_info, textvariable=self.__textoJogadorDaVez).grid(row=1, column=0, columnspan=2)

		Frame(frame_info).grid(row=2, columnspan=2, pady=separatorSpace)  # Separator

		Label(frame_info, text="Pontuação").grid(row=3, column=0, columnspan=2)
		Label(frame_info, text="Jogador 1:").grid(row=4, column=0, padx=10)
		Label(frame_info, textvariable=self.__scoreJ1).grid(row=5, column=0)
		Label(frame_info, text="Jogador 2:").grid(row=4, column=1, padx=10)
		Label(frame_info, textvariable=self.__scoreJ2).grid(row=5, column=1)

		self.__frameIteracoes = Frame(frame_info)
		self.__frameIteracoes.grid(row=7, columnspan=2)
		Frame(self.__frameIteracoes).grid(row=0, columnspan=2, pady=separatorSpace)  # Separator
		Label(self.__frameIteracoes, text="Dados da última chamada\ndo MinMax:").grid(row=1,columnspan=2)
		Label(self.__frameIteracoes, text="Iterações: ").grid(row=2, column=0, padx=10)
		Label(self.__frameIteracoes, textvariable=self.__iteracoesMinMax).grid(row=3, column=0)
		Label(self.__frameIteracoes, text="Tempo(s): ").grid(row=2, column=1, padx=10)
		Label(self.__frameIteracoes, textvariable=self.__tempoMinMax).grid(row=3, column=1)
		#self.__frameIteracoes.grid_remove() # Frame Escondido

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

	def hideIAStats(self):
		self.__frameIteracoes.grid_remove()

	def boardClick(self, event):
		pxSquareWidth = int(self.__canvas_tabuleiro.cget("width"))/self.__horSpaces
		pxSquareHeight = int(self.__canvas_tabuleiro.cget("height"))/self.__vertSpaces
		casaX = max(0, min(math.floor(event.x / pxSquareWidth), self.__horSpaces - 1))
		casaY = max(0, min(math.floor(event.y / pxSquareHeight), self.__vertSpaces - 1))
		self.__controller.CB_clicarTabuleiro(casaX, casaY)

	def boardClickR(self, event):
		pxSquareWidth = int(self.__canvas_tabuleiro.cget("width"))/self.__horSpaces
		pxSquareHeight = int(self.__canvas_tabuleiro.cget("height"))/self.__vertSpaces
		casaX = max(0, min(math.floor(event.x / pxSquareWidth), self.__horSpaces - 1))
		casaY = max(0, min(math.floor(event.y / pxSquareHeight), self.__vertSpaces - 1))
		self.__controller.CB_remover(casaX, casaY)

	def getTipoAdversarios(self):
		return self.__opcaoAdversario1.get(), self.__opcaoAdversario2.get()

	def getJogadorInicial(self):
		return (self.__opcaoPrimeiro.get() + 1)

	def getProfundidade(self):
		return self.__profundidade.get()

	def updateTempoEsperado(self):
		texto = "~ "
		profundidade = self.__profundidade.get()
		if profundidade == 1:
			texto += "0.07s"
		elif profundidade == 2:
			texto += "0.70s"
		elif profundidade == 3:
			texto += "10.00s"
		elif profundidade == 4:
			texto += "60.00s"
		self.__tempoEsperado.set(texto)

	def irParaJogo(self):
		self.displayMainMenu(False)
		self.displayGameMenu(True)

	def setJogadorDaVez(self, numJogador, isIA):
		jogador = "Jogador "
		if numJogador == 1:
			jogador += "1\nBranco"
		else:
			jogador += "2\nPreto"

		if isIA:
			jogador += " (Pensando...)"
		self.__textoJogadorDaVez.set(jogador)

	def setPontuacao(self, pontuacao, jogador):
		if jogador == 1:
			self.__scoreJ1.set(pontuacao)
		else:
			self.__scoreJ2.set(pontuacao)

	def setIteracoesMinMax(self, iteracoes):
		self.__iteracoesMinMax.set(iteracoes)

	def setTempoMinMax(self, tempo):
		self.__tempoMinMax.set(tempo)

	def mostrarAreaVencedor(self, jogador):
		texto = "Jogador " + str(jogador) + " venceu!"

		#Frame(self.__frame_jogo).grid(row=1, column=1, padx=10)  # Separator

		frame_vencedor = Frame(self.__frame_jogo, bd=5, relief=SUNKEN)
		frame_vencedor.grid(row=1, column=2)
		Label(frame_vencedor, text=texto).grid(padx=10, pady=10)

	def updateGame(self):
		self.__root.update()
