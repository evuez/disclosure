import items

class Block(object):
	DURABILITY = 0 # 0: unbreakable, scale from 1 to MAX_DURABILITY
	MOVEABLE = False # False, True or (required0, required1,)
	CROSSABLE = False
	OPENABLE = False
	def __init__(self):
		self.hp = MAX_HP
		self.coords = Point()

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