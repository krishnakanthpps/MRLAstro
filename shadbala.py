from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from natsort import natsorted
from funcs import *
from shadvarga import *

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

male_planets_list = ["Sun","Mars","Mercury","Jupiter","Saturn"]
female_planets_list = ["Moon","Venus"]

kendra_houses_list = ["House1", "House4", "House7", "House10" ]
panapara_houses_list = ["House2", "House5", "House8", "House11" ]
apoklima_houses_list = ["House3", "House6", "House9", "House12" ]

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
	total_ucchabala = 0.0
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
					#print(f"Found {planet} in {sign}!")

					#Check swarasi
					for x in swarasi_dict[planet]:
						if sign == x:
							vargabala_dict[planet] += 30
							#print(f"{planet} is in swarasi {x}")
								
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
							#print(f"Found adhimitra kshetra for {planet}")
							vargabala_dict[planet] += 20
						if p in relationships_dict[planet]["Friends"]:
							#print(f"Found mitra kshetra for {planet}")
							vargabala_dict[planet] += 15

						elif p in relationships_dict[planet]["Neutrals"]:
							#print(f"Found sama kshetra for {planet}")
							vargabala_dict[planet] += 10

						#adhishatru
						elif p in relationships_dict[planet]["Enemies"] and planet in rasi_lord_enemies:
							#print(f"Found adhisatru kshetra for {planet}")
							vargabala_dict[planet] += 2		
						elif p in relationships_dict[planet]["Enemies"]:
							#print(f"Found satru kshetra for {planet}")
							vargabala_dict[planet] += 4

	#Get the total of all computed ucchabalas
	total_vargabala = 0.0
	for vb in vargabala_dict.values():
		total_vargabala+=vb

	vargabala_dict['total_vargabala'] = total_vargabala

	#print(vargabala_dict)
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
			vargabala_dict[planet] = 0.0

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


	#print("############# Calculating Drekkana vargabalas ##################")
	drekkana_dict = shadvarga_dict["drekkana_dict"]
	get_varga_balas(drekkana_dict)

	#Calculate vargabalas for each DX chart
	#print("############# Calculating Navamsa vargabalas ##################")
	navamsa_dict = shadvarga_dict["navamsa_dict"]
	get_varga_balas(navamsa_dict)

	#print("############# Calculating Dwadasamsa vargabalas ##################")
	dwa_dict = shadvarga_dict["dwa_dict"]
	get_varga_balas(dwa_dict)

	#Hora dict needs some pre-processing due to additional symbols
	#print ("############ Calculating Hora vargabalas ##################")
	hora_dict = shadvarga_dict["hora_dict"]
	hora_dict_clean = {}
	#Cleanup the + and - symbols from planet names
	for k,v in hora_dict.items():
		p_list = []
		for x in v:
			x = x.replace("+:","")
			x = x.replace("-:","")
			p_list.append(x)
		hora_dict_clean[k] = p_list

	get_varga_balas(hora_dict_clean)

	#print("############# Calculating Saptamsa vargabalas ##################")
	
	saptamsa_dict = shadvarga_dict["saptamsa_dict"]
	#get_varga_balas(saptamsa_dict)

	#print(vargabala_dict)

	#Hora dict needs some pre-processing due to additional symbols
	# print("############# Calculating Trimsamsa vargabalas ##################")
	# trimsamsa_dict = shadvarga_dict["trimsamsa_dict"]

	# print(trimsamsa_dict)

	return vargabala_dict

# Ojhayugmarasiamsabala
def get_ojhayugmarasiamsabala(planets_dict, shadvarga_dict):
	
	ojhayugmarasiamsabala_dict = {}

	#Calculate for rasi chart
	for obj in planets_dict.items():
		#print(f"Processing: {obj}")
		planet = obj[0]
		sign = obj[1][0]

		#Initialize scores
		ojhayugmarasiamsabala_dict[planet] = 0

		#No ojhayugmarasiamsabala for rahu,ketu & transsaturnian planets
		if planet not in transsaturnian_list:
			#Check if moon, venus in even signs
			if sign not in zs_odd_signs and planet in female_planets_list:
				ojhayugmarasiamsabala_dict[planet] += 15
			elif sign in zs_odd_signs and planet in male_planets_list:
				ojhayugmarasiamsabala_dict[planet] += 15

	#Calculate ojhayugmarasiamsabala for navamsa chart
	navamsa_dict = shadvarga_dict["navamsa_dict"]
	#Go through list of planets and get amsa sign and lord of sign
	for planet in planets_list:
		if planet not in transsaturnian_list:
			#Find what sign this planet is in
			for sign,p_list in navamsa_dict.items():
				if planet[0:2] in p_list:
					if sign not in zs_odd_signs and planet in female_planets_list:
						ojhayugmarasiamsabala_dict[planet] += 15
					elif sign in zs_odd_signs and planet in male_planets_list:
						ojhayugmarasiamsabala_dict[planet] += 15
	
	
	#Get the total of all computed ojhayugmarasiamsabalas
	total_ojhayugmarasiamsabala = 0.0
	for ob in ojhayugmarasiamsabala_dict.values():
		total_ojhayugmarasiamsabala+=ob

	ojhayugmarasiamsabala_dict['total_ojhayugmarasiamsabala'] = total_ojhayugmarasiamsabala

	return ojhayugmarasiamsabala_dict


