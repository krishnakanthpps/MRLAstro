import math
from funcs import *
import pprint

#some lists
zs_odd_signs = ['Aries', 'Gemini', 'Leo','Libra', 'Sagittarius', 'Aquarius']

zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']


"""
	Returns HORA of planet given the below example dictionary
	
	{'Sun': ['Capricorn', 279.9196373475607], 'Moon': ['Sagittarius', 269.1425613804137], 'Mars': ['Capricorn', 283.6911963266094], 'Mercury': ['Sagittarius', 258.7059129886326], 'Jupiter': ['Sagittarius', 241.09105316185673], 'Venus': ['Aquarius', 306.0894496658849], 'Saturn': ['Sagittarius', 267.6901331020929], 'Uranus': ['Sagittarius', 250.1264855882071], 'Neptune': ['Gemini', 85.22504147608478], 'Pluto': ['Gemini', 75.25527693994611], 'Rahu': ['Sagittarius', 259.17343174945495], 'Ketu': ['Gemini', 79.17343174945495], 'Chiron': ['Sagittarius', 258.8702714981658]}

"""
def calc_horas(planets_dict):

	zs_odd_signs = ['Aries', 'Gemini', 'Leo','Libra', 'Sagittarius', 'Aquarius']
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

	#one hora is 15 deg
	#one_hora = 360 / 24
	hora_dict = {}

	for planet,pos in planets_dict.items():
		#number of horas elapsed
		lon = int(pos[1])
		sign = pos[0] 
		#horas_elapsed = int((lon / one_hora))
		lon_sign_deg = lon % 30
		#print(horas_elapsed, lon_sign_deg, sign)

		#Sun and Moon don't have horas
		if (planet != 'Sun') and (planet != 'Moon') and (planet != 'Chiron'):
			#print("planet is: "+planet)

			if sign in zs_odd_signs and lon_sign_deg <= 15:
				#add + in front of planet name
				planet = "+"+planet[0:2]
				if sign in hora_dict:
					hora_dict[sign].append(planet)
				else:
					hora_dict[sign] = [planet]

			elif sign in zs_odd_signs and lon_sign_deg > 15:
				planet = "-"+planet[0:2]
				if sign in hora_dict:
					hora_dict[sign].append(planet)
				else:
					hora_dict[sign] = [planet]

			elif sign not in zs_odd_signs and lon_sign_deg <= 15:
				planet = "-"+planet[0:2]
				if sign in hora_dict:
					hora_dict[sign].append(planet)
				else:
					hora_dict[sign] = [planet]

			elif sign not in zs_odd_signs and lon_sign_deg > 15:
				planet = "+"+planet[0:2]
				if sign in hora_dict:
					hora_dict[sign].append(planet)
				else:
					hora_dict[sign] = [planet]


	#print(hora_dict)
	return hora_dict

"""
	Returns the Drekkana (D-3) of given planet
"""
def calc_drekkana(planets_dict):
	
	drek_dict = {}

	for planet,pos in planets_dict.items():
		#number of horas elapsed
		lon = int(pos[1])
		sign = pos[0] 
		#horas_elapsed = int((lon / one_hora))
		planet = planet[0:2]
		lon_sign_deg = int(lon % 30)
		#print(horas_elapsed, lon_sign_deg, sign)
		if lon_sign_deg <= 10:
			#planet lies in 1st drekkana (same sign)
			drek_sign = sign
			if drek_sign in drek_dict:
				drek_dict[drek_sign].append(planet)
			else:
				drek_dict[drek_sign] = [planet]

		##get the 5th sign from current sign if planet between 10 - 20 deg
		elif (lon_sign_deg > 10) and (lon_sign_deg <= 20):
			
			curr_sign_index = zs_list.index(sign)
			#print(f"Current sign is: {sign}, sign index is: {curr_sign_index}")
			#get 5th sign from this and normalize by number of signs
			curr_sign_index = (curr_sign_index + 4) % 12
			#print(f"Fifth sign from: {sign}, is: {zs_list[curr_sign_index]}")
			drek_sign = zs_list[curr_sign_index]
			if drek_sign in drek_dict:
				drek_dict[drek_sign].append(planet)
			else:
				drek_dict[drek_sign] = [planet]	

		else:
			##get the 5th sign from current sign if planet between 20 - 30 deg
			curr_sign_index = zs_list.index(sign)
			#print(f"Current sign is: {sign}, sign index is: {curr_sign_index}")
			#get 9th sign from this and normalize by number of signs
			curr_sign_index = (curr_sign_index + 8) % 12
			#rint(f"9th sign from: {sign}, is: {zs_list[curr_sign_index]}")
			drek_sign = zs_list[curr_sign_index]
			if drek_sign in drek_dict:
				drek_dict[drek_sign].append(planet)
			else:
				drek_dict[drek_sign] = [planet]		

	#print(drek_dict)
	return drek_dict

