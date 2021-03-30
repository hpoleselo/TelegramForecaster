import datetime
import requests
import re
import sys
from bs4 import BeautifulSoup as BS


response = 0


def checkPage():
	global response
	try:
		response = requests.get('https://pt.surf-forecast.com/breaks/Vilas/forecasts/latest')
		if response.status_code:
			if response.status_code == 200:
				# THAT'S WHY WE GOT THE CHARACTER CONVERSION (IT WAS ON UNICODE ON THE WEBSITE) ON LINE 132!!
				# Standard of this page will be utf-8 because it has special characters
				response.encoding = "utf-8"
				return response
			elif response.status_code == 204:
				print("Retrieved data but no content.")
			elif response.status_code == 304:
				print("Not modified.")
	except(requests.exceptions.ConnectionError):
		print("[ERROR]: Could not connect to the internet, network error. Check if you're connected to the internet.")
		sys.exit(1)
	except(requests.exceptions.Timeout, requests.exceptions.ConnectTimeout):
		print("[ERROR]: Connection timed out.")
	except requests.exceptions.HTTPError as errh:
		print ("[ERROR]: HTTP Error:", errh)
	except(requests.exceptions.RequestException):
		print("[ERROR]: Didn't catch the error with the previous exceptions, some brutal error is going on...")
		sys.exit(1)

def checkContent(response):
	pageContent = response.content
	# Transform the page into a string so we can parse it
	pageText = response.text
	return pageText

def getContent(pageText):
	soup = BS(pageText, "lxml")

	verbose = True
	period = []
	energy = []
	wave_height = []
	wave_direction = []
	wind_speed = []
	wind_direction = []
	high_tide = []
	low_tide = []
	dates = []
	time = []
	# Variable added for our application to be more scalable, I have figure out somehow how to get the limit instead of hardcoding it
	table_length = 60


	# TODO: Checar o porquê o tamanho de time eh 46 e nao 23, ele ta dando parsing 2x?
	# TODO usar dictionary pro wind e wind direction
	# TODO: VER QUAL SWELL PEGAR, há 3 swells possiveis e ele ta confundindo na hora de pegar o swell!!!!
	# TODO: Pegar rating e escalar o melhor dia da semana como um resultado do boletim! Para isso precisariamos criar tipo uma tabela nossa


	# find_all retorna um iteravel, por isso precisamos passar por um for

	# Wave period
	forecastTableRows = soup.find_all("tr", {"data-row-name":"periods"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all('td', class_='forecast-table__cell')
		for cell in tableCells:
			value = cell.find("strong").text
			period.append(value)

	# Wave energy
	forecastTableRows = soup.find_all("tr", {"data-row-name":"energy"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all('td', class_='forecast-table__cell')
		for cell in tableCells:
			value = cell.find("strong").text
			energy.append(value)

	# Wind speed and direction
	forecastTableRows = soup.find_all("tr", {"data-row-name":"wind"})
	for tableRow in forecastTableRows:
		# Gets the wind direction
		tableCells = tableRow.find_all('div', class_='forecast-table__value')
		for cell in tableCells:
			wind_direction.append(cell.text)

	# Gets the wind speed
	windSpeeds = tableRow.find_all('text', class_='wind-icon-val')
	for windSpeed in windSpeeds:
		wind_speed.append(windSpeed.text)


	# High-tide 
	forecastTableRows = soup.find_all("tr", {"data-row-name":"high-tide"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all('div', class_='forecast-table__value--tiny')
		for cell in tableCells:
			high_tide.append(cell.text)

	# Low-tide
	forecastTableRows = soup.find_all("tr", {"data-row-name":"low-tide"})
	for tableRow in forecastTableRows:
			lowTides = tableRow.find_all('div', class_='forecast-table__value--tiny')
			for lowTide in lowTides:
					low_tide.append(lowTide.text)


	# Wave height
	forecastTableRows = soup.find_all("tr", {"data-row-name":"wave-height"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all('div', class_='forecast-table__value')
		for cell in tableCells:
			wave_direction.append(cell.text)

	waveHeights = tableRow.find_all('text', class_='swell-icon-val')
	for waveHeight in waveHeights:
		wave_height.append(waveHeight.text)


	# Time
	forecastTableRows = soup.find_all("tr", {"data-row-name":"time"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all('td', class_='forecast-table-time__cell')
		for cell in tableCells:
			timeOfTheDay = cell.text
			# One of the characters wasn't in Unicode, so either we had to eliminate the Unicode part (which in my case was useless)
			# Or we convert it to utf-8
			timeOfTheDayConv = (timeOfTheDay.encode('ascii', 'ignore')).decode("utf-8")
			time.append(timeOfTheDayConv)


	# Date/Days of the week
	forecastTableRows = soup.find_all("tr", {"data-row-name":"days"})
	for tableRow in forecastTableRows:
		tableCells = tableRow.find_all("div", {"class":'forecast-table__value'})
		for cell in tableCells:
			dates.append(cell.text)


	"""
	# Date
	date = datetime.datetime.today()
	rangeOfDays = 2
	for i in range(rangeOfDays):
			# Adds 
			if i == 0:
					dates.append(date.strftime("%b-%d"))
			date += datetime.timedelta(days=1)
			dates.append(date.strftime("%b-%d")) 
	"""


	# ! Data Treatment !

	# When we parse the wind direction we get 'Vento' and 'km/h' as values, so we slice them out from the list!
	wind_direction = wind_direction[2:]

	# Was getting 46 for the length (somehow it is parsing twice? Check later.)
	# UPDATE: It always retrieves time twice, after the Surfforecast update it went from 23 to 60 time positions
	# Meaning we have to slice it to 60.
	time = time[:table_length]

	# Days were being repeated
	dates_temp = dates[:12]
	# Cleanup the list
	dates = []
	remainder = 0
	# Get values Sabado20, Domingo21... (Divisible by 3 including the first one (0))
	for i in range(len(dates_temp)):
		if i == 0:
			dates.append(dates_temp[i])
		elif remainder == (i%3):
			dates.append(dates_temp[i])

	if verbose:
		print("## Resultados ##\n")
		print("\nPeriodo das ondas: ", period)
		print("Tamanho: ", len(period))
		print("\nEnergia das ondas: ", energy)
		print("Tamanho: ", len(energy))
		print("\nTamanho das ondas: ", wave_height)
		print("Tamanho: ", len(wave_height))
		print("\nDireção das ondas: ", wave_direction)
		print("Tamanho: ", len(wave_direction))
		print("\nVelocidade do vento: ", wind_speed)
		print("Tamanho: ", len(wind_speed))
		print("\nDireção do vento: ", wind_direction)
		print("Tamanho: ", len(wind_direction))
		print("\nMare alta: ", high_tide)
		print("Tamanho: ", len(high_tide))
		print("\nMare baixa: ", low_tide)
		print("Tamanho: ", len(low_tide))
		print("\nDatas: ", dates)
		print("Tamanho: ", len(dates))
		print("\nHorários: ", time)
		print("Tamanho: ", len(time))
    # Use dictionary to return since there're too many values?
	return table_length, period, wind_speed, wind_direction, wave_height, wave_direction, energy, dates, time, high_tide, low_tide
		

"""
def main():
	response = checkPage()
	pageText = checkContent(response)
	a,b,c,d,e,f,g,h,j,k = getContent(pageText)
	#print(a, b,c,d,e,f,g,h,j,k)
main()
"""
