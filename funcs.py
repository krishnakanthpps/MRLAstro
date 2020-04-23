from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

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
	return deg,mnt,sec

#create and return the chart dict
def calc_allpos():
	#declare an empty dict to store chart objs
	planets_dict = {}
	houses_dict = {}

	date = Datetime('2020/04/22', '19:14', '-07:00')
	geopos = GeoPos('33n60', '117w80')
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
			planets_dict['Rahu'] = [p.sign, to_dms_prec(p.signlon)]
		elif p.id == 'South Node':
			planets_dict['Ketu'] = [p.sign, to_dms_prec(p.signlon)]
		else:
			planets_dict[p.id] = [p.sign, to_dms_prec(p.signlon)]


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
		houses_dict[h.id] = [h.sign, to_dms_prec(h.signlon)]		


	#return planets_dict and houses_dict
	return planets_dict, houses_dict


if __name__ == "__main__":
	planets,houses = calc_allpos()

	print(planets['Sun'])

