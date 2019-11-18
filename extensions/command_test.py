import discord
from discord.ext import commands

class CommandTest:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief='')
	async def listen(self, ctx):
		await self.bot.change_presence(discord.Spotify())

def setup(bot):
	bot.add_cog(CommandTest(bot))