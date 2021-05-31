from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from natsort import natsorted

# Convert 23d 30' 30" to 23.508333 degrees
from_dms = lambda degs, mins, secs: degs + mins/60 + secs/3600


planets_list = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Uranus","Neptune","Pluto","Rahu","Ketu","Chiron"]

# the inverse
def to_dms_prec(deg):
  d = int(deg)
  d_norm = d%30
  mins = (deg - d) * 60
  m = int(mins)
  s = round((mins - m) * 60)
  return [d, m, s]

def to_dms(deg):
  d, m, s = to_dms_prec(deg)
  return [d, m, int(s)]

def decdeg2dms(dd):
	mnt,sec = divmod(dd*3600,60)
	deg,mnt = divmod(mnt,60)
	deg = round(deg)
	mnt = round(mnt)
	sec = round(sec)
	return [deg,mnt,sec]

#convert

#Get the latitude and longitude
def get_lat_lon(city):
	geolocator = Nominatim(user_agent="mrlastro")
	location = geolocator.geocode(city)
	lat = location.latitude
	lon = location.longitude
	#lat = "000"
	#lon = "000"

	return lat, lon

#create and return the chart dict
#calc_allpos(dob, tob, city_lat_lon, tz)
def calc_allpos(dob, tob, city, tz):
	#declare an empty dict to store chart objs
	#stores sign+lon
	planets_dict = {}
	#dict to contain lon only
	planets_dict_lon_only = {}
	houses_dict = {}
	houses_dict_signlon = {}

	date = Datetime(dob, tob, tz)
	city_lat, city_lon = get_lat_lon(city)
	geopos = GeoPos(city_lat, city_lon)
	chart = Chart(date, geopos, hsys=const.HOUSES_PLACIDUS, IDs=const.LIST_OBJECTS)

	sun = chart.getObject(const.SUN)
	moon = chart.getObject(const.MOON)
	mars = chart.getObject(const.MARS)
	mercury = chart.getObject(const.MERCURY)
	jupiter = chart.getObject(const.JUPITER)
	venus = chart.getObject(const.VENUS)
	saturn = chart.getObject(const.SATURN)
	uranus = chart.getObject(const.URANUS)
	neptune = chart.getObject(const.NEPTUNE)
	pluto = chart.getObject(const.PLUTO)
	rahu = chart.getObject(const.NORTH_NODE)
	ketu = chart.getObject(const.SOUTH_NODE)
	chiron = chart.getObject(const.CHIRON)

	#put all the planet objects into a list
	planets_list = [sun,moon,mars,mercury,jupiter,venus,saturn,uranus,neptune,pluto,rahu,ketu,chiron]
	#iterate and put into dict
	for p in planets_list:
		if p.id == 'North Node':
			planets_dict['Rahu'] = [p.sign, decdeg2dms(p.signlon)]
			planets_dict_lon_only['Rahu'] = [p.sign, p.lon]
		elif p.id == 'South Node':
			planets_dict['Ketu'] = [p.sign, decdeg2dms(p.signlon)]
			planets_dict_lon_only['Ketu'] = [p.sign, p.lon]
		else:
			planets_dict[p.id] = [p.sign, decdeg2dms(p.signlon)]
			planets_dict_lon_only[p.id] = [p.sign, p.lon]

	#Get the house positions
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

	house_list = [house1,house2,house3,house4,house5,house6,house7,house8,house9,house10,house11,house12]

	#add the house pos to houses_dict
	for h in house_list:
		houses_dict[h.id] = [h.sign, decdeg2dms(h.signlon)]	
		houses_dict_signlon[h.id] = [h.sign, h.signlon]

	#return planets_dict and houses_dict
	return planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart

#creates sort key for getPrintableObjects(), takes d, m of object
#strips m, sort by deg only
def sortkey(obj):
	d = int(obj.split(' ')[1].split('\'')[0])
	return d


