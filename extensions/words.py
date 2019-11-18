import discord
from discord.ext import commands

import etym

import requests

class Words:

	def __init__(self, bot):
		self.bot = bot

		self.url = 'https://googledictionaryapi.eu-gb.mybluemix.net/'
		self.payload = {'define' : None, 'lang' : 'en'}

	def get_json(self, word:str)->dict:
		self.payload['define'] = word
		response = requests.get(self.url, params=self.payload)

		json = response.json()
		output = {}

		output['word'] = json['word']
		output['phonetic'] = json['phonetic']
		for j, (key, value) in enumerate(json['meaning'].items()):
			output[f'meaning ({key})'] = json['meaning'][key][0]
			output[f'meaning ({key})']['synonyms'] = json['meaning'][key][0]['synonyms'][:3]

		return output

	@commands.command(brief='Gets the definition for a given word.')
	async def word(self, ctx, word:str):
		json = self.get_json(word)
		await ctx.send(json)

	@commands.command(brief='Gets the etymology of the given word.', aliases=['etym'])
	async def etymology(self, ctx, word):
		await ctx.send(etym.main(word))

def setup(bot):
	bot.add_cog(Words(bot))