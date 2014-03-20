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


def color_variant(hex_color, brightness_offset=1):
	"""
	darken or lighten a color
	shoud try with `col = (col & 0xfefefe) >> 1`
	"""
	rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
	new_rgb_int = [int(v, 16) + brightness_offset for v in rgb_hex]
	new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
	return "#" + "".join([hex(i)[2:] for i in new_rgb_int])