#Calculate kendradibala
def get_kendradibala(planets_dict, houses_dict, shadvarga_dict, chart):

	kendradibala_dict = {}

	#Get the house data
	house1 = chart.get(const.HOUSE1)
	house2 = chart.get(const.HOUSE2)
	house3 = chart.get(const.HOUSE3)
	house4 = chart.get(const.HOUSE4)
	house5 = chart.get(const.HOUSE5)
	house6 = chart.get(const.HOUSE6)
	house7 = chart.get(const.HOUSE7)
	house8 = chart.get(const.HOUSE8)
	house9 = chart.get(const.HOUSE9)
	house10 = chart.get(const.HOUSE10)
	house11 = chart.get(const.HOUSE11)
	house12 = chart.get(const.HOUSE12)
	sun = chart.getObject(const.SUN)
	moon = chart.getObject(const.MOON)
	mars = chart.getObject(const.MARS)
	mercury = chart.getObject(const.MERCURY)
	jupiter = chart.getObject(const.JUPITER)
	venus = chart.getObject(const.VENUS)
	saturn = chart.getObject(const.SATURN)

	planet_objs_dict = { "Sun":sun, "Moon":moon, "Mars":mars, "Mercury":mercury, "Jupiter":jupiter, "Venus":venus, "Saturn":saturn }
	houses_objs_list = [house1,house2,house3,house4,house5,house6,house7,house8,house9,house10,house11,house12]

	for planet in planets_list:
		if planet not in transsaturnian_list:
			kendradibala_dict[planet] = 0.0
			#find which house the planet is in
			for h in houses_objs_list:
				if h.hasObject(planet_objs_dict[planet]):
					if h.id in kendra_houses_list:
						kendradibala_dict[planet] += 60
					elif h.id in panapara_houses_list:
						kendradibala_dict[planet] += 30
					elif h.id in apoklima_houses_list:
						kendradibala_dict[planet] += 15
					
	
	#Get the total of all computed 
	total_kendradibala = 0.0
	for kb in kendradibala_dict.values():
		total_kendradibala+=kb

	kendradibala_dict['total_kendradibala'] = total_kendradibala
	#print(kendradibala_dict)
	return kendradibala_dict

#Get the drekkana bala
def get_drekkanabala(planets_dict):

	drekkanabala_dict = {}

	male_planets_list = ["Sun","Mars","Jupiter"]
	female_planets_list = ["Moon","Venus"]
	herma_planets_list = ["Mercury","Saturn"]

	for planet,pos in planets_dict.items():
		if planet not in transsaturnian_list:

			deg = pos[1][0]
			sign = pos[0]

			drekkanabala_dict[planet] = 0.0
			if deg <= 10 and planet in male_planets_list:
				drekkanabala_dict[planet]+=15
			elif deg > 10 and deg <= 20 and planet in female_planets_list:
				drekkanabala_dict[planet]+=15
			elif deg >20 and deg <=30 and planet in herma_planets_list:
				drekkanabala_dict[planet]+=15

	#Get the total of all computed 
	total_drekkanabala = 0.0
	for db in drekkanabala_dict.values():
		total_drekkanabala+=db

	drekkanabala_dict['total_drekkanabala'] = total_drekkanabala

	return drekkanabala_dict

