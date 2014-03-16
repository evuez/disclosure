from generic import Point
from random import randint


MAX_RARITY = 100


class Thing(object):
	def __init__(self):
		self.element = None


class Item(Thing):
	rarity = 1
	def __init__(self, void_rarity=False):
		"""
		if void_rarity, rarity isn't taken in account
		to generate item
		"""
		if void_rarity:
			return
		if randint(0, MAX_RARITY) % max(self.rarity, 1):
			raise EmptyItem


class Key(Item):
	rarity = 0


class Battery(Item):
	pass


class Matchbox(Item):
	pass


class Safe(Item):
	pass


class Block(Thing):
	COLOR = (255, 255, 255)
	MAX_HP = 100
	DURABILITY = 0 # 0: unbreakable, scale from 1 to MAX_DURABILITY
	MOVEABLE = False # False, True or (required0, required1,)
	CROSSABLE = False
	OPENABLE = False
	def __init__(self, coords):
		self.hp = self.MAX_HP
		self.coords = coords

	def take_hit(self, power):
		self.hp -= self.DURABILITY / MAX_DURABILITY * power
		self.hp = max(self.hp, 0)
		return self.hp


class Brick(Block):
	COLOR = (0, 0, 0)


class Wood(Block):
	COLOR = (200, 100, 200)
	DURABILITY = 1


class Lava(Block):
	COLOR = (255, 000, 000)
	CROSSABLE = True


class Door(Block):
	COLOR = (176, 123, 100)
	OPENABLE = True
	def __init__(self, coords):
		super(Door, self).__init__(coords)
		self.exit_to = None


class LockedDoor(Door):
	COLOR = (255, 100, 255)
	OPENABLE = (Key,)


class EmptyItem(Exception):
	pass


class Inventory(object):
	items = []


class Body(Thing):
	MAX_HP = None


class Player(Body):
	MAX_HP = 100


class Creature(Body):
	MAX_HP = 100