"""
	Returns dwadashamsa for given planet
"""
def calc_dwadasamsa(planets_dict):
	dwa_dict = {}

	for planet,pos in planets_dict.items():
		#round longitude to 4 decimal places
		#and normalize within 30deg
		lon = round((pos[1] % 30), 4)
		sign = pos[0] 
		planet = planet[0:2]
		#each dwadashamsa is 2.5d (2d30m) so divide by 2.5 and find nth dwadashamsa
		dwa_number = math.ceil(lon / 2.5)

		#get current sign index
		curr_sign_index = zs_list.index(sign)
		#advance current sign by dwa_number, repeat from start
		curr_sign_index = (curr_sign_index + (dwa_number-1)) % 12
		#get the dwadasamsa sign
		dwa_sign = zs_list[curr_sign_index]
		
		#DEBUG
		#print(f"Planet: {planet} | Sign: {sign} |  Longitude: {lon} DMS: {str(decdeg2dms(pos[1]))} | Dwa number: {dwa_number}  |  Dwa sign: {dwa_sign}")
		if dwa_sign in dwa_dict:
			dwa_dict[dwa_sign].append(planet)
		else:
			dwa_dict[dwa_sign] = [planet]		

	#print(dwa_dict)
	return dwa_dict

"""
	Returns the Trimsamsa dict for all given planets 
"""

def calc_trimsamsa(planets_dict, houses_dict):
	
	house_chars_dict = {'House1': 'I','House2': 'II','House3': 'III','House4': 'IV','House5': 'V','House6': 'VI','House7': 'VII','House8': 'VIII','House9': 'IX','House10': 'X','House11': 'XI','House12': 'XII'}
	zs_odd_signs = ['Aries', 'Gemini', 'Leo','Libra', 'Sagittarius', 'Aquarius']
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
	trimsamsa_dict = {}

	#calc trimsamsas for planets
	for planet,pos in planets_dict.items():
		lon = round((pos[1] % 30), 4)
		sign = pos[0] 
 

		#if planet in odd sign, trimsamsa
		if sign in zs_odd_signs:
			if lon <= 5:
				tr = 'Mars'
			elif (lon > 5) and (lon <=10):
				tr = 'Saturn'
			elif (lon > 10) and (lon <=18):
				tr = 'Jupiter'
			elif (lon > 18) and (lon <=25):
				tr = 'Mercury'
			elif (lon > 18) and (lon <=30):
				tr = 'Venus'

			planet = planet[0:2]
			if planet == 'Ch':
				planet = 'K'
			if tr in trimsamsa_dict:
				trimsamsa_dict[tr].append(planet)
			else:
				trimsamsa_dict[tr] = [planet]

		else:
			if lon <= 5:
				tr = 'Venus'
			elif (lon > 5) and (lon <=12):
				tr = 'Mercury'
			elif (lon > 12) and (lon <=20):
				tr = 'Jupiter'
			elif (lon > 20) and (lon <=25):
				tr = 'Saturn'
			elif (lon > 25) and (lon <=30):
				tr = 'Mars'

			planet = planet[0:2]
			if planet == 'Ch':
				planet = 'K'
			if tr in trimsamsa_dict:
				trimsamsa_dict[tr].append(planet)
			else:
				trimsamsa_dict[tr] = [planet]	

	#calc trimsamsas for houses
	for house,pos in houses_dict.items():
		lon = round((pos[1] % 30), 4)
		sign = pos[0] 
		#get the house symbol
		house = house_chars_dict[house]

		#if house in odd sign, trimsamsa
		if sign in zs_odd_signs:
			if lon <= 5:
				tr = 'Mars'
			elif (lon > 5) and (lon <=10):
				tr = 'Saturn'
			elif (lon > 10) and (lon <=18):
				tr = 'Jupiter'
			elif (lon > 18) and (lon <=25):
				tr = 'Mercury'
			elif (lon > 18) and (lon <=30):
				tr = 'Venus'
			if tr in trimsamsa_dict:
				trimsamsa_dict[tr].append(house)
			else:
				trimsamsa_dict[tr] = [house]

		else:
			if lon <= 5:
				tr = 'Venus'
			elif (lon > 5) and (lon <=12):
				tr = 'Mercury'
			elif (lon > 12) and (lon <=20):
				tr = 'Jupiter'
			elif (lon > 20) and (lon <=25):
				tr = 'Saturn'
			elif (lon > 25) and (lon <=30):
				tr = 'Mars'

			if tr in trimsamsa_dict:
				trimsamsa_dict[tr].append(house)
			else:
				trimsamsa_dict[tr] = [house]	

	#format for jinja2 printing
	#for obj in trimsamsa_dict:
