from collections import namedtuple


Point = namedtuple('Point', 'x y')


Size = namedtuple('Size', 'w h')


def is_child(child, parent):
	"""
	returns True if class child is child of class parent
	and only if it is child, returns False otherwise
	"""
	try:
		return issubclass(child, parent) and child is not parent
	except TypeError:
		return False


def color_variant(color, scale=1):
	"""
	darken or lighten a color
	"""
	return map(lambda x: int(min(max(x * scale, 0), 255)), color)


def distance(coords1, coords2):
	return (
		max(abs(coords1[0] - coords2[0]), 1) +
		max(abs(coords1[1] - coords2[1]), 1)
	) / 2