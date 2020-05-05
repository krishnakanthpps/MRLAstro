import datetime

#Calculate progressions for below date and time for now.
dob='1986/5/28'
tob = '12:25'

dob_tob = dob+' '+tob
dob_tob = datetime.datetime.strptime(dob_tob, "%Y/%m/%d %H:%M")

dob = datetime.datetime.strptime(dob, "%Y/%m/%d")
tob = datetime.datetime.strptime(tob, "%H:%M")

#today = datetime.datetime.utcnow()
today = datetime.datetime.utcnow()

curr_age = today - dob
curr_age_yrs = int((curr_age.days)/365)
prg_date = dob_tob + datetime.timedelta(days=curr_age_yrs)
#prg_date = dob_tob
#check if birthday already occured

bday_this_year = datetime.datetime(today.year, dob.month, dob.day)
bday_previous_year = datetime.datetime(today.year - 1, dob.month, dob.day)

#check if bday already occured
bday_passed = today - bday_this_year

if bday_passed.days < 0:
	print('bday yet to occur')
	#calculate number of days elapsed since last years bday
	days_since_last_bday=(today - bday_previous_year)
	print('days_since_last_bday: '+str(days_since_last_bday.days))
	
	"""convert this into progressed hours to represent year in progressed days
	1 year = 1 progressed day
	365 days = 24 progressed hrs
	1 day = 24/365 progressed hrs"""

	#get hours to add to birthtime 
	hours_to_add = (days_since_last_bday * 24/365).days

	print("adding these hours to birthtime: "+str(hours_to_add))
	print("Prg date before adding hours: "+str(prg_date))

	prg_date = prg_date + datetime.timedelta(hours=hours_to_add)

	print("Prg date after adding hours: "+str(prg_date))
	

	print("Correct progression date and time: "+str(prg_date))

else:
	print('bday has passed')
	#calculate number of days elapsed since current year bday
	days_since_last_bday=(today - bday_this_year)
	print('days_since_last_bday: '+str(days_since_last_bday.days))

	#get hours to add to birthtime 
	hours_to_add = (days_since_last_bday * 24/365).days

	print("adding these hours to birthtime: "+str(hours_to_add))
	prg_date = dob + datetime.timedelta(days=curr_age_yrs) + datetime.timedelta(hours=hours_to_add)

	print("Correct progression date and time: "+str(prg_date))




#print(bday_passed)
#print(str(bday_this_year))
#print(str(bday_previous_year))

#print('DOB is: '+str(dob))
#print('Date today is: '+str(today))
#print('Progressed date is: '+str(prg_date))
#print('Age: '+str(curr_age_yrs))

#print(tob.hour)


