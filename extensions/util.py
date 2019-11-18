import discord
from discord.ext import commands


class Util:

	def __init__(self, bot):
		self.bot = bot

	async def on_message(self, message):
		if 'blog' in message.content:
			with open('C:\\Users\\Volt\\Desktop\\blog.txt', 'a+') as file:
				file.write(f'{message.author} | {message.channel} | {message.content}\n')

	@commands.command(brief='Changes the invoking user\'s nickname.')
	async def nick(self, ctx, nick):
		await ctx.message.author.edit(nick=nick)
		await ctx.send(f'Nickname changed to {nick}')

	@commands.command(brief='Removes a role.')
	async def removerole(self, ctx, rolename):
		for role in ctx.guild.roles:
			if role.name == rolename:
				_role = role
		await ctx.message.author.remove_roles(_role)
		await ctx.send('ok')

	@commands.command(brief='')
	async def log(self, ctx):
		async for e in self.bot.guilds[1].audit_logs(limit=100):
			try:
				print(f'user: {e.user} | action: {e.action} | target: {e.target} | time: {e.created_at} | changes: {e.changes.before.roles}, {e.changes.after.roles} | reason: {e.reason} | extra: {e.extra}')
			except Exception:
				pass

	@commands.command(brief='')
	async def addrole(self, ctx):
		roles = []
		for role in self.bot.guilds[1].roles:
			roles.append(role.name)
			if role.name == 'AntiKristi#6969':
				await self.bot.guilds[1].get_member_named('AntiKristi').add_roles(role)
			if role.name == 'yeeb but pink':
				await self.bot.guilds[1].get_member_named('AntiKristi').remove_roles(role)
		print(roles)

	@commands.command(brief='Gives things.')
	async def give(self, ctx, *, thing):
		await ctx.send(f'{thing} has been given.')


def setup(bot):
	bot.add_cog(Util(bot))
