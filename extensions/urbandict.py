import discord
from discord.ext import commands

import urbandictionary as ud


class UrbanDictionary:

	def __init__(self, bot):
		self.bot = bot

		self.defs = None
		self.embed = None

	def __create_embed(self, ctx):
		self.embed = discord.Embed(color=ctx.message.author.color, title=self.defs[0].word)
		self.embed.add_field(name='Top definition', value=self.defs[0].definition, inline=False)
		self.embed.add_field(name='Examples', value=self.defs[0].example, inline=False)

	@commands.command(brief='Gives you the urbandictionary entry of a word.', aliases=['ud'])
	async def urban(self, ctx, *, query):
		self.defs = ud.define(query)
		if not self.defs:
			await ctx.send('No results.')
			return
		self.__create_embed(ctx)
		await ctx.send(embed=self.embed)


def setup(bot):
	bot.add_cog(UrbanDictionary(bot))
