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
							encadeamentoVizinho = self.encontraEncadeamento(direcao, coordVizinha, jogador)
							encadeamentoOposto = self.encontraEncadeamento(direcao, coordOposta, jogador, removerEnc=True)
							encadeamentoVizinho.mesclaEncadeamento(encadeamentoOposto)
							#self.__encadeamentos.remove(encadeamentoOposto)
							aberturas = encadeamentoVizinho.getAberturas() + encadeamentoOposto.getAberturas()
							if aberturas == 4:
								encadeamentoVizinho.setAberturas(2)
							elif aberturas == 3:
								encadeamentoVizinho.setAberturas(1)
							elif aberturas == 2:
								encadeamentoVizinho.setAberturas(0)
							self.atualizaEncadeamento(coordNova, coordVizinha, direcao, jogador)

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
		if encadeamento.getComprimento() >= 5 and not self.__fimDeJogo:
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
		return totalP1, totalP2

	def getJogadasPossiveis(self):
		listaJogadas = []

		linhaInicial = 0
		colunaInicial = 0
		linhaFinal = self.getAltura()
		colunaFinal = self.getLargura()

		while linhaInicial < linhaFinal and colunaInicial < colunaFinal:
			for i in range(colunaInicial, colunaFinal):
				coord = Coordenada(linhaInicial, i)
				if self.espacoVazio(coord):
					listaJogadas.append(coord)

			linhaInicial += 1

			for i in range(linhaInicial, linhaFinal):
				coord = Coordenada(i, colunaFinal-1)
				if self.espacoVazio(coord):
					listaJogadas.append(coord)

			colunaFinal -= 1

			if linhaInicial < linhaFinal:
				for i in range(colunaFinal-1, colunaInicial-1, -1):
					coord = Coordenada(linhaFinal-1, i)
					if self.espacoVazio(coord):
						listaJogadas.append(coord)

				linhaFinal -= 1

			if colunaInicial < colunaFinal:
				for i in range(linhaFinal-1, linhaInicial-1, -1):
					coord = Coordenada(i, colunaInicial)
					if self.espacoVazio(coord):
						listaJogadas.append(coord)

				colunaInicial += 1
		listaJogadas.reverse()
		return listaJogadas
