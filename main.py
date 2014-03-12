# -*- coding: utf-8 -*-

import Tkinter as tk
from maps import Map


ENTITY_SIZE = 30


class Game(tk.Frame):
	def __init__(self, parent, map_src, width=600, height=600):
		tk.Frame.__init__(self, parent)
		self.canvas = tk.Canvas(self, highlightthickness=0, width=width, height=height, background='white')
		self.canvas.pack(side='top', fill='both', expand=True, padx=2, pady=2)

		self.map = Map(map_src)
		self.map.generate()

		self.draw_blocks(0) # 0 = start map
		self.draw_items(0) # 0 = start map

	def draw_blocks(self, area):
		self.draw_things(area, 'blocks')

	def draw_items(self, area):
		self.draw_things(area, 'items')

	def draw_things(self, area, thing_str):
		things = getattr(self.map[area], thing_str)
		for thing in things:
			thing.element = self.canvas.create_rectangle(
				thing.coords.x + 30,
				thing.coords.y + 30,
				thing.coords.x + ENTITY_SIZE,
				thing.coords.y + ENTITY_SIZE,
				outline='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR),
				fill='#{0:02x}{1:02x}{2:02x}'.format(*thing.COLOR)
			)


	# def draw_players(self):
	# 	for order, players in self.cluster.nation.iteritems():
	# 		for player in players:
	# 			try:
	# 				self.canvas.delete(player.element)
	# 			except:
	# 				pass
	# 			method = player.draw(PLAYER_SIZE)[0]
	# 			coords = player.draw(PLAYER_SIZE)[1:]
	# 			player.element = getattr(self.canvas, method)(
	# 				*coords,
	# 				outline=player.selected * self.cluster.flag or self.canvas['background'],
	# 				fill=player.selected * self.canvas['background'] or self.cluster.flag,
	# 				tags=order
	# 			)
	# 	self.canvas.after(25, self.draw_players)

	# def draw_marker(self, coordx, coordy):
	# 	try:
	# 		self.canvas.delete(self.marker.element)
	# 	except:
	# 		pass

	# 	self.marker.coordx = coordx
	# 	self.marker.coordy = coordy

	# 	self.marker.element = getattr(self.canvas, self.marker.draw(MARKER_SIZE)[0])(
	# 		self.marker.draw(MARKER_SIZE)[1:],
	# 		outline='#ffffff'
	# 	)

	# def bind_events(self):
	# 	click = Click(self)
	# 	self.canvas.bind('<Button-1>', click.select)



# a bell ring, when approching it rings louder, to indicate direction


if __name__ == '__main__':
	root = tk.Tk()
	root.resizable(0, 0)

	game = Game(root, 'map.png')
	game.pack(side='left', padx=4, pady=4)

	root.mainloop()