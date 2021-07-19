from flask import Flask, render_template, session, redirect, url_for, request, redirect
from jinja2 import Environment, PackageLoader, select_autoescape
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from datetime import date
from funcs import *
from progressions import *
from shadvarga import *
from shadbala import *
from panchanga import *
import json
from flask_moment import Moment
import pytz


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    keep_trailing_newline=True
)

png_dict = {
	"Su":"static/png/planets/sun.png",
	"Mo":"static/png/planets/moon.png",
	"Ma":"static/png/planets/mars.png",
	"Me":"static/png/planets/mercury.png",
	"Ju":"static/png/planets/jupiter.png",
	"Ve":"static/png/planets/venus.png",
	"Sa":"static/png/planets/saturn.png",
	"Ur":"static/png/planets/uranus.png",
	"Ne":"static/png/planets/neptune.png",
	"Pl":"static/png/planets/pluto.png",
	"Ra":"static/png/planets/rahu.png",
	"Ke":"static/png/planets/ketu.png",
	"K":"static/png/planets/chiron.png",
	"I":"static/png/houses/1.png",
	"II":"static/png/houses/2.png",
	"III":"static/png/houses/3.png",
	"IV":"static/png/houses/4.png",
	"V":"static/png/houses/5.png",
	"VI":"static/png/houses/6.png",
	"VII":"static/png/houses/7.png",
	"VIII":"static/png/houses/8.png",
	"IX":"static/png/houses/9.png",
	"X":"static/png/houses/10.png",
	"XI":"static/png/houses/11.png",
	"XII":"static/png/houses/12.png"
}

unicode_dict = {
	"Su":"\u2609",
	"Mo":"\u263D",
	"Ma":"\u2642",
	"Me":"\u263F",
	"Ju":"\u2643",
	"Ve":"\u2640",
	"Sa":"\u2644",
	"Ur":"\u2645",
	"Ne":"\u2646",
	"Pl":"\u2647",
	"Ra":"\u260A",
	"Ke":"\u260B",
	"K":"\u26B7",
	"I":"I",
	"II":"II",
	"III":"III",
	"IV":"IV",
	"V":"V",
	"VI":"VI",
	"VII":"VII",
	"VIII":"VIII",
	"IX":"IX",
	"X":"X",
	"XI":"XI",
	"XII":"XII"
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ff3a5067411e420dcd0245787ba7bc533be5ce4b'

moment = Moment(app)

@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

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
	user_dob = request.form['user_dob']
	print(user_dob);
	dob = user_dob.replace("-","/")

	#Also get the day, month, year for jinja display
	date_list = user_dob.split("-")
	year = date_list[0]
	month = date_list[1]
	day = date_list[2]

	#format in dd-mm-yyyy format for jinja template display
	dob_jinja = day+"-"+month+"-"+year

	#generate tob in hh:mm format
	hour = request.form['tob_hour']
	minute = request.form['tob_minute']
	#second = request.form['tob_second']
	tob = hour+":"+minute

	#generate tz in +/-hh:mm format
	tz = request.form['timezone']

	#get prg date details
	prg_date_now = request.form.get("prg_date_now") 
	if prg_date_now is None:
		prg_day = request.form['prg_day']
		prg_month = request.form['prg_month']
		prg_year = request.form['prg_year']
		prg_date = prg_year+'/'+prg_month+'/'+prg_day
	else:
		#set prg date to today
		prg_date = datetime.datetime.utcnow()
		prg_date = prg_date.strftime('%Y/%m/%d')


	#get all the planet and house positions (raw - no formatting)
	planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(dob, tob, city, tz)
	
	#zodiac sign list
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
	
	#dicts to store formatted objects in zodiac sign - [planet_positions] format
	p_and_h_dict = {}
	navamsa_dict = {}

	#Generate dict for jinja2 with planets, houses and their positions
	for sign in zs_list:
		p_and_h_dict[sign] = getPrintableObjects(sign, planets_dict, houses_dict)

	#Navamsa dict - keys = zodiac sign; value = list of planets in that navamsa
	for sign in zs_list:
		navamsa_dict[sign] = navamsa_from_long(sign, planets_dict_lon_only)

	#Progressions dict - calculate progressions
	prog_pl_dict = {}
	prog_houses_dict = {}

	prog_pl_dict, prog_houses_dict, prg_details = calc_progressions(dob, tob, city, tz, prg_date)

	#generate printable objects for progressions
	progressions_dict_pr = {}
	for sign in zs_list:	
		progressions_dict_pr[sign] = getPrintableObjects(sign, prog_pl_dict, prog_houses_dict)

	#Generate transit chart 
	p_and_h_dict_transits = calc_transits()
	#print(p_and_h_dict_transits)

	#####Generate Sharvargas####
	hora_dict = calc_horas(planets_dict_lon_only)
	drekkana_dict = calc_drekkana(planets_dict_lon_only)
	dwa_dict = calc_dwadasamsa(planets_dict_lon_only)
	trimsamsa_dict = calc_trimsamsa(planets_dict_lon_only, houses_dict_signlon)
	saptamsa_dict = calc_saptamsa(planets_dict_lon_only)

	#Store all varga dicts in one place
	shadvarga_dict = {}
	shadvarga_dict['hora_dict'] = hora_dict
	shadvarga_dict['drekkana_dict'] = drekkana_dict
	shadvarga_dict['dwa_dict'] = dwa_dict
	shadvarga_dict['navamsa_dict'] = navamsa_dict
	shadvarga_dict['trimsamsa_dict'] = trimsamsa_dict
	shadvarga_dict['saptamsa_dict'] = saptamsa_dict
	shadbala_dict = calc_shadbalas(planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, shadvarga_dict, chart)

	return render_template('display_chart.html', birth_name=birth_name, dob=dob_jinja, city=city, tob=tob, tz=tz, p_and_h_dict=p_and_h_dict, planets_dict=planets_dict, houses_dict=houses_dict, navamsa_dict=navamsa_dict, progressions_dict_pr=progressions_dict_pr, prg_details=prg_details, p_and_h_dict_transits=p_and_h_dict_transits, hora_dict=hora_dict, drekkana_dict=drekkana_dict, dwa_dict=dwa_dict, trimsamsa_dict=trimsamsa_dict, shadbala_dict=shadbala_dict, png_dict=png_dict, unicode_dict=unicode_dict)


#Displays Shadbala
@app.route('/shadbala')
def shadbala():

	shadbala_dict = {}

	return render_template('shadbala.html',shadbala_dict=shadbala_dict)


@app.route('/panchanga', methods=['GET','POST'])
def panchanga():

	date_dict = {}
	#Generate the panchanga
	panchanga_dict = get_panchanga(date_dict, monthly=False)

	
	return render_template('panchanga.html', panchanga_dict=panchanga_dict)


if __name__ == "__main__":
     app.run()
