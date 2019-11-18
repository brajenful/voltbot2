import discord
from discord.ext import commands


class Admin:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief='Loads an extension.')
	@commands.is_owner()
	async def load(self, ctx, extension):
		try:
			self.bot.load_extension(extension)
			await ctx.send(f'Extension {extension} loaded.')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Unloads an extension.')
	@commands.is_owner()
	async def unload(self, ctx, extension):
		if extension == 'admin':
			return
		try:
			self.bot.unload_extension(extension)
			await ctx.send(f'Extension {extension} unloaded.')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Reloads an extension.')
	@commands.is_owner()
	async def reload(self, ctx, extension):
		try:
			self.bot.unload_extension(extension)
			self.bot.load_extension(extension)
			await ctx.send(f'Extension {extension} reloaded.')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Adds an extension to the list of default extensions.')
	@commands.is_owner()
	async def add(self, ctx, extension):
		if extension in self.bot.db['extensions']:
			await ctx.send('Extension is already on the list.')
			return
		else:
			try:
				if extension in self.bot.extensions:
					self.bot.unload_extension(extension)
				self.bot.db['extensions'].append(extension)
				await ctx.send(f'Extension {extension} added to the list.')
				self.bot.load_extension(extension)
				return
			except Exception as e:
				await ctx.send(e)

	@commands.command(brief='Removes an extension from the list of default extensions.')
	@commands.is_owner()
	async def remove(self, ctx, extension):
		if extension not in self.bot.db['extensions']:
			await ctx.send('Extension is not on the list.')
			return
		else:
			try:
				self.bot.db['extensions'].remove(extension)
				await ctx.send(f'Extension {extension} removed from the list.')
				return
			except Exception as e:
				await ctx.send(e)

	@commands.command(brief='Lists all available extensions.', aliases=['ext'])
	@commands.is_owner()
	async def extensions(self, ctx):
		try:
			loaded_extensions = [extension for extension in self.bot.extensions.keys()]
			unloaded_extensions = [extension for extension in self.bot.db['extensions'] if extension not in self.bot.extensions.keys()]
			if not unloaded_extensions:
				unloaded_extensions = ['None']
			embed = discord.Embed(color=ctx.message.author.color)
			embed.add_field(name='Loaded', value='\n'.join(loaded_extensions), inline=True)
			embed.add_field(name='Unloaded', value='\n'.join(unloaded_extensions), inline=True)
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Gets the class and value of a variable.')
	@commands.is_owner()
	async def get(self, ctx, var):
		try:
			var = eval(var)
			await ctx.send(f'{type(var)}\n{var}')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Sets the variable to the passed value.')
	@commands.is_owner()
	async def set(self, ctx, var, value):
		try:
			exec(f'{var}={value}')
			await ctx.send(f'{var} = {value}')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Calls an async function.')
	@commands.is_owner()
	async def call(self, ctx, var):
		try:
			var = await eval(var)
			await ctx.send(f'{type(var)}\n{var}')
		except Exception as e:
			await ctx.send(e)

	@commands.command(brief='Searches the documentation for the passed query.')
	@commands.is_owner()
	async def docs(self, ctx, query):
		await ctx.send(f'https://discordpy.readthedocs.io/en/rewrite/search.html?q={query}')


def setup(bot):
	bot.add_cog(Admin(bot))
