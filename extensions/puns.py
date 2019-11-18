import discord
from discord.ext import commands

import random

import requests
import bs4

class Puns:

	def __init__(self, bot):
		self.bot = bot

		self.url = None
		self.payload = {'utf8': '✓', 'q': None, 'commit': None}

	def __set_query_type(self, qtype):
		self.qtype = qtype
		if qtype == 'pun':
			self.url = 'https://pungenerator.org/puns'
			self.payload['commit'] = 'Generate Puns!'
		if qtype == 'phrase':
			self.url = 'https://pungenerator.org/phrases'
			self.payload['commit'] = 'Find Phrases!'
		return

	def __get_request(self, query):
		self.payload['q'] = query
		self.r = requests.get(self.url, params=self.payload)
		self.html = self.r.text

	def __parse_html(self):
		self.soup = bs4.BeautifulSoup(self.html, 'html.parser')

	def __get_results(self):
		if self.qtype == 'pun':
			self.results = {}
			lst = self.soup.find_all(attrs={'data-rhyme-id': True})
			for element in lst:
				self.results[element.td.text.strip('\n')] = element.find_all(attrs={'target': '_blank'})[0].text
		if self.qtype == 'phrase': 
			self.results = []
			lst = self.soup.find_all(attrs={'target': '_blank'})
			for element in lst:
				self.results.append(element.text.strip('\n'))

	def __pull_random(self):
		if self.qtype == 'pun':
			self.result, self.original = random.choice(list(self.results.items()))
		if self.qtype == 'phrase':
			self.result = random.choice(self.results)

	def generate(self, query):
		self.__get_request(query)
		self.__parse_html()
		self.__get_results()
		self.__pull_random()
		self.results = []

	@commands.command(brief='Gives you a pun based on your query.')
	async def pun(self, ctx, *, query=None):
		self.__set_query_type('pun')
		if not query:
			await ctx.send(self.original)
			return
		try:
			self.generate(query)
			await ctx.send(self.result)
		except IndexError:
			await ctx.send('No results.')
		
	@commands.command(brief='Gives you a phrase based on your query.')
	async def phrase(self, ctx, *, query):
		self.__set_query_type('phrase')
		try:
			self.generate(query)
			await ctx.send(self.result)
		except IndexError:
			await ctx.send('No results.')

def setup(bot):
	bot.add_cog(Puns(bot))