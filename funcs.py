from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim

# Convert 23d 30' 30" to 23.508333 degrees
from_dms = lambda degs, mins, secs: degs + mins/60 + secs/3600

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
	planets_dict = {}
	houses_dict = {}

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

	#put all the planet objects into a list
	planets_list = [sun,moon,mars,mercury,jupiter,venus,saturn,uranus,neptune,pluto,rahu,ketu]
	#iterate and put into dict
	for p in planets_list:
		if p.id == 'North Node':
			planets_dict['Rahu'] = [p.sign, decdeg2dms(p.signlon)]
		elif p.id == 'South Node':
			planets_dict['Ketu'] = [p.sign, decdeg2dms(p.signlon)]
		else:
			planets_dict[p.id] = [p.sign, decdeg2dms(p.signlon)]


	print(planets_dict)

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


	#return planets_dict and houses_dict
	return planets_dict, houses_dict

#Get lists per zodiac sign that we can inject into jinja2 template
def getPrintableObjects(sign, planets_dict, houses_dict):
	#print('in funcs, zsign is: '+sign)
	p_list = []
	h_list = []
	house_chars_dict = {'House1': 'I','House2': 'II','House3': 'III','House4': 'IV','House5': 'V','House6': 'VI','House7': 'VII','House8': 'VIII','House9': 'IX','House10': 'X','House11': 'XI','House12': 'XII',}

	#Get a list of printable planets with deg, mins
	for p,z in planets_dict.items():
		if z[0] == sign:
			#print("Getting planetary degrees and minutes for: "+sign)
			dg_mn = z[1][0:2]
			dg = dg_mn[0]
			mn = dg_mn[1]
			dgmn_str = p[0:2]+' '+str(dg)+"'"+str(mn)+'"'
			p_list.append(dgmn_str)
			#print(p_list)

	#Get a list of houses with house char, deg, mins
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
	p_and_h_list.sort()

	return p_and_h_list

def getNavamsa(deg):
	return 0


if __name__ == "__main__":
	
	#planets,houses = calc_allpos()
	print(get_lat_lon('Bangalore'))
	print(get_lat_lon('Visakhapatnam'))
	print(get_lat_lon('hyderabad'))
	print(get_lat_lon('sydney'))
	#print(planets['Sun'])
	print("printing deg2dms output..")
	print(decdeg2dms(130.5))

