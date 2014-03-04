import items
from generic import Point




class Block(object):
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
	pass


class Wood(Block):
	DURABILITY = 1


class Lava(Block):
	CROSSABLE = True


class Door(Block):
	OPENABLE = True


class LockedDoor(Door):
	OPENABLE = (items.Key,)