#####################
###### SHADBALA #####
#####################
def get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict, chart):

	#Initialize the sthanabala dict
	sthanabala_dict = {}

	#Get the ucchabalas, store in the main sthanabala dict
	ucchabala_dict = get_ucchabala(planets_dict_lon_only)
	sthanabala_dict["ucchabalas"] = ucchabala_dict 

	#Get vargabalas
	vargabala_dict = get_vargabala(planets_dict, shadvarga_dict)
	sthanabala_dict["vargabalas"] = vargabala_dict 

	#Get ojhayugmarasiamsabala
	ojhayugmarasiamsabala_dict = get_ojhayugmarasiamsabala(planets_dict, shadvarga_dict)
	sthanabala_dict["ojhayugmarasiamsabalas"] = ojhayugmarasiamsabala_dict


	#Get kendradi balas
	kendradibala_dict = get_kendradibala(planets_dict, houses_dict, shadvarga_dict, chart)
	sthanabala_dict["kendradibalas"] = kendradibala_dict


	drekkanabala_dict = get_drekkanabala(planets_dict)
	sthanabala_dict["drekkanabalas"] = drekkanabala_dict


	#################################################
	#### Compute totals for each bala per planet ####
	#################################################
	sun_total_sthanabala = sthanabala_dict['ucchabalas']['Sun'] + sthanabala_dict['vargabalas']['Sun'] + sthanabala_dict['ojhayugmarasiamsabalas']['Sun'] + sthanabala_dict["kendradibalas"]['Sun'] + sthanabala_dict["drekkanabalas"]['Sun']

	moon_total_sthanabala = sthanabala_dict['ucchabalas']['Moon'] + sthanabala_dict['vargabalas']['Moon'] + sthanabala_dict['ojhayugmarasiamsabalas']['Moon'] + sthanabala_dict["kendradibalas"]['Moon'] + sthanabala_dict["drekkanabalas"]['Moon']

	mars_total_sthanabala = sthanabala_dict['ucchabalas']['Mars'] + sthanabala_dict['vargabalas']['Mars'] + sthanabala_dict['ojhayugmarasiamsabalas']['Mars'] + sthanabala_dict["kendradibalas"]['Mars'] + sthanabala_dict["drekkanabalas"]['Mars']

	mercury_total_sthanabala = sthanabala_dict['ucchabalas']['Mercury'] + sthanabala_dict['vargabalas']['Mercury'] + sthanabala_dict['ojhayugmarasiamsabalas']['Mercury'] + sthanabala_dict["kendradibalas"]['Mercury'] + sthanabala_dict["drekkanabalas"]['Mercury']

	jupiter_total_sthanabala = sthanabala_dict['ucchabalas']['Jupiter'] + sthanabala_dict['vargabalas']['Jupiter'] + sthanabala_dict['ojhayugmarasiamsabalas']['Jupiter'] + sthanabala_dict["kendradibalas"]['Jupiter'] + sthanabala_dict["drekkanabalas"]['Jupiter']

	venus_total_sthanabala = sthanabala_dict['ucchabalas']['Venus'] + sthanabala_dict['vargabalas']['Venus'] + sthanabala_dict['ojhayugmarasiamsabalas']['Venus'] + sthanabala_dict["kendradibalas"]['Venus'] + sthanabala_dict["drekkanabalas"]['Venus']

	saturn_total_sthanabala = sthanabala_dict['ucchabalas']['Saturn'] + sthanabala_dict['vargabalas']['Saturn'] + sthanabala_dict['ojhayugmarasiamsabalas']['Saturn'] + sthanabala_dict["kendradibalas"]['Saturn'] + sthanabala_dict["drekkanabalas"]['Saturn']


	sthanabala_dict['sun_total_sthanabala'] = sun_total_sthanabala
	sthanabala_dict['moon_total_sthanabala'] = moon_total_sthanabala
	sthanabala_dict['mars_total_sthanabala'] = mars_total_sthanabala
	sthanabala_dict['mercury_total_sthanabala'] = mercury_total_sthanabala
	sthanabala_dict['jupiter_total_sthanabala'] = jupiter_total_sthanabala
	sthanabala_dict['venus_total_sthanabala'] = venus_total_sthanabala
	sthanabala_dict['saturn_total_sthanabala'] = saturn_total_sthanabala


	#print(sthanabala_dict)
	return sthanabala_dict


#Get a dict with all balas
def calc_shadbalas(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict, chart):


	#Populate all Sthanabalas - uccha, varga, ojhayugmarasiamsa, kendradi, drekkana
	shadbala_dict = {}	
	sthanabala_dict = get_sthanabala(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict, chart)
	shadbala_dict['sthanabalas'] = sthanabala_dict

	return shadbala_dict


if __name__ == "__main__":
	

	dob = "1986/05/28"
	# tob = "12:25"
	# city = "hyderabad"
	# tz = 5.5
	# planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon = calc_allpos(dob, tob, city, tz)
	# calc_shadbalas(planets_dict, houses_dict)


