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


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

def color_variant(color, scalefactor=1):
	"""
	darken or lighten a color
	"""
	r,g,b = color
	r = clamp(r * scalefactor)
	g = clamp(g * scalefactor)
	b = clamp(b * scalefactor)
	return (int(r), int(g), int(b))