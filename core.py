import logging
import discord
import asyncio
import sys
import shelve
from discord.ext import commands
import time

TOKEN = ''


class Client(commands.Bot):

	def __init__(self, *, command_prefix, description, token):
		self.command_prefix = command_prefix
		self.description = description
		self.token = token
		self.last_message = {}

		super().__init__(command_prefix=self.command_prefix, description=self.description)

		logging.basicConfig(level=logging.INFO)

		self.__open_db('data/data')
		#self.db['extensions'] = ['general', 'admin', 'group', 'util', 'weather', 'nlss', 'thesaurize', 'safebrowsing', 'color']
		self.__load_extensions()

	def __load_extensions(self):
		sys.path.append('extensions')
		sys.path.append('external')
		for extension in self.db['extensions']:
			try:
				self.load_extension(extension)
				print(f'{extension} extension loaded.')
			except Exception:
				print(f'Couldn\'t load extension {extension}.')

	def __open_db(self, database):
		self.db = shelve.open(database, writeback=True)
		print(f'{database} database file opened.')

	def __sync_db(self):
		time.sleep(1)
		try:
			self.db.sync()
		except TypeError:
			pass

	def launch(self):
		self.run(self.token)

	async def on_ready(self):
		print('Ready.')
		print(f"Guilds: {', '.join([guild.name for guild in self.guilds])}")
		print(f'Activity: {self.activity}')

	async def on_command_completion(self, ctx):
		self.__sync_db()

	async def on_message(self, message):
		await self.process_commands(message)
		try:
			self.db['last_message'][message.channel] = message
		except KeyError:
			self.db['last_message'] = {}

		#await ctx.send('Something went wrong.')


if __name__ == '__main__':
	bot = Client(command_prefix='__', description=None, token=TOKEN)
	bot.launch()
