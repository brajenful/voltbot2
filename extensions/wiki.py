import discord
from discord.ext import commands
import random

import wikipedia


class Wikipedia:

	def __init__(self, bot):
		self.bot = bot
		self.get_summary = True  # Posts a short summary alongside the link
		self.summary_sentences = 3  # The number of sentences in the summary
		self.language = 'en'

		wikipedia.set_lang(self.language)

	def __get_page(self, query: None, is_random=False):
		if is_random:
			result = wikipedia.random(pages=1)
		else:
			result = wikipedia.search(query, results=1)

		try:
			page = wikipedia.page(result)
		except wikipedia.exceptions.DisambiguationError as e:
			page = wikipedia.page(random.choice(e.args[1]))

		summary = wikipedia.summary(page.title, sentences=self.summary_sentences)
		return page, summary

	@commands.command(brief='Returns a wikipedia page based on your query.')
	async def wiki(self, ctx, *, query):
		try:
			page, summary = self.__get_page(query, is_random=True if query == 'random' else False)
		except wikipedia.exceptions.WikipediaException:
			await ctx.send('No results.')
			return
		await ctx.send(f'{summary}\n{page.url}')


def setup(bot):
	bot.add_cog(Wikipedia(bot))
