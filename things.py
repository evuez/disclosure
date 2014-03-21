from generic import Point, is_child
from random import randint


MAX_RARITY = 100
GOD_RARITY = MAX_RARITY + 1

LIGHT_WEAR_RATE = 0.05


class Thing(object):
	"""
	Things are not aware of their position,
	only the area is aware of their position
	"""
	COLOR = (0, 0, 0)
	def __init__(self):
		self.element = None


class FlagExit(Thing):
	COLOR = (39, 174, 96)


class FlagStart(Thing):
	COLOR = (0, 230, 0)


class Path(Thing):
	COLOR = (255, 255, 255)


class Item(Thing):
	RARITY = 1
	def __init__(self, void_rarity=False):
		"""
		if void_rarity, RARITY isn't taken in account
		to generate item
		"""
		super(Item, self).__init__()
		if void_rarity:
			return
		if randint(1, MAX_RARITY) % max(self.RARITY, 1):
			raise EmptyItemException


class Key(Item):
	COLOR = (241, 196, 15)
	RARITY = 99


class Safe(Item):
	COLOR = (155, 89, 182)
	RARITY = 90


class Light(Item):
	RARITY = GOD_RARITY
	RADIUS = 0
	def __init__(self, void_rarity=False):
		super(Light, self).__init__(void_rarity)
		self.wear_level = 1.0

	@property
	def radius(self):
		return self.RADIUS * self.wear_level

	def light(self):
		self.wear_level -= LIGHT_WEAR_RATE



class Flashlight(Light):
	COLOR = (26, 188, 156)
	RARITY = 75
	RADIUS = 4


class Matchstick(Light):
	COLOR = (22, 160, 133)
	RARITY = 20
	RADIUS = 1


class Block(Thing):
	MAX_HP = 100
	DURABILITY = 0 # 0: unbreakable, scale from 1 to MAX_DURABILITY
	MOVEABLE = False # False, True or (required0, required1,)
	CROSSABLE = False
	OPENABLE = False
	def __init__(self):
		super(Block, self).__init__()
		self.hp = self.MAX_HP

	def take_hit(self, power):
		self.hp -= self.DURABILITY / MAX_DURABILITY * power
		self.hp = max(self.hp, 0)
		return self.hp


class Brick(Block):
	COLOR = (44, 62, 80)


class Wood(Block): # added randomly in the walls, allows to break through a wall if got an axe or other
	COLOR = (211, 84, 0)
	DURABILITY = 1


class Lava(Block): # added randomly in the walls, allows to pass through if got the right suit
	COLOR = (231, 76, 60)
	CROSSABLE = True


class Door(Block):
	COLOR = (149, 165, 166)
	OPENABLE = True
	def __init__(self):
		super(Door, self).__init__()
		self.exit_to = None


class LockedDoor(Door): # added randomly in the walls, allows to pass through if got a key
	COLOR = (127, 140, 141)
	OPENABLE = (Key,)


class EmptyItemException(Exception):
	pass


class Body(Thing):
	MAX_HP = None


class Player(Body):
	COLOR = (46, 204, 113)
	MAX_HP = 100
	def __init__(self):
		super(Player, self).__init__()
		self.inventory = Inventory(Flashlight(True))

	def collect(self, item):
		if is_child(item.__class__, Item):
			self.inventory.append(item)
			return True
		return False

	def move(self):
		try:
			self.light.light()
		except AttributeError:
			pass

	@property
	def light(self):
		return self.inventory.best_light


class Creature(Body):
	MAX_HP = 100


class Inventory(list):
	def __init__(self, *args):
		super(Inventory, self).__init__(args)

	def append(self, item):
		super(Inventory, self).append(item)

	@property
	def lights(self):
		return (x for x in self if is_child(x.__class__, Light))

	@property
	def best_light(self):
		try:
			return max(self.lights, lambda x: x.radius)
		except ValueError:
			return None
