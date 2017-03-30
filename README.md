# Disclosure - A mini maze game.

You have to reach the exit of the maze, but be careful, your flashlight won't last forever...

![Disclosure](http://i.imgur.com/v5CvUkT.jpg)

## Items

You might find some items on your way, they will be stored automagically in your inventory. Here is a list of the available items and their respective use:

### Lights

The more light, the less dark.

 * Matchstick
 * Lantern
 * Flashlight
 * Neon

### PassThroughs

The heck? Did you just go through this wall?
Be careful, it might not be _that_ helpful in the dark...

 * Axe
 * Poleaxe
 * Crowbar

## Commands

There is a command bar on top of the map. It can be used to do several stuff, here is a list of what you can do with it (the `>` is optional):

 * __use `id`-`level`__ create a random maze of level `level` and with the random seed `id`
 * __use `id`__ create a random maze with the seed `id` using your current level
 * __reload__ generate a new maze using your current level
 * __new__ same as reload
 * __black is black__ just try it. you have to finish your level before it takes effect

There is an hidden command too, try with something bright.

## Setup

- `git clone https://github.com/evuez/disclosure`
- `cd disclosure`
- `python main.py`
- `> use 4a6ee54c-7` for instance :)
