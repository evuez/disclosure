from generic import Point
import random
import things


MAX_HP = 100
MAX_DURABILITY = 10


class Map(object):
	"""
	generate a map from a maze
	by adding blocks and items
	"""
	pass


class Maze(object):
	def __init__(self, width=21, height=21, exit_cell=(1, 1)):
		self.width = width
		self.height = height
		self.exit_cell = exit_cell
		self.create()

	def create(self):
		self.grid = [[1] * self.width for _ in range(self.height)] # full of walls
		self.start_cell = None
		self.steps = None
		self.recursion_depth = None
		self._visited_cells = []
		self._visit_cell(self.exit_cell)

	def _visit_cell(self, cell, depth=0):
		x, y = cell
		self.grid[y][x] = 0 # remove wall
		self._visited_cells.append(cell)
		neighbors = self._get_neighbors(cell)
		# random.seed(x*y) # seed * (x+y)
		random.shuffle(neighbors)
		for neighbor in neighbors:
			if not neighbor in self._visited_cells:
				self._remove_wall(cell, neighbor)
				self._visit_cell(neighbor, depth+1)
		self._update_start_cell(cell, depth)

	def _get_neighbors(self, cell):
		x, y = cell
		neighbors = []

		# Left
		if x - 2 > 0:
			neighbors.append((x-2, y))
		# Right
		if x + 2 < self.width:
			neighbors.append((x+2, y))
		# Up
		if y - 2 > 0:
			neighbors.append((x, y-2))
		# Down
		if y + 2 < self.height:
			neighbors.append((x, y+2))

		return neighbors

	def _remove_wall(self, cell, neighbor):
		x0, y0 = cell
		x1, y1 = neighbor
		# Vertical
		if x0 == x1:
			x = x0
			y = (y0 + y1) / 2
		# Horizontal
		if y0 == y1:
			x = (x0 + x1) / 2
			y = y0
		self.grid[y][x] = 0 # remove wall

	def _update_start_cell(self, cell, depth):
		if depth > self.recursion_depth:
			self.recursion_depth = depth
			self.start_cell = cell
			self.steps = depth * 2 # wall + cell

	def show(self, verbose=False):
		MAP = {0: ' ', # path
			   1: '#', # wall
			   2: 'B', # exit
			   3: 'A', # start
			  }
		x0, y0 = self.exit_cell
		self.grid[y0][x0] = 2
		x1, y1 = self.start_cell
		self.grid[y1][x1] = 3
		for row in self.grid:
			print ' '.join([MAP[col] for col in row])
		if verbose:
			print "Steps from A to B:", self.steps


if __name__ == '__main__':
	m = Maze()
	m.show(True)