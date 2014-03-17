# -*- coding: utf-8 -*-

import Tkinter as tk
from generic import Point
from maze import Maze
import things


THING_SIZE = 30

MAP_BLOCK = {
	0: things.Lava, # path
	1: things.Brick, # wall
	2: things.Door, # exit
	3: things.Door, # start
}


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

		self.maze = Maze(width / THING_SIZE, height / THING_SIZE) # give it a random seed so that the user can share it with friends
		self.draw_maze()

	def draw_maze(self):
		for i,row in enumerate(self.maze.maze):
			for j,col in enumerate(row):
				try:
					self.draw_thing(MAP_BLOCK[col](Point(i * THING_SIZE, j * THING_SIZE)))
				except TypeError:
					print "empty"

	def draw_thing(self, thing):
		"""
		raise AttributeError
		"""
		thing.element = self.canvas.create_rectangle(
			thing.coords.x,
			thing.coords.y,
			thing.coords.x + THING_SIZE,
			thing.coords.y + THING_SIZE,
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