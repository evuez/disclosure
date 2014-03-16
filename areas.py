from items import Key
from generic import Point, Size
import Image, ImageDraw
import blocks, items


MAX_HP = 100
MAX_DURABILITY = 10

AREA_SIZE = Size(90, 90)
BLOCK_SIZE = (3, 3)


class Map(object):
	def __init__(self):
		self.entry = 'Palace'
		self.areas = []

	def __str__(self):
		return "Areas in this map: {}".format(
			', '.join([a.__name__ for a in self.areas])
		)

	def generate(self, area=None):
		if area is None:
			area = self.entry
		area = globals()[area]
		if area in self.areas:
			return
		area().generate()
		self.areas.append(area)
		for neighbor in area.neighbors:
			self.generate(neighbor)


class Area(object):
	special_blocks = None
	items = None
	neighbors = None
	def __init__(self):
		self.generate()

	def iscrossable(self):
		"""
		check if a player can go from a door
		to every other doors without dying
		"""
		pass

	def generate(self):
		self.walls = []
		self.doors = []
		for n in self.neighbors:
			x = 5
			y = 5
			self.doors.append(
				blocks.Door(Point(x, y))
			)
		return self


class Dungeon(Area):
	special_blocks = ((blocks.Lava, 3),)
	items = ((items.Battery, 2),)
	neighbors = ('Palace','Watchtower')


class Palace(Area):
	neighbors = ('Dungeon',)


class Watchtower(Area):
	neighbors = ('Palace',)


if __name__ == '__main__':
	m = Map()
	print m
	m.generate()
	print m
	# for a in m.areas:
	# 	for n in a.neighbors:
	# 		print globals()[n]() # generate maps by browing in neighbors