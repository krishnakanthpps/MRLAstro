from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from natsort import natsorted
from funcs import *

#Define some globals
exaltation_dict = {"Sun":10,"Moon":33,"Mars":298,"Mercury":165,"Jupiter":95,"Venus":357,"Saturn":200}
moolatrikona_dict = {"Sun":"Leo","Moon":"Taurus","Mars":"Aries","Mercury":"Virgo","Jupiter":"Sagittarius","Venus":"Libra","Saturn":"Aquarius"}
swarasi_dict = {"Sun":["Leo"],"Moon":["Cancer"],"Mars":["Aries","Scorpio"],"Mercury":["Gemini","Virgo"],"Jupiter":["Sagittarius","Pisces"],"Venus":["Taurus","Libra"],"Saturn":["Aquarius","Capricorn"]}
planets_list = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Uranus","Neptune","Pluto","Rahu","Ketu"]
transsaturnian_list = ["Uranus","Neptune","Pluto","Chiron","Rahu","Ketu"]
relationships_dict = { "Sun": { "Friends": ["Moon","Mars","Jupiter"], "Neutrals": ["Mercury"], "Enemies": ["Saturn","Venus"] },
						"Moon": { "Friends": ["Sun","Mercury"], "Neutrals": ["Mars","Jupiter","Saturn","Venus"], "Enemies": [] },
						"Mars": { "Friends": ["Sun","Moon","Jupiter"], "Neutrals": ["Saturn","Venus"], "Enemies": ["Mercury"] },
						"Mercury": { "Friends": ["Sun","Venus"], "Neutrals": ["Saturn","Mars","Jupiter"], "Enemies": ["Moon"] },
						"Jupiter": { "Friends": ["Sun","Moon","Mars"], "Neutrals": ["Saturn"], "Enemies": ["Mercury","Venus"] },
						"Venus": { "Friends": ["Mercury","Saturn"], "Neutrals": ["Mars","Jupiter"], "Enemies": ["Moon","Sun"] },
						"Saturn": { "Friends": ["Mercury","Venus"], "Neutrals": ["Jupiter"], "Enemies": ["Moon","Sun","Mars"] },
						"Uranus": { "Friends": [""], "Neutrals": [""], "Enemies": [""] },
						"Neptune": { "Friends": [""], "Neutrals": [""], "Enemies": [""] },
						"Pluto": { "Friends": [""], "Neutrals": [""], "Enemies": [""] },
						"Chiron": { "Friends": [""], "Neutrals": [""], "Enemies": [""] }

}
rasilords_dict = { "Aries":["Mars"], "Taurus":["Venus"], "Gemini": ["Mercury"], "Cancer": ["Moon"], "Leo": ["Sun"], "Virgo": ["Mercury","Chiron"], "Libra":["Venus"], "Scorpio":["Mars"], "Sagittarius":["Jupiter"],"Capricorn":["Saturn"],"Aquarius":["Saturn","Uranus"],"Pisces":["Jupiter","Neptune"]}

planets_abbr_dict = { "Su":"Sun", "Mo":"Moon", "Ma":"Mars", "Me":"Mercury", "Ju":"Jupiter", "Ve":"Venus", "Sa":"Saturn", "Ur":"Uranus", "Ne":"Neptune", "Pl":"Pluto", "Ch":"Chiron", "Ra":"Rahu", "Ke":"Ketu" }

#Returns a dict with the ucchabalas of all planets
def get_ucchabala(planets_dict_lon_only):

	ucchabala_dict = {}

	for obj in planets_dict_lon_only.items():
		planet = obj[0]
		p_long = obj[1][1]

		#Get ucchabala only for regular planets
		if planet in exaltation_dict.keys():

			#Find the debilitation for the given planet
			if exaltation_dict[planet] - 180 < 360:
				p_deb_deg = exaltation_dict[planet] + 180
			else:
				p_deb_deg = ( exaltation_dict[planet] + 180 ) - 360
			
			#Find the ucchabala
			if abs(p_long - p_deb_deg) > 180:
				u_bala = abs((360 - abs(p_long - p_deb_deg)) / 3)
			else:
				u_bala = abs(( p_long - p_deb_deg ) / 3)

			#Save the computed value in the ucchabala dict
			ucchabala_dict[planet] = round(u_bala, 2)

	#Get the total of all computed ucchabalas
	total_ucchabala = 0
	for ub in ucchabala_dict.values():
		total_ucchabala+=ub

	ucchabala_dict['total_ucchabala'] = total_ucchabala
	return ucchabala_dict

