import discord
from discord.ext import commands
import datetime
import requests

from forecastiopy.ForecastIO import ForecastIO
from forecastiopy.FIOCurrently import FIOCurrently
import geopy

import geocoder


class Weather(object):

	def __init__(self, bot):
		self.bot = bot

		self.darksky_api_key = 'dd1473466769051ef1c08eb24e7946fd'
		self.geonames_username = 'brajenful'
		self.owm_api_key = 'f4287542973c771350cf050f94680e37'
		self.owm_url = 'http://api.openweathermap.org/data/2.5/weather'
		self.owm_payload = {'lat': None, 'lon': None, 'appid': self.owm_api_key}

		#self.geocoder = geopy.geocoders.GeoNames(username=self.geopy_username)

	def __geolocate(self, location):
		self.coordinates = {}
		self.location = geocoder.geonames(location, key=self.geonames_username)
		self.coordinates[0] = self.location.lat
		self.coordinates[1] = self.location.lng

	def __get_forecast(self):
		self.forecast = ForecastIO(self.darksky_api_key, latitude=self.coordinates[0], longitude=self.coordinates[1])

	def __get_current(self, location):
		self.__geolocate(location)
		self.__get_forecast()

		self.current = FIOCurrently(self.forecast)

		self.output = {}

		if self.location.country == 'United States':
			self.output['Temperature'] = f'{round(self.current.temperature, 1)} °F, {round((self.current.temperature-32)*5/9, 1)} °C'
		else:
			self.output['Temperature'] = f'{round(self.current.temperature, 1)} °C, {round(self.current.temperature*9/5+32, 1)} °F'

		if self.location.country == 'United States':
			self.output['Apparent temperature'] = f'{round(self.current.apparentTemperature, 1)} °F, {round((self.current.apparentTemperature-32)*5/9, 1)} °C'
		else:
			self.output['Apparent temperature'] = f'{round(self.current.apparentTemperature, 1)} °C, {round(self.current.apparentTemperature*9/5+32, 1)} °F'
		
		self.output['Humidity'] = f'{self.current.humidity*100}%'
		self.output['Wind'] = self.current.windSpeed
		self.output['Precipitation'] = self.current.precipIntensity
		self.output['Summary'] = self.current.summary
		self.output['Country'] = self.location.country
		self.output['State/Region'] = self.location.state
		self.output['City/Town'] = self.location.address


		return self.output

	def __get_owm(self, location):
		self.__geolocate(location)
		self.owm_payload['lat'] = self.coordinates[0]
		self.owm_payload['lon'] = self.coordinates[1]
		r = requests.get(self.owm_url, params=self.owm_payload)
		print(r.json())

	@commands.command(brief='Retrieves the current weather at the given location.')
	async def weather(self, ctx, *, location):
		output = self.__get_current(location)
		embed = discord.Embed(color=ctx.message.author.color)
		for i, (key, value) in enumerate(output.items()):
			inline = False
			if i % 2 == 0:
				inline = True
			embed.add_field(name=key, value=value, inline=True)
		embed.set_footer(text='Powered by Dark Sky API')
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Weather(bot))