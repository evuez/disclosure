from random import randint


MAX_RARITY = 100


class EmptyItem(Exception):
	pass


class Inventory(object):
	items = []


class Item(object):
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