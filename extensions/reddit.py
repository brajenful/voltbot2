import discord
from discord.ext import commands

import praw

import random
import json


class Reddit:

	def __init__(self, bot):
		self.bot = bot

		self.auth_info_path = 'F:/github/voltbot_v2/resources/reddit/login.json'
		with open(self.auth_info_path, 'r') as file:
			self.auth_info = json.loads(file.read())

		self.login()

		self.time_filters = ['week', 'month', 'year', 'all']

	def login(self):
		self.reddit = praw.Reddit(
								client_id=self.auth_info['client_id'],
								client_secret=self.auth_info['client_secret'],
								username=self.auth_info['username'],
								password=self.auth_info['password'],
								user_agent='Discord bot script by /u/Volt69'
								)

	def get_random_post(self, sr, link_only=False):
		time_filter = random.choice(self.time_filters)
		submissions = []
		for submission in self.reddit.subreddit(sr).top(time_filter):
			if link_only:
				submissions.append(submission) if not submission.selftext else None
			else:
				submissions.append(submission)
		return random.choice(submissions)

	@commands.command(brief='Gives you a tip.')
	async def tip(self, ctx):
		subreddit = random.choice(['unethicallifeprotips', 'lifeprotips'])
		post = self.get_random_post(subreddit)
		await ctx.send(post.title[5:])

	@commands.command(brief='cromch')
	async def cromch(self, ctx):
		post = self.get_random_post('cromch', True)
		await ctx.send(post.url)

	@commands.command(brief='loaf')
	async def loaf(self, ctx):
		post = self.get_random_post('Catloaf', True)
		await ctx.send(post.url)

	@commands.command(brief='cursed images')
	async def cursed(self, ctx):
		post = self.get_random_post('cursedimages', True)
		await ctx.send(post.url)

	@commands.command(brief='blursed images')
	async def blursed(self, ctx):
		post = self.get_random_post('blursedimages', True)
		await ctx.send(post.url)

	@commands.command(brief='meow irl')
	async def meow(self, ctx):
		post = self.get_random_post('meow_irl', True)
		await ctx.send(post.url)

	@commands.command(brief='Sad cat.')
	async def sadcat(self, ctx):
		post = self.get_random_post('sadcats', True)
		await ctx.send(post.url)

	@commands.command(brief='hmmm')
	async def hmmm(self, ctx):
		post = self.get_random_post('hmmm', True)
		await ctx.send(post.url)

	@commands.command(brief='Gets a picture from a subreddit.')
	async def r(self, ctx, subreddit):
		post = self.get_random_post(subreddit, True)
		await ctx.send(post.url)

def setup(bot):
	bot.add_cog(Reddit(bot))
