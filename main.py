# -*- coding: utf-8 -*-

import Tkinter as tk
from generic import Point, Size
from area import Area
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

		self.area = Area(THING_COUNT, THING_COUNT) # give it a random seed so that the user can share it with friends
		self.draw_area()

		self.bind_events()

	def draw_area(self):
		for y,row in enumerate(self.area.grid):
			for x,col in enumerate(row):
				thing = self.area.grid[y][x]
				try:
					self.draw_thing(thing, x, y)
				except AttributeError:
					pass
				else:
					if isinstance(thing, things.Player):
						self.player = thing
		self.canvas.tag_raise(self.player.element)

	def draw_thing(self, thing, x, y):
		"""
		raise AttributeError
		assign thing to self.player if it is
		an instance of things.Player
		"""
		thing.element = self.canvas.create_rectangle(
			x * self.THING_SIZE.w,
			y * self.THING_SIZE.h,
			x * self.THING_SIZE.w + self.THING_SIZE.w,
			y * self.THING_SIZE.h + self.THING_SIZE.h,
			width=0,
			fill='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR)
		)

	def bind_events(self):
		self.canvas.bind_all('<KeyPress-Up>', self.move_player)
		self.canvas.bind_all('<KeyPress-Down>', self.move_player)
		self.canvas.bind_all('<KeyPress-Left>', self.move_player)
		self.canvas.bind_all('<KeyPress-Right>', self.move_player)

	def move_player(self, event):
		x = y = 0
		if event.keysym == 'Up':
			y = -1
		if event.keysym == 'Down':
			y = 1
		if event.keysym == 'Left':
			x = -1
		if event.keysym == 'Right':
			x = 1

		if self.can_goto(x, y):
			self.canvas.move(
				self.player.element,
				x * self.THING_SIZE.w,
				y * self.THING_SIZE.h
			)

	def can_goto(self, x, y):
		coords = self.get_thing_coords(self.player)
		return not isinstance(
			self.area.grid[y + coords[0]][x + coords[1]],
			things.Block
		)

	def get_thing_coords(self, thing):
		coords = self.canvas.coords(thing.element)
		return (
			int(coords[1] / self.THING_SIZE.w),
			int(coords[0] / self.THING_SIZE.h)
		)


# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()