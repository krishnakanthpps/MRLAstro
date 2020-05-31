from flask import Flask, render_template, session, redirect, url_for, request, redirect
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from funcs import *
import datetime
from datetime import date


zs_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']	


#planets_dict, houses_dict, planets_dict_lon_only = calc_allpos(dob, tob, city, tz)

def calc_progressions(dob, tob, city, tz, prg_to_date):
	
	"""

	"""
	planets_dict_prg = {}
	houses_dict_prg = {}
	planets_dict_lon_only_prg = {}
	prg_details_dict = {}

	dob_tob = dob+' '+tob
	dob_tob = datetime.datetime.strptime(dob_tob, "%Y/%m/%d %H:%M")
	
	#make it a datetime object
	dob = datetime.datetime.strptime(dob, "%Y/%m/%d")
	prg_to_date = datetime.datetime.strptime(prg_to_date, "%Y/%m/%d")
	dob_for_prnt = dob.strftime('%d-%m-%Y')

	#today = datetime.datetime.utcnow()
	today_prnt = prg_to_date.strftime('%d-%m-%Y')

	#get current age of person in years to dob_from_prg and get dob_to_prg
	curr_age = prg_to_date - dob
	curr_age_yrs = int((curr_age.days)/365) 

	prg_date = dob_tob + datetime.timedelta(days=curr_age_yrs)

	#check if birthday already occured
	bday_this_year = datetime.datetime(prg_date.year, dob.month, dob.day)
	bday_previous_year = datetime.datetime(prg_date.year - 1, dob.month, dob.day)

	#check if bday already occured
	bday_passed = prg_date - bday_this_year

	if bday_passed.days < 0:
		#print('bday yet to occur this year')
		#calculate number of days elapsed since last years bday
		days_since_last_bday=(prg_date - bday_previous_year)
		#print('days_since_last_bday: '+str(days_since_last_bday.days))
		
		"""convert this into progressed hours to represent year in progressed days
		1 year = 1 progressed day
		365 days = 24 progressed hrs
		1 day = 24/365 progressed hrs"""

		#get hours to add to birthtime 
		hours_to_add = (days_since_last_bday * 24/365).days

		#print("adding these hours to birthtime: "+str(hours_to_add))
		#print("Prg date before adding hours: "+str(prg_date))
		prg_date = prg_date + datetime.timedelta(hours=hours_to_add)

		#print("Prg date after adding hours: "+str(prg_date))
		#print("New PRG date with hours added is: "+str(prg_date))
		#print("Correct progression date and time: "+str(prg_date))
		
		prg_date_prnt = prg_date
		prg_date = prg_date.strftime('%Y/%m/%d')

		#format change for jinja2
		prg_date_prnt = prg_date_prnt.strftime('%d-%m-%Y')

		#Generate the new progressed chart objects for the new date
		planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg, houses_dict_signlon = calc_allpos(prg_date, tob, city, tz)
		prg_details_dict['dob'] = str(dob_for_prnt)
		prg_details_dict['curr_age'] = str(curr_age_yrs)
		prg_details_dict['prg_date'] = str(prg_date_prnt)
		prg_details_dict['today_date'] = str(today_prnt)
	

		#return planets_dict_prg, houses_dict_prg, prg_details_dict

	else:
		#This block executes if birthday has already passed in current year
		#print('bday has passed')
		#calculate number of days elapsed since current year bday
		days_since_last_bday=(prg_date - bday_this_year)
		#print('days_since_last_bday: '+str(days_since_last_bday.days))
		
		"""convert this into progressed hours to represent year in progressed days
		1 year = 1 progressed day
		365 days = 24 progressed hrs
		1 day = 24/365 progressed hrs"""

		#get hours to add to birthtime 
		hours_to_add = (days_since_last_bday * 24/365).days

		#print("adding these hours to birthtime: "+str(hours_to_add))
		#print("Prg date before adding hours: "+str(prg_date))
		prg_date = prg_date + datetime.timedelta(hours=hours_to_add)

		#print("Prg date after adding hours: "+str(prg_date))
		#print("New PRG date with hours added is: "+str(prg_date))
		#print("Correct progression date and time: "+str(prg_date))
		
		prg_date_prnt = prg_date
		prg_date = prg_date.strftime('%Y/%m/%d')

		#format change for jinja2
		prg_date_prnt = prg_date_prnt.strftime('%d-%m-%Y')

		#Generate the new progressed chart objects for the new date
		planets_dict_prg, houses_dict_prg, planets_dict_lon_only_prg, houses_dict_signlon = calc_allpos(prg_date, tob, city, tz)
		prg_details_dict['dob'] = str(dob_for_prnt)
		prg_details_dict['curr_age'] = str(curr_age_yrs)
		prg_details_dict['prg_date'] = str(prg_date_prnt)
		prg_details_dict['today_date'] = str(today_prnt)

	

	return planets_dict_prg, houses_dict_prg, prg_details_dict

#calculates transits for current utc time
def calc_transits():

	planets_dict_transit= {}
	houses_dict_transit = {}
	planets_dict_lon_only_transit = {}
	p_and_h_dict_transit = {}

	today = datetime.datetime.utcnow()
	transit_date = today.strftime('%Y/%m/%d')
	transit_time = today.strftime('%H:%M')

	#Set the timezone to UTC/GMT, we calculate transits to this timezone
	tz = "00:00"
	city = "London"

	planets_dict_transit, houses_dict_transit, planets_dict_lon_only_transit, houses_dict_signlon = calc_allpos(transit_date, transit_time, city, tz)

	for sign in zs_list:
		p_and_h_dict_transit[sign] = getPrintableObjects(sign, planets_dict_transit, houses_dict_transit, p_only=True)

	return p_and_h_dict_transit


#DEBUGGING 

# dob = '1958/3/9'
# tob = '12:25'
# tz = '5:30'
# city = 'Hyderabad'

# calc_transits(dob, tob, city, tz)

"""
# print("########")
# calc_progressions(dob, tob, city, tz)

dob='1958/3/9'
dob = datetime.datetime.strptime(dob, "%Y/%m/%d")
today = datetime.datetime.utcnow()
curr_age = today - dob
curr_age_yrs = int((curr_age.days)/365)
prg_date = dob + datetime.timedelta(days=curr_age_yrs)

print('Progressed date is: '+str(prg_date))
print('Age: '+str(curr_age_yrs))
"""

