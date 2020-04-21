from flask import Flask, render_template
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/ephemeris')	
def getChart():
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

	#pass chart object to template
	return render_template('ephemeris.html', all_objs=all_objs)


	
