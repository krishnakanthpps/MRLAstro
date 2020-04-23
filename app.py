from flask import Flask, render_template, session, redirect, url_for, request, redirect
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from funcs import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghij'


@app.route('/', methods=['GET','POST'])
def index():
	name = 'aditya'
	return '<h1>Hello, {}!</h1>'.format(name)

#Chart creation page
@app.route('/enterdetails', methods=['GET'])
def enterdetails():
	#shows horoscope details entry form
	return render_template('enterdetails.html')

#Chart creation page
@app.route('/showchart', methods=['GET','POST'])
def showchart():
	
	#get the date and tob from form
	#get the pob from form, html input formats below
	#Time: 3 03 03
	#Timezone: -6
	birth_name = request.form['birth_name']
	country = request.form['country']
	city = request.form['city']
	state = request.form['state']
	
	day = request.form['dob_day']
	month = request.form['dob_month']
	year = request.form['dob_year']
	#generate dob in yyyy/mm/dd format
	dob = year+'/'+month+'/'+day

	hour = request.form['tob_hour']
	minute = request.form['tob_minute']
	second = request.form['tob_second']
	#generate tob in hh:mm format
	tob = hour+":"+minute

	tz = request.form['timezone']
	#generate tz in +/-hh:mm format
	tz = tz+":"+"00"

	#get all the planetary and house positions
	#pass all parameters generated above
	planets_dict, houses_dict = calc_allpos(dob, tob, city, tz)
	#sun = planets_dict['Sun'][0]

	## DEBUG ##
	city_lat, city_lon = get_lat_lon(city)
	print("Name: "+birth_name)
	print("DOB: "+dob)
	print("City: "+city+" "+str(city_lat)+" "+str(city_lon))
	print("Time: "+str(tob))
	print("Timezone: "+tz)

	#return redirect(url_for('showchart'))
	return render_template('display_chart.html', planets_dict=planets_dict, houses_dict=houses_dict, birth_name=birth_name, dob=dob, city=city, tob=tob, tz=tz)


@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, {}!</h1>'.format(name)

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


	
