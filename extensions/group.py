import time
import asyncio

from twitch import TwitchClient

import discord
from discord.ext import commands

class Group:

	def __init__(self, bot):
		self.bot = bot

		self.groups = {} # {name: object}

	def group_exists(self, group):
		if group in self.groups.keys():
			return True

		return False

	def group_exists(self):
		def predicate(self, ctx):
			group = ctx.message.content.split(' ')[1]
			if group in self.groups.keys():
				return True
			else:
				ctx.send(f'Group {group} does not exist.')
		return commands.check(predicate)

	@commands.group(brief='Command group for managing user groups.')
	async def group(self, ctx):
		pass

	@group.command(brief='Creates a new user group.')
	async def create(self, ctx, group):
		self.groups[group] = UserGroup(ctx, group, False)
		await ctx.send(f'Created user group {group}.')

	@group.command(brief='Lists all currently existing groups.')
	async def list(self, ctx):
		groups = '\n'.join([group for group in self.groups.keys()])
		await ctx.send(f'Currently existing groups:\n{groups}')

	@group.command(brief='Adds a user to a group based on user ID.')
	async def add(self, ctx, group, userid):
		if not self.group_exists(group):
			return
		await ctx.send(self.groups[group].add_user(await self.bot.get_user_info(userid)))

	@group.command(brief='Removes a user from a group based on user ID.')
	async def remove(self, ctx, group, userid):
		self.group_exists(group)
		await ctx.send(self.groups[group].remove_user(await self.bot.get_user_info(userid)))
		
	@group.command(brief='Lists all members of a certain group.')
	async def members(self, ctx, group):
		self.group_exists(group)
		users = '\n'.join(self.groups[group].get_users())
		await ctx.send(f'Current members of group {group}:\n{users}')
		

class UserGroup:

	def __init__(self, ctx, name, is_twitch:bool):
		self.CLIENT_ID = 'w6h5tufp5eg7gu7szpivgfvc48qcej'
		self.OAUTH_ID = 'bdzlkuug1khpy6mtfi1j16lyhh7a0w'
		self.USERNAME = 'Volt669'

		self.name = name
		self.ctx = ctx
		self.is_twitch = is_twitch

		self.owner = self.ctx.message.author
		self.destination = self.ctx.message.channel

		self.users = []

		if self.is_twitch:
			self.client = TwitchClient(self.CLIENT_ID, self.OAUTH_ID)
			self.channel = self.Channel(self.ctx, self.name)

	def __add_owner(self):
		self.users.append(self.owner)

	def _is_twitch(self):
		return self.is_twitch

	def get_owner(self):
		return self.owner.name

	def get_name(self):
		return self.name

	def get_users(self):
		usernames = []
		for user in self.users:
			usernames.append(user.name)
		return usernames

	def add_user(self, user):
		if user in self.users:
			return f'User {user.name} already exists in group {self.name}.'
		else:
			self.users.append(user)
			return f'User {user.name} added to group {self.name}.'

	def remove_user(self, user):
		if user in self.users:
			self.users.remove(user)
			return f'User {user.name} removed from group {self.name}.'
		else:
			return f'User {user.name} does not exist in group {self.name}.'

	class Channel(object):

		def __init__(self, ctx, name):
			self.ctx = ctx
			self.name = name

			self.status = None
			self.last_status = None
			self.destination = self.ctx.message.channel

			try:
				self.id = client.users.translate_usernames_to_ids(self.name)[0]['id']
			except Exception as e:
				print(e)

			self.refresh_status()

		def get_channel_id(self):
			return self.id

		async def get_stream_status(self):
			if client.streams.get_stream_by_user(self.id):
				self.status = True
			else:
				self.status = False

			if self.status != self.last_status:
				if self.status:
					await g.client.send_message(self.destination, f'{self.name} is online.')
					self.last_status = True
				else:
					await g.client.send_message(self.destination, f'{self.name} is offline.')
					self.last_status = False

		async def __looper(self):
			while True:
				#print(await self.get_stream_status())
				await asyncio.sleep(30)

		def refresh_status(self):
			looper = asyncio.ensure_future(self.__looper())

def setup(bot):
	bot.add_cog(Group(bot))