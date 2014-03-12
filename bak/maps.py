from items import Key
from generic import Point
import Image, ImageDraw
import blocks, items


MAX_HP = 100
MAX_DURABILITY = 10
PIXEL_MAPPING = (
	((0, 0, 0), blocks.Brick),
	((200, 100, 200), blocks.Wood),
	((255, 000, 000), blocks.Lava),
	((176, 123, 100), blocks.Door),
	((255, 100, 255), blocks.LockedDoor)
)
AREA_SIZE = (100, 100)
PIXEL_SIZE = (30, 30)


class Area(object):
	blocks = []
	items = []
	def __init__(self, pixels):
		self.generate(pixels)

	def generate(self, pixels):
		for p in pixels:
			obj = [
				d[1] for d in PIXEL_MAPPING
				if d[0] == p[0]
			]
			try:
				obj = obj[0](p[1])
			except IndexError:
				continue
			if issubclass(obj.__class__, blocks.Block):
				self.blocks.append(obj)
			if issubclass(obj.__class__, items.Item):
				self.items.append(obj)


class Map(object):
	areas = []
	def __init__(self, src):
		self.im_map = src
		self.areas = []

	def __str__(self):
		return "Areas in this map: {}".format(
			', '.join([a.__class__.__name__ for a in self.areas])
		)

	def __getitem__(self, key):
		return self.areas[key]

	def read_data(self, src):
		im = Image.open(src)
		return (im.load(), im.size)

	def generate(self):
		im_pixels, im_size = self.read_data(self.im_map)
		pixels = []
		for x in xrange(0, im_size[0], PIXEL_SIZE[0]):
			for y in xrange(0, im_size[1], PIXEL_SIZE[1]):
				pixels.append((im_pixels[x,y], Point(x, y)))
			if x >= AREA_SIZE[0]:
				self.areas.append(Area(pixels))
				pixels = []


if __name__ == '__main__':
	m = Map('map.png')
	m.generate()
	print vars(m)