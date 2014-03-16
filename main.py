# -*- coding: utf-8 -*-

import Tkinter as tk
from maze import Maze


THING_SIZE = 30


class Game(tk.Frame):
	def __init__(self, parent, width=600, height=600):
		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(
			self,
			highlightthickness=0,
			width=width,
			height=height,
			background='white'
		)
		self.canvas.pack(side='top', fill='both', expand=True, padx=2, pady=2)

		self.draw_maze()

	def draw_maze(self):
		self.maze = Maze() # give it a random seed so that the user can share it with friends
		for block in self.maze.blocks:
			self.draw_thing(block)

	def draw_thing(self, thing):
		"""
		raise AttributeError
		"""
		thing.element = self.canvas.create_rectangle(
			thing.coords.x - THING_SIZE / 2,
			thing.coords.y - THING_SIZE / 2,
			thing.coords.x + THING_SIZE / 2,
			thing.coords.y + THING_SIZE / 2,
			outline='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR),
			fill='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR)
		)



# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()