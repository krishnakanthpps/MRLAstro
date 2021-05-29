from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from natsort import natsorted
from funcs import *

exaltation_dict = {"Sun":10,"Moon":33,"Mars":298,"Mercury":165,"Jupiter":95,"Venus":357,"Saturn":200}

def get_ucchabala(planets_dict_lon_only):

	ucchabala_dict = {}

	for obj in planets_dict_lon_only.items():
		planet = obj[0]
		p_long = obj[1][1]

		#Get ucchabala only for regular planets
		if planet in exaltation_dict.keys():

			#Find the debilitation for planet
			if exaltation_dict[planet] - 180 < 360:
				p_deb_deg = exaltation_dict[planet] + 180
			else:
				p_deb_deg = ( exaltation_dict[planet] + 180 ) - 360
			
			#Find the ucchabala
			if abs(p_long - p_deb_deg) > 180:
				u_bala = abs((360 - abs(p_long - p_deb_deg)) / 3)
			else:
				u_bala = abs(( p_long - p_deb_deg ) / 3)

			ucchabala_dict[planet] = round(u_bala, 2)

	return ucchabala_dict

#####################
###### SHADBALA #####
#####################
def get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon):

	#Initialize the sthanabala dict
	sthanabala_dict = {}
	# for p in planets_list:
	# 	sthanabala_dict[p] = 0

	# #Get swakshetra, uccha
	# for obj in planets_dict_lon_only.items():
	# 	planet = obj[0]
	# 	p_long = obj[1][1]

	#Get the ucchabalas
	ucchabala_dict = get_ucchabala(planets_dict_lon_only)
		#Calculate the ucchabala for each planets
		#if planet == "Sun" and zsign == "Leo":
		#	sthanabala_dict["Sun"] += 1

		# elif planet == "Moon" and zsign == "Cancer":
		# 	sthanabala_dict["Moon"] += 1

		# elif planet == "Mars" and (zsign == "Aries" or zsign == "Scorpio"):
		# 	sthanabala_dict["Mars"] += 1

		# elif planet == "Mercury" and zsign == "Gemini":
		# 	sthanabala_dict["Mercury"] += 1

		# elif planet == "Jupiter" and (zsign == "Sagittarius" or zsign == "Pisces"):
		# 	sthanabala_dict["Jupiter"] += 1

		# elif planet == "Venus" and (zsign == "Taurus" or zsign == "Libra"):
		# 	sthanabala_dict["Venus"] += 1

		# elif planet == "Saturn" and (zsign == "Capricorn" or zsign == "Aquarius"):
		# 	sthanabala_dict["Saturn"] += 1

	#Store all the bala dicts in the main sthanabala dict
	sthanabala_dict["ucchabalas"] = ucchabala_dict 
	
	#print(sthanabala_dict)

	return sthanabala_dict


#Get a dict with all balas
def calc_shadbalas(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon):

	shadbala_dict = {}
	
	sthanabala_dict = get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon)
	shadbala_dict['sthanabalas'] = sthanabala_dict

	#print(shadbala_dict)
	return shadbala_dict


if __name__ == "__main__":
	

	dob = "1986/05/28"
	# tob = "12:25"
	# city = "hyderabad"
	# tz = 5.5
	# planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon = calc_allpos(dob, tob, city, tz)
	# calc_shadbalas(planets_dict, houses_dict)


