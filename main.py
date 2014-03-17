# -*- coding: utf-8 -*-

import Tkinter as tk
from generic import Point, Size
from area import Map
import things


THING_COUNT = 21


class Game(tk.Frame):
	def __init__(self, parent, width=630, height=630):
		self.THING_SIZE = Size(
			width / THING_COUNT,
			height / THING_COUNT
		)

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(
			self,
			highlightthickness=0,
			width=width,
			height=height,
			background='white'
		)
		self.canvas.pack(side='top', fill='both', expand=True, padx=2, pady=2)

		self.map = Map(THING_COUNT, THING_COUNT) # give it a random seed so that the user can share it with friends
		self.draw_map()

	def draw_map(self):
		for thing in self.map.grid:
			try:
				self.draw_thing(thing)
			except AttributeError:
				pass

	def draw_thing(self, thing):
		"""
		raise AttributeError
		"""
		thing.element = self.canvas.create_rectangle(
			thing.coords.x * self.THING_SIZE.w,
			thing.coords.y * self.THING_SIZE.h,
			thing.coords.x * self.THING_SIZE.w + self.THING_SIZE.w,
			thing.coords.y * self.THING_SIZE.h + self.THING_SIZE.h,
			width=0,
			fill='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR)
		)



# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()