#Get varga balas for amsa (D2, D3, D9, D12, D30) charts
def get_varga_balas(amsa_dict):

	#Go through list of planets and get amsa sign and lord of sign
	for planet in planets_list:
		if planet not in transsaturnian_list:

		#Find what sign this planet is in
			for sign,p_list in amsa_dict.items():

				if planet[0:2] in p_list:
					print(f"Found {planet} in {sign}!")

					#Check swarasi
					for x in swarasi_dict[planet]:
						if sign == x:
							vargabala_dict[planet] += 30
							print(f"{planet} is in swarasi {x}")
								
					#Get the lord(s) of sign where planet is located
					rasi_lords = rasilords_dict[sign]

					#Get friends of rasi lord
					rasi_lord_friends = []
					for r in rasi_lords:
						for f in relationships_dict[r]["Friends"]:
							rasi_lord_friends.append(f)

					rasi_lord_enemies = []
					for r in rasi_lords:
						for f in relationships_dict[r]["Enemies"]:
							rasi_lord_enemies.append(f)

					for p in rasi_lords:

						#adhimitra & mitra
						if p in relationships_dict[planet]["Friends"] and planet in rasi_lord_friends:
							print(f"Found adhimitra kshetra for {planet}")
							vargabala_dict[planet] += 20
						if p in relationships_dict[planet]["Friends"]:
							print(f"Found mitra kshetra for {planet}")
							vargabala_dict[planet] += 15

						elif p in relationships_dict[planet]["Neutrals"]:
							print(f"Found sama kshetra for {planet}")
							vargabala_dict[planet] += 10

						#adhishatru
						elif p in relationships_dict[planet]["Enemies"] and planet in rasi_lord_enemies:
							print(f"Found adhisatru kshetra for {planet}")
							vargabala_dict[planet] += 2		
						elif p in relationships_dict[planet]["Enemies"]:
							print(f"Found satru kshetra for {planet}")
							vargabala_dict[planet] += 4
	
	print(vargabala_dict)
	return vargabala_dict


#Returns vargabala
def get_vargabala(planets_dict, shadvarga_dict):

	global vargabala_dict 
	vargabala_dict = {}

	for obj in planets_dict.items():
		planet = obj[0]
		sign = obj[1][0]

		#No vargabala for rahu,ketu & transsaturnian planets
		if planet not in transsaturnian_list:

			#Initialize scores
			vargabala_dict[planet] = 0

			#Check moolatrikona
			if sign == moolatrikona_dict[planet]:
				#print(f"Moolatrikona found for: {planet}")
				vargabala_dict[planet] += 45

			#Check swarasi
			if type(swarasi_dict[planet]) is list:
				for x in swarasi_dict[planet]:
					if sign == x:
						vargabala_dict[planet] += 30
						#print(f"{planet} is in swarasi {x}, current score is: {vargabala_dict[planet]}")
						
			elif sign == swarasi_dict[planet] and type(swarasi_dict[planet]) is not list:
				vargabala_dict[planet] += 30

			#Get the lord of sign where planet is located
			rasi_lords = rasilords_dict[sign]

			#Get friends of rasi lord
			rasi_lord_friends = []
			for r in rasi_lords:
				for f in relationships_dict[r]["Friends"]:
					rasi_lord_friends.append(f)

			rasi_lord_enemies = []
			for r in rasi_lords:
				for f in relationships_dict[r]["Enemies"]:
					rasi_lord_enemies.append(f)

			for p in rasi_lords:
				
				#adhimitra & mitra
				if p in relationships_dict[planet]["Friends"] and planet in rasi_lord_friends:
					vargabala_dict[planet] += 20
				if p in relationships_dict[planet]["Friends"]:
					vargabala_dict[planet] += 15

				elif p in relationships_dict[planet]["Neutrals"]:
					#print(f"Found {planet} in neutral place: {sign}!")
					vargabala_dict[planet] += 10

				#adhishatru
				elif p in relationships_dict[planet]["Enemies"] and planet in rasi_lord_enemies:
					#print(f"Found {planet} in enemy place: {sign}!")
					vargabala_dict[planet] += 2		
				elif p in relationships_dict[planet]["Enemies"]:
					#print(f"Found {planet} in enemy place: {sign}!")
					vargabala_dict[planet] += 4



	#Calculate vargabalas for each DX chart
	print("############# Calculating Navamsa vargabalas ##################")
	navamsa_dict = shadvarga_dict["navamsa_dict"]
	get_varga_balas(navamsa_dict)

	print("############# Calculating Drekkana vargabalas ##################")
	drekkana_dict = shadvarga_dict["drekkana_dict"]
	get_varga_balas(drekkana_dict)

	print("############# Calculating Dwadasamsa vargabalas ##################")
	dwa_dict = shadvarga_dict["dwa_dict"]
	get_varga_balas(dwa_dict)


	print(vargabala_dict)
	return vargabala_dict



#####################
###### SHADBALA #####
#####################
def get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict):

	#Initialize the sthanabala dict
	sthanabala_dict = {}

	#Get the ucchabalas, store in the main sthanabala dict
	ucchabala_dict = get_ucchabala(planets_dict_lon_only)
	sthanabala_dict["ucchabalas"] = ucchabala_dict 

	#Get vargabalas
	vargabala_dict = get_vargabala(planets_dict, shadvarga_dict)
	sthanabala_dict["vargabalas"] = vargabala_dict 

	print(sthanabala_dict)
	return sthanabala_dict


#Get a dict with all balas
def calc_shadbalas(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict):


	#Populate all Sthanabalas - uccha, varga, ojhayugmarasiamsa, kendradi, drekkana
	shadbala_dict = {}	
	sthanabala_dict = get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict)
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


