from flask import Flask, render_template, session, redirect, url_for, request, redirect
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from funcs import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghij'


@app.route('/', methods=['GET'])
def index():
	name = 'aditya'
	return '<h1>Hello, {}!</h1>'.format(name)

#Chart creation page
@app.route('/horoscope', methods=['GET'])
def horoscope():
	#shows horoscope details entry form
	return render_template('enter_details.html')

# Display the chart
@app.route('/showchart', methods=['GET','POST'])
def showchart():
	
	#Get name, location from form
	birth_name = request.form['birth_name']
	country = request.form['country']
	city = request.form['city']
	state = request.form['state']
	city_lat, city_lon = get_lat_lon(city)
	
	#generate dob in yyyy/mm/dd format
	day = request.form['dob_day']
	month = request.form['dob_month']
	year = request.form['dob_year']
	dob = year+'/'+month+'/'+day

	#generate tob in hh:mm format
	hour = request.form['tob_hour']
	minute = request.form['tob_minute']
	second = request.form['tob_second']
	tob = hour+":"+minute

	#generate tz in +/-hh:mm format
	tz = request.form['timezone']
	#tz = tz+":"+"00"
	#tz = '+05:30'

	#get all the planetary and house positions for loc without formatting
	planets_dict, houses_dict, planets_dict_lon_only = calc_allpos(dob, tob, city, tz)
	
	#Get objects per each zodiac sign
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
	
	p_and_h_dict = {}
	navamsa_dict = {}

	#Generate dict for jinja2 with planets, houses and their positions
	for sign in zs_list:
		p_and_h_dict[sign] = getPrintableObjects(sign, planets_dict, houses_dict)

	#Returns dict with keys = zodiac sign; value = list of planets in that navamsa
	for sign in zs_list:
		navamsa_dict[sign] = navamsa_from_long(sign, planets_dict_lon_only)


	## DEBUG ##
	print("############PRINTING NAVAMSA DICT###########")
	print(navamsa_dict)
	print("###########################################")
	
	print("Name: "+birth_name)
	print("DOB: "+dob)
	print("City: "+city+" "+str(city_lat)+" "+str(city_lon))
	print("Time: "+str(tob))
	print("Timezone: "+tz)
	#print("############# P, H POSITIONS ##########")
	#print(p_and_h_dict)

	return render_template('display_chart.html', birth_name=birth_name, dob=dob, city=city, tob=tob, tz=tz, p_and_h_dict=p_and_h_dict, planets_dict=planets_dict, houses_dict=houses_dict, navamsa_dict=navamsa_dict)

#Displays current planetary positions
@app.route('/ephemeris')	
def ephemeris():
	date = Datetime('2020/04/21', '12:06', '-07:00')
	pos = GeoPos('38n32', '8w54')
	chart = Chart(date, pos, hsys=const.HOUSES_PLACIDUS)
	all_objs = chart.objects

	#get planets and signs
	sun = chart.getObject(const.SUN)
	moon = chart.getObject(const.MOON)
	mars = chart.getObject(const.MARS)
	mercury = chart.getObject(const.MERCURY)
	jupiter = chart.getObject(const.JUPITER)
	venus = chart.getObject(const.VENUS)
	saturn = chart.getObject(const.SATURN)
	rahu = chart.getObject(const.NORTH_NODE)
	ketu = chart.getObject(const.SOUTH_NODE)

	#to access attributes
	#sun.id, sun.lon, sun.sign, son.signlon, sun.lonspeed

	#Get house objects
	asc = chart.get(const.ASC)
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

	#pass chart object to template
	return render_template('ephemeris.html', all_objs=all_objs)


if __name__ == "__main__":
     app.run()
