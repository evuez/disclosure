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

		self.bind_events()

	def draw_map(self):
		for thing in self.map.grid:
			try:
				self.draw_thing(thing)
			except AttributeError:
				pass
			if isinstance(thing, things.Player):
				self.player = thing
		self.canvas.tag_raise(self.player.element)

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

		new_coords = Point(
			self.player.coords.x + x,
			self.player.coords.y + y
		)

		if self.can_goto(new_coords):
			self.player.coords = new_coords
			self.canvas.move(
				self.player.element,
				x * self.THING_SIZE.w,
				y * self.THING_SIZE.h
			)

	def can_goto(self, coords):
		for thing in self.map.grid:
			try:
				print thing.coords, coords
				if thing.coords == coords:
					return False
			except AttributeError:
				pass
		return True



# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()