from items import Key
from generic import Point
import Image, ImageDraw
import blocks, items


MAX_HP = 100
MAX_DURABILITY = 10

BLOCK_SIZE = (30, 30)


class Map(object):
	def __init__(self):
		self.areas = (Dungeon, Palace)

	def __str__(self):
		return "Areas in this map: {}".format(
			', '.join([a.__class__.__name__ for a in self.areas])
		)

	def generate(self):
		pass


class Area(object):
	special_blocks = None
	items = None
	neighbors = None
	def __init__(self):
		self.generate()

	def check_doable(self):
		"""
		check if a player can go from a door
		to every other doors without dying
		"""
		pass

	def generate(self):
		pass


class Dungeon(Area):
	special_blocks = ((blocks.Lava, 3),)
	items = ((items.Battery, 2),)
	neighbors = (map.Palace,)


class Palace(Area):
	neighbors = (Dungeon,)


if __name__ == '__main__':
	m = Map()
	m.generate()
	print vars(m)