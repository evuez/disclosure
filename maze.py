from generic import Point
import things


MAX_HP = 100
MAX_DURABILITY = 10


class Map(object):
	pass


class Maze(object):
	def __init__(self):
		self.blocks = []
		for x in range(0, 100):
			self.blocks.append(things.Block(Point(x, x)))


if __name__ == '__main__':
	pass