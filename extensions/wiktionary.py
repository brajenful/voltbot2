import discord
from discord.ext import commands

from wiktionaryparser import WiktionaryParser


class Wiktionary:

	def __init__(self, bot):
		self.bot = bot

		self.parser = WiktionaryParser()
		self.words = {}
		self.output = None
		self.embed = None

		self.parser.set_default_language('english')

	def __fetch_word(self, word):
		self.words = self.parser.fetch(word)

	@commands.group(brief='Gives you a word\'s etymology, definition, examples etc.')
	async def word(self, ctx):
		pass

	@word.command(brief='Changes the language the command will use.')
	async def lang(self, ctx, lang):
		self.parser.set_default_language(lang)
		language_list = 'https://en.wiktionary.org/wiki/Wiktionary:List_of_languages'
		await ctx.send(f'Language changed to {lang}.\nThe list of languages can be found here: {language_list}')

	@word.command(brief='Gives you a word\'s etymologies.', aliases=['e', 'ety'])
	async def etymology(self, ctx, word):
		self.__fetch_word(word)
		title = word
		description = f'{len(self.words)} results found.'
		self.embed = discord.Embed(color=ctx.message.author.color, title=title, description=description)
		for i, word in enumerate(self.words[:3], 1):
			self.embed.add_field(name=i, value=word['etymology'])
		await ctx.send(embed=self.embed)

	@word.command(brief='Gives you example usages for a word.', aliases=['ex'])
	async def example(self, ctx, word):
		self.__fetch_word(word)
		self.output = [str(word['definitions'][0]['examples']) for i, word in enumerate(self.words)][:3]
		print(self.output)
		await ctx.send('\n'.join(self.output))

	@word.command(brief='Gives you a word\'s definition.', aliases=['d', 'def'])
	async def definition(self, ctx, word):
		self.__fetch_word(word)
		self.output = [str(word['definitions'][0]['text']) for i, word in enumerate(self.words)][:3]
		print(self.output)
		await ctx.send('\n'.join(self.output))


def setup(bot):
	bot.add_cog(Wiktionary(bot))
