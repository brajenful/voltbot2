import discord
from discord.ext import commands

class Player:

	def __init__(self, bot):
		self.bot = bot

		self.path = 'F:\\github\\voltbot_v2\\data\\libopus-0.x86.dll'
		self.player = None

	async def on_ready(self):
		if not discord.opus.is_loaded():
			try:
				discord.opus.load_opus(self.path)
				print('Opus library loaded.')
			except Exception as e:
				print(e)
		else:
			print('Opus library loaded.')

	@commands.command(brief='Joins a voice channel.')
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		if channel:
			self.player = await ctx.message.author.voice.channel.connect()
			await ctx.send(f'Joined voice channel {channel}')
		else:
			await ctx.send('You\'re not in a voice channel.')
			return

	@commands.command(brief='Leaves the voice channel.')
	async def leave(self, ctx):
		if self.player.channel:
			await self.player.disconnect()
			await ctx.send(f'Left voice channel {self.player.channel}')
		else:
			await ctx.send('I\'m not in a voice channel.')

def setup(bot):
	bot.add_cog(Player(bot))