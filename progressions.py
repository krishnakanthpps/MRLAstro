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

	#DOB change format for jinja2
	dob_for_prnt = dob.strftime('%d-%m-%Y')

	today = datetime.datetime.utcnow()
	today_prnt = today.strftime('%d-%m-%Y')

	#get current age of person in years to dob_from_prg and get dob_to_prg
	curr_age = today - dob
	curr_age_yrs = int((curr_age.days)/365) + 1

	#add this number of days to dob to get new progressed date
	prg_date = dob + datetime.timedelta(days=curr_age_yrs)

	#generate d-m-yyyy formatted string for jinja2
	prg_date_prnt = prg_date.strftime('%d-%m-%Y')
	#convert the date obj to yyyy/mm/dd string format, also
	prg_date = prg_date.strftime('%Y/%m/%d')
	

	#Generate the new progressed chart objects for the new date
	planets_dict_prg = {}
	houses_dict_prg = {}
	planets_dict_lon_only_prg = {}

	planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg = calc_allpos(prg_date, tob, city, tz)

	prg_details_dict = {}
	prg_details_dict['dob'] = str(dob_for_prnt)
	prg_details_dict['curr_age'] = str(curr_age_yrs - 1)
	prg_details_dict['prg_date'] = str(prg_date_prnt)
	prg_details_dict['today_date'] = str(today_prnt)
	
	#print("########## printing PRG PLANETS############")
	print(prg_details_dict)
	#print(houses_dict_prg)
	#print("######### END ##############")

	return planets_dict_prg, houses_dict_prg, prg_details_dict


	#generate the progressed chart for this to date


	#end_date = date_1 + datetime.timedelta(days=34)
	#dob_prg = dob.split('/')
	#planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg = calc_allpos(dob, tob, city, tz)	

dob = '1986/5/28'
tob = '12:25'
tz = '5:30'
city = 'Hyderabad'

print("########")
print(calc_progressions(dob, tob, city, tz))
