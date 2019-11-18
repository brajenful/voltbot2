import discord
from discord.ext import commands
import asyncio

import requests


class EmoteAdder:

	def __init__(self, bot):
		self.bot = bot
		self.temp_path = 'F:\\github\\voltbot_v2\\resources\\emote_adder\\temp'

	@commands.command(brief='Adds a custom emote.')
	async def addemote(self, ctx):
		await ctx.send('React to this message with the emote you want to add.')

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=30)
		except asyncio.TimeoutError:
			await ctx.send('Timed out, please try again.')
		else:
			emote = reaction.emoji
			img_data = requests.get(emote.url).content

			with open(f'{self.temp_path}\\{emote.name}.png', 'w+') as handler:
				handler.write(img_data)

			await ctx.guild.create_custom_emoji(name=emote.name, image=f'{self.temp_path}\\{emote.name}.png')
			await ctx.send(f'Emote {emote.name} added.')


def setup(bot):
	bot.add_cog(EmoteAdder(bot))
