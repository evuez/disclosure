from items import Key
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


class Point(object):
	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y


class Area(object):
	blocks = []
	items = []
	def __init__(self, pixels):
		self.generate(pixels)

	def generate(self, pixels):
		for p in pixels:
			print pixels[:3]
			print [
				d[1] for d in PIXEL_MAPPING
				if d[0] == pixels[:3]
			]


			# obj = [
			# 	d[1] for d in PIXEL_MAPPING
			# 	if d[0] == pixels[:3]
			# ][0]()
			# if obj is Block:
			# 	self.blocks.append(obj)
			# if obj is Item:
			# 	self.items.append(obj)


class Map(object):
	areas = []
	def __init__(self, src):
		self.pixels, self.size = self.read_data(src)

	def __str__(self):
		return "Areas in this map: {}".format(
			', '.join([a.__class__.__name__ for a in self.areas])
		)

	def read_data(self, src):
		im = Image.open(src)
		return (im.load(), im.size)

	def generate(self):
		pixels = []
		for x in xrange(0, self.size[0], PIXEL_SIZE[0]):
			for y in xrange(0, self.size[1], PIXEL_SIZE[1]):
				pixels.append(self.pixels[x,y])
			if x >= AREA_SIZE[0]:
				self.areas.append(Area(pixels))
				pixels = []