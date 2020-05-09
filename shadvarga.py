import math
from funcs import *

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

#def calc_trimsamsa(planets_dict):
#	trimsamsa_dict = {}

# planets_dict = {'Sun': ['Aries', 2.50000], 'Moon': ['Sagittarius', 269.1425613804137], 'Mars': ['Capricorn', 283.6911963266094], 'Mercury': ['Sagittarius', 258.7059129886326], 'Jupiter': ['Sagittarius', 241.09105316185673], 'Venus': ['Aquarius', 306.0894496658849], 'Saturn': ['Sagittarius', 267.6901331020929], 'Uranus': ['Sagittarius', 250.1264855882071], 'Neptune': ['Gemini', 85.22504147608478], 'Pluto': ['Gemini', 75.25527693994611], 'Rahu': ['Sagittarius', 259.17343174945495], 'Ketu': ['Gemini', 79.17343174945495], 'Chiron': ['Sagittarius', 258.8702714981658]}
	
# # planets_dict = {'Sun': ['Aries', 24.9196373475607], 'Moon': ['Sagittarius', 29.1425613804137]}


# # #calc_horas(planets_dict)
# # calc_drekkana(planets_dict)
# calc_dwadasamsa(planets_dict)