#Get formatted lists of planets, houses per zodiac sign for jinja2 template insertion
def getPrintableObjects(sign, planets_dict, houses_dict, p_only=False):
	#print('in funcs, zsign is: '+sign)
	p_list = []
	h_list = []
	house_chars_dict = {'House1': 'I','House2': 'II','House3': 'III','House4': 'IV','House5': 'V','House6': 'VI','House7': 'VII','House8': 'VIII','House9': 'IX','House10': 'X','House11': 'XI','House12': 'XII'}

	#reverse the sort order of objects by degree for these signs (print descending to ascending)
	rev_deg_signs = ['Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

	#Get a list of printable planets with deg, mins
	for p,z in planets_dict.items():
		if z[0] == sign:
			#print("Getting planetary degrees and minutes for: "+sign)
			dg_mn = z[1][0:2]
			dg = dg_mn[0]
			mn = dg_mn[1]
			#dgmn_str = p[0:2]+' '+str(dg)+"'"+str(mn)+'"'
			if p == 'Chiron':
				dgmn_str = 'K'+' '+str(dg)+"'"+str(mn)+'"'
				p_list.append(dgmn_str)
			else:
				dgmn_str = p[0:2]+' '+str(dg)+"'"+str(mn)+'"'
				p_list.append(dgmn_str)
			#print(p_list)

	#Get a list of houses with house char, deg, mins
	#only calculate houses if p_only is set to False
	if not p_only:
		for h,z in houses_dict.items():
			if z[0] == sign:
				dg_mn = z[1][0:2]
				dg = dg_mn[0]
				mn = dg_mn[1]
				#Get house symbol
				h = house_chars_dict[h]
				dgmn_str = h+' '+str(dg)+"'"+str(mn)+'"'
				h_list.append(dgmn_str)

	#Append the planet and house lists and return per zodiac sign
	p_and_h_list = p_list + h_list

	#sort this list from lowest to highest for Ar - Sc and in reverse from Sg to Pi
	if sign in rev_deg_signs:
		p_and_h_list = sorted(p_and_h_list, key=sortkey, reverse=True)
	else:
		p_and_h_list = sorted(p_and_h_list, key=sortkey)

	return p_and_h_list

#returns list of planets per navamsa sign
def navamsa_from_long(sign, planets_dict_lon_only):

	sign_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
	nav_list = []

	for p,z in planets_dict_lon_only.items():
		longitude = planets_dict_lon_only[p][1]
		one_pada = (360 / (12 * 9))  # There are also 108 navamsas
		one_sign = 12 * one_pada    # = 40 degrees exactly
		signs_elapsed = longitude / one_sign
		fraction_left = signs_elapsed % 1
		navamsa_sign_num = int(fraction_left * 12)
		#we now know which sign the navamsa falls under
		navamsa_sign_name = sign_list[navamsa_sign_num]
		#add planet to the list if it falls in 'sign' navamsa
		if navamsa_sign_name == sign:
			#truncate planet name to first two chars
			p = p[0:2]
			nav_list.append(p)

	nav_list = natsorted(nav_list)
	return nav_list



# def navamsa_from_long(planets_dict_lon_only):
#   """Calculates the navamsa-sign in which given longitude falls
#   0 = Aries, 1 = Taurus, ..., 11 = Pisces
#   """
# 	sign_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
# 	navamsa_dict = {}
	
# 	for p,z in planets_dict_lon_only.items():
# 		longitude = planets_dict_lon_only[p][1]
# 		one_pada = (360 / (12 * 9))  # There are also 108 navamsas
# 		one_sign = 12 * one_pada    # = 40 degrees exactly
# 		signs_elapsed = longitude / one_sign
# 		fraction_left = signs_elapsed % 1
# 		navamsa_sign_num = int(fraction_left * 12)
#   		#we now know which sign the navamsa falls under
# 		navamsa_sign_name = sign_list[navamsa_sign_num]
# 		navamsa_dict[p] = navamsa_sign_name

	return navamsa_dict



if __name__ == "__main__":
	
	
	dob = "1986/05/28"
	tob = "12:25"
	city = "hyderabad"
	tz = 5.5
	planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon = calc_allpos(dob, tob, city, tz)

	get_sthanabala(planets_dict, houses_dict)
	#print(houses_dict)

	#print(get_lat_lon('Bangalore'))
	#print(get_lat_lon('Visakhapatnam'))
	#print(get_lat_lon('hyderabad'))
	#print(get_lat_lon('sydney'))
	#print(planets['Sun'])
	#print("printing deg2dms output..")
	#print(decdeg2dms(130.5))

	#print("navamsa for 352.7901809551436")
	#print(navamsa_from_long(352.7901809551436))


