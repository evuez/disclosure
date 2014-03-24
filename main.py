# -*- coding: utf-8 -*-

import Tkinter as tk
import tkFont
from uuid import uuid4
from collections import Counter
from generic import Point, Size, color_variant, distance
from area import Area
import things


AREA_HEIGHT = 630
THING_COUNT = 5
SHADOW_COLOR = (0, 0, 0)
INVENTORY = Size(AREA_HEIGHT, 60)


class NotWideEnoughException(Exception):
	pass


class Game(tk.Frame):
	def __init__(self, parent, width=AREA_HEIGHT, height=AREA_HEIGHT):
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

		self.inventory = tk.Canvas(
			self,
			highlightthickness=0,
			width=INVENTORY.w,
			height=INVENTORY.h,
			background='black'
		)
		self.inventory.pack(
			side='bottom',
			fill='both',
			expand=True,
			padx=2,
			pady=2
		)

		self.player = things.Player()
		self.new()

		self.bind_events()

	@property
	def thing_size(self):
		return AREA_HEIGHT / self.thing_count

	@property
	def thing_count(self):
		return THING_COUNT + self.player.level * 2

	def font(self, size=14, weight='bold'):
		return tkFont.Font(
			family='Courier',
			size=size,
			weight=weight,
			name='font{}'.format(size)
		)

	def new(self):
		self.seed = '{}-{}'.format (str(uuid4())[:8], self.player.level)

		self.player.refresh()
		self.canvas.delete('all')
		self.area = Area(self.thing_count, self.thing_count, self.seed)
		self.draw_area()
		self.draw_inventory()

	def draw_area(self):
		for y,row in enumerate(self.area.grid):
			for x,col in enumerate(row):
				thing = self.area.grid[y][x]

				self.draw_thing(thing, x, y)
				if isinstance(thing, things.FlagStart):
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
			x * self.thing_size,
			y * self.thing_size,
			x * self.thing_size + self.thing_size,
			y * self.thing_size + self.thing_size,
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
				x * self.thing_size,
				y * self.thing_size
			)
			self.player.move()
			self.collect_item()
			self.draw_inventory()
			self.update_shadow()
			if self.has_won():
				self.player.level_up()
				# self.draw_won_screen()
				self.new()

	def can_goto(self, x, y):
		coords = self.get_thing_coords(self.player)
		return not isinstance(
			self.area.grid[coords[0] + y][coords[1] + x],
			things.Block
		)

	def get_thing_coords(self, thing):
		coords = map(round, self.canvas.coords(thing.element))
		return (
			int(coords[1] / self.thing_size),
			int(coords[0] / self.thing_size)
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
			radius = 0

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

	def has_won(self):
		coords = self.get_thing_coords(self.player)
		return isinstance(
			self.area.grid[coords[0]][coords[1]],
			things.FlagExit
		)

	def draw_inventory_thing(self, thing_class, count, slot):
		self.inventory.create_rectangle(
			slot * INVENTORY.h,
			INVENTORY.h,
			slot * INVENTORY.h + INVENTORY.h,
			0,
			width=0,
			fill='#{0:02x}{1:02x}{2:02x}'.format(*thing_class.COLOR)
		)
		self.inventory.create_text(
			slot * INVENTORY.h + INVENTORY.h / 2,
			9,
			text=thing_class.__name__,
			font=self.font(size=7, weight='normal')
		)
		self.inventory.create_text(
			slot * INVENTORY.h + INVENTORY.h / 2,
			INVENTORY.h / 2,
			text=count,
			font=self.font(size=14, weight='bold')
		)

	def draw_inventory(self):
		self.inventory.delete('all')
		thing_classes = [t.__class__ for t in self.player.inventory.unused]
		for slot,thing in enumerate(Counter(thing_classes).items()):
			self.draw_inventory_thing(*thing, slot=slot)


# a bell ring, when approching it rings louder, to indicate direction
if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root)
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()