import discord
from discord.ext import commands

import thesaurus
import random

class Thesaurize:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief='Thesaurizes the passed string.', aliases=['th'])
	async def thesaurize(self, ctx, *, message = None):
		if not message and not self.bot.db['last_message'][ctx.message.channel].content.startswith('__'):
			message = self.bot.db['last_message'][ctx.message.channel].content
		th_message = [] 
		for word in message.split(' '):
			try:
				th_word = random.choice(thesaurus.Word(word).synonyms())
			except Exception:
				th_word = word
			th_message.append(th_word)
		await ctx.send(' '.join(th_message))

def setup(bot):
	bot.add_cog(Thesaurize(bot))