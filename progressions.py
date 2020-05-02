from flask import Flask, render_template, session, redirect, url_for, request, redirect
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from funcs import *
import datetime
from datetime import date


#planets_dict, houses_dict, planets_dict_lon_only = calc_allpos(dob, tob, city, tz)

def calc_progressions(dob, tob, city, tz):
	
	"""


	"""
	zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']	

	#make it a datetime object, we set progressed time to utc
	dob = datetime.datetime.strptime(dob, "%Y/%m/%d")
	today = datetime.datetime.utcnow()

	#get current age of person in years to dob_from_prg and get dob_to_prg
	curr_age = today - dob
	curr_age_yrs = int((curr_age.days)/365) + 1

	#add this number of days to dob to get new progressed date
	prg_date = dob + datetime.timedelta(days=curr_age_yrs)

	#convert the date obj to yyyy/mm/dd string format
	prg_date = prg_date.strftime('%Y/%m/%d')

	#Generate the new progressed chart objects for the new date
	planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg = calc_allpos(prg_date, tob, city, tz)

	mystr = "Birthday: "+str(dob)+", \ncurrent age is: "+str(curr_age_yrs) + ", \nProgressed date is: "+str(prg_date)
	
	print("########## printing PRG PLANETS############")
	print(mystr)
	print(planets_dict_prg)
	print("######### END ##############")

	return planets_dict_prg


	#generate the progressed chart for this to date


	#end_date = date_1 + datetime.timedelta(days=34)
	#dob_prg = dob.split('/')
	#planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg = calc_allpos(dob, tob, city, tz)	

#ob = '28/5/1986'
#tob = '5:10'
#tz = '00:00'
#city = 'London'

print("########")
#print(calc_progressions(dob, tob, city, tz))
