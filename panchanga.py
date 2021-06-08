import datetime
from datetime import date
from datetime import timedelta
import time
from funcs import *
from shadvarga import *
import pytz

tithis_dict = { 1:  "Śukla pakṣa prathamā",
            2:  "Śukla pakṣa dvitīyā",
            3:  "Śukla pakṣa tṛtīyā",
            4:  "Śukla pakṣa caturthī",
            5:  "Śukla pakṣa pañcamī",
            6:  "Śukla pakṣa ṣaṣṭhī",
            7:  "Śukla pakṣa saptamī",
            8:  "Śukla pakṣa aṣṭhamī",
            9:  "Śukla pakṣa navamī",
            10: "Śukla pakṣa daśamī",
            11: "Śukla pakṣa ekādaśī",
            12: "Śukla pakṣa dvādaśī",
            13: "Śukla pakṣa trayodaśī",
            14: "Śukla pakṣa caturdasī",
            15: "Pūrṇimā",
            16: "Kṛṣṇa pakṣa prathamā",
            17: "Kṛṣṇa pakṣa dvitīyā",
            18: "Kṛṣṇa pakṣa tṛtīyā",
            19: "Kṛṣṇa pakṣa caturthī",
            20: "Kṛṣṇa pakṣa pañcamī",
            21: "Kṛṣṇa pakṣa ṣaṣṭhi",
            22: "Kṛṣṇa pakṣa saptamī",
            23: "Kṛṣṇa pakṣa aṣṭhamī",
            24: "Kṛṣṇa pakṣa navamī",
            25: "Kṛṣṇa pakṣa daśamī",
            26: "Kṛṣṇa pakṣa ekādaśī",
            27: "Kṛṣṇa pakṣa dvādaśī",
            28: "Kṛṣṇa pakṣa trayodaśī",
            29: "Kṛṣṇa pakṣa caturdasī",
            30: "Amāvāsyā"
           }

#Get the daily motion of Sun, Moon etc. in degrees
def get_daily_motion(planets_dict_lon_only, date_dict):

  daily_motion_dict = {}

  #calculate pos for next day
  today_date = date_dict['date']
  today_date = datetime.datetime.strptime(today_date, "%Y/%m/%d")
  tmrw_date = today_date + datetime.timedelta(days = 1)
  tmrw_date = tmrw_date.strftime('%Y/%m/%d')

  #Calculate the planetary positions tomorrow
  planets_dict_tmrw, houses_dict_tmrw, planets_dict_lon_only_tmrw, houses_dict_signlon_tmrw, chart_tmrw = calc_allpos(tmrw_date, date_dict['time_of_day'], date_dict['city'], date_dict['tz'])

  for p in ["Sun", "Moon"]:
    p_lon = planets_dict_lon_only[p][1]
    p_lon_tmrw = planets_dict_lon_only_tmrw[p][1]
    daily_motion_dict[p] = p_lon_tmrw - p_lon

  return daily_motion_dict

#Get tithi for a given place
def get_tithi(planets_dict_lon_only, date_dict):

  panchanga_dict = date_dict

  sun_lon = planets_dict_lon_only["Sun"][1]
  moon_lon = planets_dict_lon_only["Moon"][1]

  if moon_lon < sun_lon:
    tithi_lon = moon_lon + 360 - sun_lon
  else:
    tithi_lon = moon_lon - sun_lon

  #Find the tithi numnber, one tithi is 12 deg
  tithi_num = tithi_lon / 12 + 1
  tithi_name = tithis_dict[int(tithi_num)]
  #print(f"Date: {date_dict['date']}, Place: {date_dict['city']}")
  #print(f"Tithi is: {tithi_name}")
  #print(f"Next tithi begins at degrees: { int(tithi_num) * 12 }")
  rem_distance = (int(tithi_num) * 12) - tithi_lon
  #print(f"Remaining distance for {tithi_name}: {(int(tithi_num) * 12) - tithi_lon } ")

  #Daily motion of Sun, Moon
  daily_motion_dict = get_daily_motion(planets_dict_lon_only, date_dict)

  #print(daily_motion_dict)
  #Time to cover remaining distance
  hrs_to_tithi_end = ( rem_distance / ( daily_motion_dict["Moon"] - daily_motion_dict["Sun"] ) ) * 24
  mins_to_tithi_end = hrs_to_tithi_end * 60

  #Start the day at 5.30 AM
  day_begins = "5:30"
  tithi_end_time = datetime.datetime.strptime(day_begins, "%H:%M") + datetime.timedelta(minutes = mins_to_tithi_end)
  tithi_end_time_fmt = tithi_end_time.strftime("%H:%M")
  print(f"Date: {date_dict['date']}, Tithi: {tithi_name}, Ends: {tithi_end_time_fmt}")

  date_dict["tithi_name"] = tithi_name
  date_dict["tithi_end_time"] = tithi_end_time_fmt

  #print(panchanga_dict)
  return panchanga_dict

def get_monthly_panchanga(date):

  


  print("monthly")

if __name__ == "__main__":
  

  #date = "2021/06/07"
  time_of_day = "5:30"
  city = "hyderabad"
  tz = 5.5

  #curr_date = datetime.datetime.now(pytz.timezone("Asia/Calcutta"))
  curr_date = datetime.datetime(2020, 7, 1)
  curr_date_fmt = curr_date.strftime('%d-%m-%Y')
  date_swisseph_fmt_date = curr_date.strftime('%Y/%m/%d')
  planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(date_swisseph_fmt_date, time_of_day, city, tz)

  num_of_days_month =  (date(curr_date.year, curr_date.month + 1, 1) - date(curr_date.year, curr_date.month, 1)).days
  
  month_panchanga = {}
  for d in range(1, num_of_days_month + 1):
    dt = f"{curr_date.year}/{curr_date.month}/{d}"
    date_dict = { "date": dt, "date_fmt":dt, "time_of_day": time_of_day, "city": city, "tz": tz } 
    planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(dt, time_of_day, city, tz)
    month_panchanga[dt] = get_tithi(planets_dict_lon_only, date_dict)
   #panchanga_dict = get_tithi(planets_dict_lon_only, date_dict)

  #print(month_panchanga)
  #get_tithi(planets_dict_lon_only, date_dict)