#		pl_list = ', '.join(trimsamsa_dict[obj])
#		trimsamsa_dict[obj] = pl_list

	#print(trimsamsa_dict)
	return trimsamsa_dict

	


#planets_dict = {'Sun': ['Aries', 2.50000], 'Moon': ['Aries', 2.50000], 'Mars': ['Capricorn', 283.6911963266094], 'Mercury': ['Sagittarius', 258.7059129886326], 'Jupiter': ['Sagittarius', 241.09105316185673], 'Venus': ['Aquarius', 306.0894496658849], 'Saturn': ['Sagittarius', 267.6901331020929], 'Uranus': ['Sagittarius', 250.1264855882071], 'Neptune': ['Gemini', 85.22504147608478], 'Pluto': ['Gemini', 75.25527693994611], 'Rahu': ['Sagittarius', 259.17343174945495], 'Ketu': ['Gemini', 79.17343174945495], 'Chiron': ['Sagittarius', 258.8702714981658]}
	
# #houses_dict = {'House1': ['Libra', [3, 39, 47]], 'House2': ['Scorpio', [1, 32, 27]], 'House3': ['Sagittarius', [2, 1, 30]], 'House4': ['Capricorn', [3, 52, 44]], 'House5': ['Aquarius', [5, 45, 18]], 'House6': ['Pisces', [6, 9, 32]], 'House7': ['Aries', [3, 39, 47]], 'House8': ['Taurus', [1, 32, 27]], 'House9': ['Gemini', [2, 1, 30]], 'House10': ['Cancer', [3, 52, 44]], 'House11': ['Leo', [5, 45, 18]], 'House12': ['Virgo', [6, 9, 32]]}
# # # # planets_dict = {'Sun': ['Aries', 24.9196373475607], 'Moon': ['Sagittarius', 29.1425613804137]}
#houses_dict = {'House1': ['Libra', 3.6629645418784094], 'House2': ['Scorpio', 1.5408442522945052], 'House3': ['Sagittarius', 2.0251098186394643], 'House4': ['Capricorn', 3.879007240706926], 'House5': ['Aquarius', 5.754867809076472], 'House6': ['Pisces', 6.159021441151367], 'House7': ['Aries', 3.6629645418784094], 'House8': ['Taurus', 1.5408442522945052], 'House9': ['Gemini', 2.0251098186394643], 'House10': ['Cancer', 3.8790072407069403], 'House11': ['Leo', 5.754867809076501], 'House12': ['Virgo', 6.159021441151339]}

# # # #calc_horas(planets_dict)
# # # calc_drekkana(planets_dict)
# # calc_dwadasamsa(planets_dict)
#calc_trimsamsa(planets_dict, houses_dict)
