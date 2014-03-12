import items
from generic import Point


class Block(object):
	COLOR = (255, 255, 255)
	MAX_HP = 100
	DURABILITY = 0 # 0: unbreakable, scale from 1 to MAX_DURABILITY
	MOVEABLE = False # False, True or (required0, required1,)
	CROSSABLE = False
	OPENABLE = False
	def __init__(self, coords):
		self.element = None
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


class LockedDoor(Door):
	COLOR = (255, 100, 255)
	OPENABLE = (items.Key,)