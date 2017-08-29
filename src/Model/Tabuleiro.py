from Model.Coordenada import Coordenada
from Model.Direcao import Direcao
from Model.Encadeamento import Encadeamento
from Model.Jogador import Jogador


class Tabuleiro:

	__tabuleiro = None
	__encadeamentos = None

	__fimDeJogo = None
	__vencedor = None

	def __init__(self, numLinhas, numColunas):
		self.__tabuleiro = []
		for i in range(numLinhas):
			self.__tabuleiro.append([])
			for j in range(numColunas):
				self.__tabuleiro[i].append(0)
		self.__encadeamentos = []
		self.__fimDeJogo = False
		self.__vencedor = False

	def adicionarPeca(self, coord, jogador):
		#print("Adicionando: " + str(coord.x) + ", " + str(coord.y))
		self.__tabuleiro[coord.x][coord.y] = jogador.value
		self.verificaEncadeamentosNovaPeca(coord, jogador)

	def removerPeca(self, coord):
		#print("Removendo: " + str(coord.x) + ", " + str(coord.y))
		jogador = Jogador(self.getValor(coord))
		self.__tabuleiro[coord.x][coord.y] = 0
		self.verificaEncadeamentosRetiraPeca(coord, jogador)

	def getMatriz(self):
		return self.__tabuleiro

	def getValor(self, coord):
		if 0 <= coord.x < self.getLargura() and 0 <= coord.y < self.getAltura():
			return self.__tabuleiro[coord.x][coord.y]
		else:
			return -1

	def getLargura(self):
		return len(self.__tabuleiro)

	def getAltura(self):
		return len(self.__tabuleiro[0])

	def espacoVazio(self, coord):
		return (self.__tabuleiro[coord.x][coord.y] == 0)

	def getFimDeJogo(self):
		return self.__fimDeJogo

	def setFimDeJogo(self, novoEstado):
		self.__fimDeJogo = novoEstado

	def getVencedor(self):
		return self.__vencedor

	# Retorna o valor no tabuleiro na posição coordC seguindo a sequencia CoordA, CoordB, CoordC.
	def proximaPecaNaSequencia(self, CoordA, CoordB):
		coordC = self.proximaCoordNaSequencia(CoordA, CoordB)
		return self.getValor(coordC)

	# Retorna a coordenada da tabuleiro na posição coordC seguindo a sequencia CoordA, CoordB, CoordC.
	def proximaCoordNaSequencia(self, CoordA, CoordB):
		if CoordA.adjacenteA(CoordB):
			direcao = Direcao.getDirecao(CoordA, CoordB)
			if direcao == Direcao.HORIZONTAL:
				if CoordA.x > CoordB.x:
					coordC = Coordenada((CoordB.x - 1), CoordB.y)
				else:
					coordC = Coordenada((CoordB.x + 1), CoordB.y)
			elif direcao == Direcao.VERTICAL:
				if CoordA.y > CoordB.y:
					coordC = Coordenada(CoordB.x, (CoordB.y - 1))
				else:
					coordC = Coordenada(CoordB.x, (CoordB.y + 1))
			elif direcao == Direcao.DIAGONAL_BARRA:
				if CoordA.x > CoordB.x:
					coordC = Coordenada((CoordB.x - 1), (CoordB.y + 1))
				else:
					coordC = Coordenada((CoordB.x + 1), (CoordB.y - 1))
			else:  # Direcao.DIAGONAL_CONTRA_BARRA \
				if CoordA.x > CoordB.x:
					coordC = Coordenada((CoordB.x - 1), (CoordB.y - 1))
				else:
					coordC = Coordenada((CoordB.x + 1), (CoordB.y + 1))
			return coordC
		else:
			print("Coordenadas Não São Adjacentes")
			raise -1

	def verificaEncadeamentosNovaPeca(self, coordNova, jogador):
		for j in range(coordNova.y - 1, coordNova.y + 1):
			#if 0 <= j < self.getLargura():
			for i in range(coordNova.x - 1, coordNova.x + 2):
				if (j < coordNova.y) or (i < coordNova.x):  # (i != coordNova.x and j != coordNova.y) or (i != coordNova.x + 1 and j != coordNova.y)
					coordVizinha = Coordenada(i, j)
					valorVizinho = self.getValor(coordVizinha)

					direcao = Direcao.getDirecao(coordNova, coordVizinha)
					coordOposta = self.proximaCoordNaSequencia(coordVizinha, coordNova)
					valorOposto = self.getValor(coordOposta)

					if valorVizinho == 0:
						if valorOposto == 0:
							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(2)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == jogador.value:
							self.atualizaEncadeamento(coordNova, coordOposta, direcao, jogador)

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(1)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == -1:
							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(1)
							self.__encadeamentos.append(novoEncadeamento)

					elif valorVizinho == jogador.value:

						if valorOposto == 0:
							self.atualizaEncadeamento(coordNova, coordVizinha, direcao, jogador)

						elif valorOposto == jogador.value:
							encadeamento = self.atualizaEncadeamento(coordNova, coordVizinha, direcao, jogador)
							encadeamentoOposto = self.encontraEncadeamento(direcao, coordOposta, jogador, removerEnc=True)
							encadeamento.mesclaEncadeamento(encadeamentoOposto)
							#self.__encadeamentos.remove(encadeamentoOposto)
							aberturas = encadeamento.getAberturas() + encadeamentoOposto.getAberturas()
							if aberturas == 4:
								encadeamento.setAberturas(2)
							elif aberturas == 3:
								encadeamento.setAberturas(1)
							elif aberturas == 2:
								encadeamento.setAberturas(0)

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamento = self.atualizaEncadeamento(coordNova, coordVizinha, direcao, jogador)
							encadeamento.reduzirAberturas()

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

						elif valorOposto == -1:
							encadeamento = self.atualizaEncadeamento(coordNova, coordVizinha, direcao, jogador)
							encadeamento.reduzirAberturas()

					elif valorVizinho == jogador.jogadorOposto().value:

						if valorOposto == 0:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(1)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == jogador.value:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							encadeamento = self.atualizaEncadeamento(coordNova, coordOposta, direcao, jogador)
							encadeamento.reduzirAberturas()

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							encadeamentoAdversarioOposto = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversarioOposto.reduzirAberturas()

							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(0)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == -1:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(0)
							self.__encadeamentos.append(novoEncadeamento)

					elif valorVizinho == -1:

						if valorOposto == 0:
							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(1)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == jogador.value:
							encadeamento = self.atualizaEncadeamento(coordNova, coordOposta, direcao, jogador)
							encadeamento.reduzirAberturas()

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.reduzirAberturas()

							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(0)
							self.__encadeamentos.append(novoEncadeamento)

						elif valorOposto == -1:
							novoEncadeamento = Encadeamento(jogador, direcao, coordNova)
							novoEncadeamento.setAberturas(0)
							self.__encadeamentos.append(novoEncadeamento)

	def verificaEncadeamentosRetiraPeca(self, coordRemovida, jogador):
		for j in range(coordRemovida.y - 1, coordRemovida.y + 1):
			for i in range(coordRemovida.x - 1, coordRemovida.x + 2):
				if (j < coordRemovida.y) or (i < coordRemovida.x):
					coordVizinha = Coordenada(i, j)
					valorVizinho = self.getValor(coordVizinha)

					direcao = Direcao.getDirecao(coordRemovida, coordVizinha)
					coordOposta = self.proximaCoordNaSequencia(coordVizinha, coordRemovida)
					valorOposto = self.getValor(coordOposta)

					if valorVizinho == 0:
						if valorOposto == 0:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							# self.__encadeamentos.remove(encadeamento)
							# del encadeamento

						elif valorOposto == jogador.value:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							#del encadeamento

						elif valorOposto == -1:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							#del encadeamento

					elif valorVizinho == jogador.value:

						if valorOposto == 0:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)

						elif valorOposto == jogador.value:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

							novoEncVizinho = Encadeamento(jogador, direcao, coordVizinha)
							coordA = coordRemovida
							coordB = coordVizinha
							proxCoord = self.proximaCoordNaSequencia(coordA, coordB)
							while self.getValor(proxCoord) == jogador.value:
								novoEncVizinho.adicionaCoordenada(proxCoord)
								coordA = coordB
								coordB = proxCoord
								proxCoord = self.proximaCoordNaSequencia(coordA, coordB)
							else:
								if self.getValor(proxCoord) == 0:
									novoEncVizinho.setAberturas(2)
								else:
									novoEncVizinho.setAberturas(1)
							self.__encadeamentos.append(novoEncVizinho)

							novoEncOposto = Encadeamento(jogador, direcao, coordOposta)
							coordA = coordRemovida
							coordB = coordOposta
							proxCoord = self.proximaCoordNaSequencia(coordA, coordB)
							while self.getValor(proxCoord) == jogador.value:
								novoEncOposto.adicionaCoordenada(proxCoord)
								coordA = coordB
								coordB = proxCoord
								proxCoord = self.proximaCoordNaSequencia(coordA, coordB)
							else:
								if self.getValor(proxCoord) == 0:
									novoEncOposto.setAberturas(2)
								else:
									novoEncOposto.setAberturas(1)
							self.__encadeamentos.append(novoEncOposto)

						elif valorOposto == jogador.jogadorOposto().value:
							encadeamento = self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)
							encadeamento.incrementarAberturas()

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

						elif valorOposto == -1:
							encadeamento = self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)
							encadeamento.incrementarAberturas()

					elif valorVizinho == jogador.jogadorOposto().value:

						if valorOposto == 0:
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

						elif valorOposto == jogador.value:
							encadeamento = self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)
							encadeamento.incrementarAberturas()

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

						elif valorOposto == jogador.jogadorOposto().value:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

							encadeamentoAdversarioOposto = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversarioOposto.incrementarAberturas()

						elif valorOposto == -1:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordVizinha, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

					elif valorVizinho == -1:

						if valorOposto == 0:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

						elif valorOposto == jogador.value:
							encadeamento = self.encontraEncadeamento(direcao, coordRemovida, jogador, remover=True)
							encadeamento.incrementarAberturas()

						elif valorOposto == jogador.jogadorOposto().value:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador.jogadorOposto())
							encadeamentoAdversario.incrementarAberturas()

						elif valorOposto == -1:
							self.encontraEncadeamento(direcao, coordRemovida, jogador, removerEnc=True)
							#self.__encadeamentos.remove(encadeamento)
							# del encadeamento

	def atualizaEncadeamento(self, coordNova, coordVizinha, direcao, jogador):
		encadeamento = self.encontraEncadeamento(direcao, coordVizinha, jogador)
		encadeamento.adicionaCoordenada(coordNova)
		if encadeamento.getComprimento() >= 5:
			self.__fimDeJogo = True
			self.__vencedor = jogador
		return encadeamento

	def encontraEncadeamento(self, direcao, coord, jogador, remover=False, removerEnc=False):
		for i in range(0, len(self.__encadeamentos)):
			enc = self.__encadeamentos[i]
			if enc.getDirecao() == direcao and enc.getJogador() == jogador:
				coordenadas = enc.getCoordenadas()
				if direcao == Direcao.HORIZONTAL:
					if coordenadas[0].y == coord.y:
						for j in range(0, len(coordenadas)):
							if coord == coordenadas[j]:
								if remover:
									coordenadas.pop(j)
								if removerEnc:
									return self.__encadeamentos.pop(i)
								else:
									return enc

				elif direcao == Direcao.VERTICAL:
					if coordenadas[0].x == coord.x:
						for j in range(0, len(coordenadas)):
							if coord == coordenadas[j]:
								if remover:
									coordenadas.pop(j)
								if removerEnc:
									return self.__encadeamentos.pop(i)
								else:
									return enc

				elif direcao == Direcao.DIAGONAL_BARRA:
					if -(coordenadas[0].x - coord.x) == (coordenadas[0].y - coord.y):
						for j in range(0, len(coordenadas)):
							if coord == coordenadas[j]:
								if remover:
									coordenadas.pop(j)
								if removerEnc:
									return self.__encadeamentos.pop(i)
								else:
									return enc

				elif direcao == Direcao.DIAGONAL_CONTRA_BARRA:
					if (coordenadas[0].x - coordenadas[0].y) == (coord.x - coord.y):
						for j in range(0, len(coordenadas)):
							if coord == coordenadas[j]:
								if remover:
									coordenadas.pop(j)
								if removerEnc:
									return self.__encadeamentos.pop(i)
								else:
									return enc

	# Retorna uma tupla de 3 elementos: (Pontuacao P1, Pontuacao P2, Diferenca)
	def getPontuacao(self):
		totalP1 = 0
		totalP2 = 0
		for enc in self.__encadeamentos:
			if enc.getJogador() == Jogador.UM:
				totalP1 += enc.getPontuacao()
			else:
				totalP2 += enc.getPontuacao()
		return (totalP1, totalP2, totalP2-totalP1)

	def getHeuristica(self):
		return self.getPontuacao()[2]

	def getFilho(self, coord, jogador):
		filho = self.clone()
		filho.adicionarPeca(coord, jogador)
		return filho

	def getJogadasPossiveis(self):
		listaJogadas = []

		top = 0
		down = self.getAltura() -1
		left = 0
		right = self.getLargura() -1

		while True:
			for j in range(left, right + 1):
				coord = Coordenada(top, j)
				if self.getValor(coord) == 0:
					listaJogadas.append(coord)
			top += 1
			if (top > down) or (left > right):
				break

			for i in range(top, down + 1):
				coord = Coordenada(i, right)
				if self.getValor(coord) == 0:
					listaJogadas.append(coord)
				right -= 1
			if (top > down) or (left > right):
				break

			for j in range(left + 1, right):
				coord = Coordenada(down, j)
				if self.getValor(coord) == 0:
					listaJogadas.append(coord)
			down -= 1
			if (top > down) or (left > right):
				break

			for i in range(top + 1, down):
				coord = Coordenada(i, left)
				if self.getValor(coord) == 0:
					listaJogadas.append(coord)
			left += 1
			if (top > down) or (left > right):
				break

		listaJogadas.reverse()


		'''
		listaJogadas = []
		for i in range(0, self.getAltura()):
			for j in range(0, self.getLargura()):
				coord = Coordenada(i, j)
				if self.getValor(coord) == 0:
					listaJogadas.append(coord)
		'''
		return listaJogadas

	def clone(self):
		copia = Tabuleiro(self.getAltura(), self.getLargura())
		copia.__fimDeJogo = self.__fimDeJogo
		copia.__vencedor = self.__vencedor

		for enc in self.__encadeamentos:
			copia.__encadeamentos.append(enc.clone())

		for i in range(0, self.getAltura()):
			copia.__tabuleiro[i] = list(self.__tabuleiro[i])

		for i in range(0, self.getAltura()):
			for j in range(0, self.getLargura()):
				copia.__tabuleiro[i][j] = self.__tabuleiro[i][j]
		return copia