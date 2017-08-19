from tkinter import *


class GUI:

	def __init__(self):
		self.__root = Tk()
		self.__root.title("Gomoku - Dunia e Vinicius")
		theLabel = Label(self.__root, text="Hello")
		theLabel.pack()

	def refresh(self):
		try:
			self.__root.update()
		except:
			sys.exit()
