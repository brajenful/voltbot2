import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import tweepy

class NLSS:

	def __init__(self, bot):
		self.bot = bot
		self.url = 'http://whenisnlss.com'
		self.api_url = 'https://api.nightbot.tv/1/commands'
		self.units = ['days', 'hours', 'minutes']
		self.raw_string = "The next NLSS starts in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds."
		self.request_headers = {'Nightbot-Channel': '56c882e8dacf6dd11be0e953'}
		#self.twitter_access_token = '2767875434-zWViNxCSuh4uznxAM8rSKITgmjs8Aqy1mdRicWf'
		#self.twitter_access_token_secret = 'dW9SJV1Toav2PKEnYaUhssBYW6PoOguWKRszZFBgVNFrj'

		#self.auth = tweepy.OAuthHandler(self.twitter_access_token, self.twitter_access_token_secret)
		#self.api = tweepy.API(self.auth)

	def get_docket(self):
		for command in requests.get(self.api_url, headers=self.request_headers).json()['commands']:
			if command['_id'] == '56c882e8dacf6dd11be0e95c':
				return command['message']

	@commands.command(brief='Gives you the remaining time until the next NLSS.', aliases=['nlss'])
	async def whenisnlss(self, ctx):
		soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
		goal = datetime.fromtimestamp(int(soup.body['data-goal']))
		now = datetime.fromtimestamp(int(soup.body['data-now']))
		if now > goal:
			await ctx.send(f'The NLSS is live right now!\n{self.get_docket()}\nhttp://www.twitch.tv/northernlion')
			return
		else:
			delta = goal-now
			seconds = delta.seconds
			days = delta.days
			hours, remainder = divmod(seconds, 3600)
			minutes, seconds = divmod(remainder, 60)
			await ctx.send(f'The next NLSS starts in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds.')

	@commands.command(brief='Gets the docket.')
	async def docket(self, ctx):
		await ctx.send(self.get_docket())

def setup(bot):
	bot.add_cog(NLSS(bot))