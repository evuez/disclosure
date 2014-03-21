# -*- coding: utf-8 -*-

import Tkinter as tk
from generic import Point, Size, color_variant, distance
from area import Area
import things


AREA_HEIGHT = 630
THING_COUNT = 21
THING_SIZE = AREA_HEIGHT / THING_COUNT
SHADOW_COLOR = (0, 0, 0)


class NotWideEnoughException(Exception):
	pass


class Game(tk.Frame):
	def __init__(self, parent, width=630, height=AREA_HEIGHT):
		if width < AREA_HEIGHT:
			raise NotWideEnoughException(
				'Width must be greater than {}'.format(AREA_HEIGHT)
			)

		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(
			self,
			highlightthickness=0,
			width=height,
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

				self.draw_thing(thing, x, y)
				if isinstance(thing, things.FlagStart):
					self.player = things.Player()
					self.draw_thing(self.player, x, y)

		self.canvas.tag_raise(self.player.element)
		self.update_shadow()

	def draw_thing(self, thing, x, y):
		"""
		raise AttributeError
		assign thing to self.player if it is
		an instance of things.Player
		"""
		# http://effbot.org/tkinterbook/canvas.htm#canvas.Canvas.create_image-method
		# to use an image instead
		thing.element = self.canvas.create_rectangle(
			x * THING_SIZE,
			y * THING_SIZE,
			x * THING_SIZE + THING_SIZE,
			y * THING_SIZE + THING_SIZE,
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
				x * THING_SIZE,
				y * THING_SIZE
			)
			self.collect_item()
			self.update_shadow()

	def can_goto(self, x, y):
		coords = self.get_thing_coords(self.player)
		return not isinstance(
			self.area.grid[coords[0] + y][coords[1] + x],
			things.Block
		)

	def get_thing_coords(self, thing):
		coords = self.canvas.coords(thing.element)
		return (
			int(coords[1] / THING_SIZE),
			int(coords[0] / THING_SIZE)
		)

	def collect_item(self):
		coords = self.get_thing_coords(self.player)
		item = self.area.grid[coords[0]][coords[1]]

		if self.player.collect(item):
			self.remove_thing(item)

	def remove_thing(self, thing):
		coords = self.get_thing_coords(thing)
		new_path = things.Path()

		self.area.grid[coords[0]][coords[1]] = new_path
		self.canvas.delete(thing.element)

		self.draw_thing(new_path, coords[1], coords[0])
		self.canvas.tag_raise(self.player.element)

	def update_shadow(self):
		try:
			radius = self.player.light.radius
		except AttributeError:
			radius = 4

		player_coords = self.get_thing_coords(self.player)
		for y,row in enumerate(self.area.grid):
			for x,v in enumerate(row):
				thing = self.area.grid[x][y]

				self.canvas.itemconfig(
					thing.element,
					fill='#{0:02x}{1:02x}{2:02x}'.format(
						*color_variant(
							thing.COLOR,
							radius / distance(player_coords, (x,y)))
					)
				)


# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()