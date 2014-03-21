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