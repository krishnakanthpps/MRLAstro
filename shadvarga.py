"""
	Returns hora of planet given the below example dictionary
	
	{'Sun': ['Capricorn', 279.9196373475607], 'Moon': ['Sagittarius', 269.1425613804137], 'Mars': ['Capricorn', 283.6911963266094], 'Mercury': ['Sagittarius', 258.7059129886326], 'Jupiter': ['Sagittarius', 241.09105316185673], 'Venus': ['Aquarius', 306.0894496658849], 'Saturn': ['Sagittarius', 267.6901331020929], 'Uranus': ['Sagittarius', 250.1264855882071], 'Neptune': ['Gemini', 85.22504147608478], 'Pluto': ['Gemini', 75.25527693994611], 'Rahu': ['Sagittarius', 259.17343174945495], 'Ketu': ['Gemini', 79.17343174945495], 'Chiron': ['Sagittarius', 258.8702714981658]}

"""
def calc_horas(planets_dict):

	zs_odd_signs = ['Aries', 'Gemini', 'Leo','Libra', 'Sagittarius', 'Aquarius']
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

	#one hora is 15 deg
	one_hora = 360 / 24
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











#calc_horas(planets_dict)

