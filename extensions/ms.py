import discord
from discord.ext import commands
import random
import sys

class Minesweeper:

	def __init__(self, bot):
		self.bot = bot
		self.settings = {'gridsize' : 8}

	def create_grid(self):
		self.grid = [[self.Tile() for x in range(self.settings['gridsize'])] for x in range(self.settings['gridsize'])] 

	def populate_grid(self):
		for row in range(self.settings['gridsize']):
			for column in range(self.settings['gridsize']):
				has_mine = random.randint(1, self.settings['gridsize']*10)
				self.grid[row][column].row = row
				self.grid[row][column].column = column
				self.grid[row][column].nearby_mines = self.find_nearby_mines(row, column)
				if has_mine == 1:
					self.grid[row][column].state = 1
					self.minecount += 1
				else:
					self.grid[row][column].state = 0

	def calculate_numbers(self):
		pass

	@commands.command(brief='')
	async def ms(self, ctx):
		self.create_grid()
		self.populate_grid()
		await ctx.send(self.grid)

	class Tile:

		def __init__(self):

			self.row = None
			self.column = None

			self.state = None
			self.nearby_mines = None

def setup(bot):
	bot.add_cog(Minesweeper(bot))