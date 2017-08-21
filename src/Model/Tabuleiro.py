from Model.Coordenada import Coordenada
from Model.Direcao import Direcao
from Model.Encadeamento import Encadeamento
from Model.Jogador import Jogador


class Tabuleiro:

	__tabuleiro = None
	__encadeamentos = None

	def __init__(self, numLinhas, numColunas):
		self.__tabuleiro = []
		for i in range(numLinhas):
			self.__tabuleiro.append([])
			for j in range(numColunas):
				self.__tabuleiro[i].append(0)
		self.__encadeamentos = []

	def adicionarPeca(self, coord, jogador):
		self.__tabuleiro[coord.x][coord.y] = jogador.value
		self.verificaEncadeamentos(coord, jogador)

	def getMatriz(self):
		return self.__tabuleiro

	def getValor(self, coord):
		if 0 <= coord.x < self.getLarguraTabuleiro() and 0 <= coord.y < self.getAlturaTabuleiro():
			return self.__tabuleiro[coord.x][coord.y]
		else:
			return -1

	def getLarguraTabuleiro(self):
		return len(self.__tabuleiro)

	def getAlturaTabuleiro(self):
		return len(self.__tabuleiro[0])

	def espacoVazio(self, coord):
		return (self.__tabuleiro[coord.x][coord.y] == 0)

	def fimDeJogo(self):
		for enc in self.__encadeamentos:
			if enc.getComprimento() >= 5:
				return True
		return False

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

	def verificaEncadeamentos(self, coordNova, jogador):
		for j in range(coordNova.y - 1, coordNova.y + 1):
			#if 0 <= j < self.getLarguraTabuleiro():
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
							encadeamentoOposto = self.encontraEncadeamento(direcao, coordOposta, jogador)
							encadeamento.mesclaEncadeamento(encadeamentoOposto)
							self.__encadeamentos.remove(encadeamentoOposto)

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
							encadeamentoAdversario = self.encontraEncadeamento(direcao, coordOposta, jogador)
							encadeamentoAdversario.reduzirAberturas()

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




		pass

	def atualizaEncadeamento(self, coordNova, coordVizinha, direcao, jogador):
		encadeamento = self.encontraEncadeamento(direcao, coordVizinha, jogador)
		encadeamento.adicionaCoordenada(coordNova)
		return encadeamento

	def encontraEncadeamento(self, direcao, coord, jogador):
		for enc in self.__encadeamentos:
			if enc.getDirecao() == direcao and enc.getJogador() == jogador:
				coordenadas = enc.getCoordenadas()

				if direcao == Direcao.HORIZONTAL:
					if coordenadas[0].y == coord.y:
						for coordEnc in coordenadas:
							if coord == coordEnc:
								return enc

				elif direcao == Direcao.VERTICAL:
					if coordenadas[0].x == coord.x:
						for coordEnc in coordenadas:
							if coord == coordEnc:
								return enc

				elif direcao == Direcao.DIAGONAL_BARRA:
					if -(coordenadas[0].x - coord.x) == (coordenadas[0].y - coord.y):
						for coordEnc in coordenadas:
							if coord == coordEnc:
								return enc

				elif direcao == Direcao.DIAGONAL_CONTRA_BARRA:
					if (coordenadas[0].x - coordenadas[0].y) == (coord.x - coord.y):
						for coordEnc in coordenadas:
							if coord == coordEnc:
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

		return (totalP1, totalP2, totalP1-totalP2)
