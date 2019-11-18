import discord
from discord.ext import commands

class Clapify:

	def __init__(self, bot):
		self.bot = bot

		self.clap = '👏'

	@commands.command(brief='Clapifies your string.', aliases=['clap'])
	async def clapify(self, ctx, *, text):
		await ctx.send(self.clap.join(text.split(' ')))

def setup(bot):
	bot.add_cog(Clapify(bot))