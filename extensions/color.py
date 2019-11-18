import discord
from discord.ext import commands


class Color:

	def __init__(self, bot):
		self.bot = bot
		self.rolename = None

	"""
	@commands.command(brief='Changes your color.')
	async def color(self, ctx, arg):
		self.rolename = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
		if arg == 'get':
			await self.get_own_color(ctx)
		try:
			colorcode = int(arg, 16)
		except Exception:
			pass
		"""

	async def get_own_color(self, ctx):
		for role in ctx.guild.roles:
			if role.name == self.rolename:
				await ctx.send(f'{role}\'s color is {role.color}.')
				return

	@commands.command(brief='Changes your color.')
	async def color(self, ctx, colorcode16):
		rolename = f'{ctx.message.author.name}#{ctx.message.author.discriminator}'
		if colorcode16 == 'get':
			for role in ctx.guild.roles:
				if role.name == rolename:
					_role = role
			await ctx.send(f'{rolename}\'s color is {hex(_role.color.value)}.')
			return
		try:
			colorcode = int(colorcode16, 16)
		except ValueError:
			await ctx.send('Invalid color code, please use 6-digit hex format (without #).')
			return
		for role in ctx.guild.roles:
			if role.name == rolename:
				_role = role
				await _role.edit(color=discord.Color(colorcode))
				await ctx.send(f'{rolename}\'s color changed to {colorcode16}.')
				return
		_role = await ctx.guild.create_role(name=rolename, color=discord.Color(colorcode))
		await ctx.message.author.add_roles(_role)
		await ctx.send(f'Created new role for {rolename} with color {colorcode16}.')
		return


def setup(bot):
	bot.add_cog(Color(bot))
