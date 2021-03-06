from generic import Point, is_child
import random
import things


MAX_HP = 100
MAX_DURABILITY = 10

MAP_BLOCK = {
	0: None, # path
	1: things.Brick, # wall
	2: things.FlagExit, # exit
	3: things.FlagStart, # start
}


def is_block(thing):
	try:
		return is_child(getattr(things, thing), things.Block)
	except TypeError:
		return False


def is_item(thing):
	try:
		return is_child(getattr(things, thing), things.Item)
	except TypeError:
		return False


def count_exit(grid, x, y):
	"""
	count exit path for a given cell of
	coordinates x,y
	"""
	count = 0
	if grid[x][y+1] == 0:
		count += 1
	if grid[x][y-1] == 0:
		count += 1
	if grid[x+1][y] == 0:
		count += 1
	if grid[x-1][y] == 0:
		count += 1
	return count


class Area(object):
	"""
	generate an area from a maze
	by adding blocks and items
	"""
	def __init__(self, width, height, seed=None): # add level argument
		random.seed(seed)

		self.items = [t for t in dir(things) if is_item(t)]
		self.maze = Maze(width, height)
		self.create()

	def create(self):
		self.grid = [[self.add_thing(v) for v in r] for r in self.maze.grid]

	def add_thing(self, thing):
		try:
			return MAP_BLOCK[thing]()
		except TypeError:
			return self.fill_path()

	def fill_path(self):
		"""
		did wrong here
		shoud calculate the probability of an item
		to be on the area, not its probability to
		probably be on the area

		i.e.: do a global random of how many times every items
		shoud appear at max on the area based on a LEVEL and
		add them to the area. if item raise EmptyItemException, then just
		don't add it
		"""
		try:
			return getattr(things, random.choice(self.items))()
		except things.EmptyItemException:
			return things.Path()


class Maze(object):
	def __init__(self, width, height, exit_cell=(1, 1)):
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
		# readd exit and start cells
		x0, y0 = self.exit_cell
		self.grid[y0][x0] = 2
		x1, y1 = self.start_cell
		self.grid[y1][x1] = 3

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
				self._visit_cell(neighbor, depth + 1)
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
	# m = Area(21, 21)
	# print m.grid
	print is_item('Item')
	print is_item('Key')
	print is_child(things.Item, things.Item)