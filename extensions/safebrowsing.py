import discord
from discord.ext import commands

import sb
import requests

from requests.exceptions import MissingSchema

class SafeBrowsing:

	def __init__(self, bot):
		self.bot = bot
		self.api_key = ''

		self.sb = sb.LookupAPI(self.api_key)

	@commands.command(brief='Scans the given link for any threats.')
	async def scan(self, ctx, link):
		r = self.sb.threat_matches_find(link)
		if not self.is_valid(link):
			await ctx.send('Invalid link.')
			return
		if not r:
			threat_level = 'Safe'
		else:
			threat_level = 'Unsafe'
		await ctx.send(f'{threat_level}.')

	def is_valid(self, link):
		try:
			res = requests.get(link)
		except Exception as e:
			return False
		return True

def setup(bot):
	bot.add_cog(SafeBrowsing(bot))
