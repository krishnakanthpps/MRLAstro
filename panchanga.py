import datetime
from datetime import date
from datetime import timedelta
import time
from funcs import *
from shadvarga import *
import pytz
import math

tithis_dict = { 1:  "Śukla pakṣa pādyami",
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
            16: "Kṛṣṇa pakṣa pādyami",
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


varas_dict = {
           0: "Bhānuvāra",
           1: "Somavāra",
           2: "Maṅgalavāra",
           3: "Budhavāra",
           4: "Guruvāra",
           5: "Śukravāra",
           6: "Śanivāra",
           7: "Aadivāra"
         }

nakshatras_dict = { 
                1:"Kṛttikā",
                2:"Rohiṇī",
                3:"Mṛgaśirā",
                4:"Ārdrā",
                5:"Punarvasū",
                6:"Puṣya",
                7:"Āśleṣā",
                8:"Maghā",
                9:"Pūrvaphalgunī",
                10:"Uttaraphalgunī",
                11:"Hasta",
                12:"Cittā",
                13:"Svāti",
                14:"Viśākhā",
                15:"Anurādhā",
                16:"Jyeṣṭhā",
                17:"Mūlā",
                18:"Pūrvāṣāḍhā",
                19:"Uttarāṣāḍhā",
                20:"Śravaṇā",
                21:"Dhaniṣṭhā",
                22:"Śatabhiṣā",
                23:"Pūrvābhādrā",
                24:"Uttarābhādrā",
                25:"Revatī",
                26:"Aśvinī",
                27:"Bharaṇī"
              }

nakshatras_dict_trad = { 
                1:"Aśvinī",
                2:"Bharaṇī",
                3:"Kṛttikā",
                4:"Rohiṇī",
                5:"Mṛgaśirā",
                6:"Ārdrā",
                7:"Punarvasū",
                8:"Puṣya",
                9:"Āśleṣā",
                10:"Maghā",
                11:"Pūrvaphalgunī",
                12:"Uttaraphalgunī",
                13:"Hasta",
                14:"Cittā",
                15:"Svāti",
                16:"Viśākhā",
                17:"Anurādhā",
                18:"Jyeṣṭhā",
                19:"Mūlā",
                20:"Pūrvāṣāḍhā",
                21:"Uttarāṣāḍhā",
                22:"Śravaṇā",
                23:"Dhaniṣṭhā",
                24:"Śatabhiṣā",
                25:"Pūrvābhādrā",
                26:"Uttarābhādrā",
                27:"Revatī"
              }


yogas_dict = {
           1:"Viṣkumbha",
           2:"Prīti",
           3:"Āyuṣmān",
           4:"Saubhāgya",
           5:"Śobhana",
           6:"Atigaṇḍa",
           7:"Sukarmā",
           8:"Dhṛti",
           9:"Śūla",
           10:"Gaṇḍa",
           11:"Vṛddhi",
           12:"Dhruva",
           13:"Vyāghāta",
           14:"Harṣaṇa",
           15:"Vajra",
           16:"Siddhi",
           17:"Vyatīpāta",
           18:"Vārīyana",
           19:"Parigha",
           20:"Śiva",
           21:"Siddha",
           22:"Sādhya",
           23:"Śubha",
           24:"Śukla",
           25:"Brahma",
           26:"Aindra",
           27:"Vaidhṛti"
         }


karanas_dict = {
             1:"Kiṃstughna",
             2:"Bava",
             3:"Bālava",
             4:"Kaulava",
             5:"Taitila",
             6:"Garaja",
             7:"Vaṇija",
             8:"Viṣṭi",
             9:"Bava",
             10:"Bālava",
             11:"Kaulava",
             12:"Taitila",
             13:"Garaja",
             14:"Vaṇija",
             15:"Viṣṭi",
             16:"Bava",
             17:"Bālava",
             18:"Kaulava",
             19:"Taitila",
             20:"Garaja",
             21:"Vaṇija",
             22:"Viṣṭi",
             23:"Bava",
             24:"Bālava",
             25:"Kaulava",
             26:"Taitila",
             27:"Garaja",
             28:"Vaṇija",
             29:"Viṣṭi",
             30:"Bava",
             31:"Bālava",
             32:"Kaulava",
             33:"Taitila",
             34:"Garaja",
             35:"Vaṇija",
             36:"Viṣṭi",
             37:"Bava",
             38:"Bālava",
             39:"Kaulava",
             40:"Taitila",
             41:"Garaja",
             42:"Vaṇija",
             43:"Viṣṭi",
             44:"Bava",
             45:"Bālava",
             46:"Kaulava",
             47:"Taitila",
             48:"Garaja",
             49:"Vaṇija",
             50:"Viṣṭi",
             51:"Bava",
             52:"Bālava",
             53:"Kaulava",
             54:"Taitila",
             55:"Garaja",
             56:"Vaṇija",
             57:"Viṣṭi",
             58:"Śakuni",
             59:"Catuṣpāda",
             60:"Nāgava"
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
  planets_dict_tmrw, houses_dict_tmrw, planets_dict_lon_only_tmrw, houses_dict_signlon_tmrw, chart_tmrw = calc_allpos(tmrw_date, date_dict['day_begins'], date_dict['city'], date_dict['tz'])

  for p in ["Sun", "Moon"]:
    p_lon = planets_dict_lon_only[p][1]
    p_lon_tmrw = planets_dict_lon_only_tmrw[p][1]
    daily_motion_dict[p] = p_lon_tmrw - p_lon

  return daily_motion_dict

#Get tithi for a given place
def get_tithi(planets_dict_lon_only, date_dict):

  tithi_dict = {}

  sun_lon = planets_dict_lon_only["Sun"][1]
  moon_lon = planets_dict_lon_only["Moon"][1]

  if moon_lon < sun_lon:
    tithi_lon = moon_lon + 360 - sun_lon
  else:
    tithi_lon = moon_lon - sun_lon

  #Find the tithi numnber, one tithi is 12 deg
  tithi_num = tithi_lon / 12 + 1
  tithi_name = tithis_dict[int(tithi_num)]
  rem_distance = (int(tithi_num) * 12) - tithi_lon

  #Daily motion of Sun, Moon
  daily_motion_dict = get_daily_motion(planets_dict_lon_only, date_dict)

  #Time to cover remaining distance
  hrs_to_tithi_end = ( rem_distance / ( daily_motion_dict["Moon"] - daily_motion_dict["Sun"] ) ) * 24
  mins_to_tithi_end = hrs_to_tithi_end * 60

  #Start the day at 5.30 AM
  day_begins = "5:30"
  tithi_end_time = datetime.datetime.strptime(day_begins, "%H:%M") + datetime.timedelta(minutes = mins_to_tithi_end)
  tithi_end_time_fmt = tithi_end_time.strftime("%H:%M")

  tithi_dict["date"] =  date_dict["date"]
  tithi_dict["tithi_name"] = tithi_name
  tithi_dict["tithi_end_time"] = tithi_end_time_fmt

  return tithi_dict

#Returns the weekday for a given date
def get_vara(date_dict):

  weekday_num = date_dict['date_obj'].weekday()
  weekday_num = weekday_num + 1
  weekday_name = varas_dict[weekday_num] 

  return weekday_name


#Returns the nakshatra for a given date
def get_nakshatra(date_dict, planets_dict_lon_only):

  moon_lon = planets_dict_lon_only["Moon"][1]
  daily_motion_dict = get_daily_motion(planets_dict_lon_only, date_dict)
  
  #temp ayanamsa
  #moon_lon = moon_lon - 23.5900

  one_pada = (360 / (12 * 9))  # There are also 108 navamsas
  one_nakshatra = (360 / 27)

  nakshatras_elapsed = int(moon_lon / one_nakshatra)
  nak_num = nakshatras_elapsed + 1

  rem_distance = ( nak_num * one_nakshatra ) - moon_lon

  hrs_to_nak_end = ( rem_distance / daily_motion_dict["Moon"] ) * 24
  mins_to_nak_end = hrs_to_nak_end * 60

  day_begins = date_dict["day_begins"]
  nak_end_time = datetime.datetime.strptime(day_begins, "%H:%M") + datetime.timedelta(minutes = mins_to_nak_end)
  nak_end_time_fmt = nak_end_time.strftime("%H:%M")
  #print(f"nak_end_time: {nak_end_time_fmt }")

  padas_elapsed = int(moon_lon / one_pada)
  pada_num = (padas_elapsed + 1) % 4
  
  nakshatra_name = nakshatras_dict[nak_num]
  nakshatra_name = f"{nakshatra_name} ends {nak_end_time_fmt}"

  #print(f"nakshatra_name: {nakshatra_name}")
  return nakshatra_name


#Returns the Yoga
def get_yoga(planets_dict_lon_only, date_dict):

  yoga_dict = {}

  sun_lon = planets_dict_lon_only["Sun"][1]  
  moon_lon = planets_dict_lon_only["Moon"][1]
  daily_motion_dict = get_daily_motion(planets_dict_lon_only, date_dict)

  #nirayana test
  #sun_lon = sun_lon - 23.5900
  #moon_lon = moon_lon - 23.5900

  total_lon = sun_lon + moon_lon
  if total_lon > 360:
    total_lon = total_lon - 360

  #divide by 13d20m
  one_yoga = (360 / 27)
  yoga_num = int((total_lon / one_yoga) + 1)
  yoga_name = yogas_dict[yoga_num]

  rem_distance = (yoga_num * one_yoga) - total_lon

  daily_motion_total = daily_motion_dict["Moon"] + daily_motion_dict["Sun"]
  hrs_to_yoga_end = rem_distance / daily_motion_total 
  hrs_to_yoga_end = hrs_to_yoga_end * 24
  mins_to_yoga_end = hrs_to_yoga_end * 60

  day_begins = date_dict["day_begins"]
  yoga_end_time = datetime.datetime.strptime(day_begins, "%H:%M") + datetime.timedelta(minutes = mins_to_yoga_end)
  yoga_end_time_fmt = yoga_end_time.strftime("%H:%M")

  return yoga_name

def get_karana(planets_dict_lon_only, date_dict):

  karana_dict = {}

  sun_lon = planets_dict_lon_only["Sun"][1]
  moon_lon = planets_dict_lon_only["Moon"][1]
  #nirayana test
  #sun_lon = sun_lon - 23.5900
  #moon_lon = moon_lon - 23.5900

  if moon_lon < sun_lon:
    tithi_lon = moon_lon + 360 - sun_lon
  else:
    tithi_lon = moon_lon - sun_lon

  #Find the tithi numnber, one tithi is 12 deg
  tithi_num = int(tithi_lon / 12 + 1)

  today = tithi_lon / 6
  degrees_left = today * 6 - tithi_lon

  karana_num = int(today) + 1
  karana_name = karanas_dict[karana_num]

  #print(karana_name)

  return karana_name

#Returns panchanga for a month
# def get_monthly_panchanga(date):
#   # num_of_days_month =  (date(curr_date.year, curr_date.month + 1, 1) - date(curr_date.year, curr_date.month, 1)).days  
#   # month_panchanga = {}
#   # for d in range(1, num_of_days_month + 1):
#   #   dt = f"{curr_date.year}/{curr_date.month}/{d}"
#   #   date_dict = { "date": dt, "date_obj":curr_date, "date_fmt":dt, "day_begins": day_begins, "city": city, "tz": tz } 
#   #   planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(dt, day_begins, city, tz)
#   #   month_panchanga[dt] = get_tithi(planets_dict_lon_only, date_dict)
#   print("Todo")


############################################################################
# Calculates the tithi, vara, nakshatra, yoga and karana for a given date. #
############################################################################
def get_panchanga(date_dict, monthly=False):

  panchanga_dict = {}
  day_begins = "5:30"
  city = "hyderabad"
  tz = 5.5

  #Get the current date, time in India
  curr_date = datetime.datetime.now(pytz.timezone("Asia/Calcutta"))
  #curr_date = datetime.datetime(1996, 6, 1)
  curr_date_fmt = curr_date.strftime('%d-%m-%Y')
  date_swisseph_fmt_date = curr_date.strftime('%Y/%m/%d')

  date_dict = { "date": date_swisseph_fmt_date, "date_obj":curr_date, "date_fmt":curr_date_fmt, "day_begins": day_begins, "city": city, "tz": tz } 
  
  #merge panchanga_dict & date_dict
  panchanga_dict = { **panchanga_dict, **date_dict }
  
  #Get the required information
  planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(date_swisseph_fmt_date, day_begins, city, tz)
  panchanga_dict['tithi'] = get_tithi(planets_dict_lon_only, date_dict)
  panchanga_dict['vara'] = get_vara(date_dict)
  panchanga_dict['nakshatra'] = get_nakshatra(date_dict, planets_dict_lon_only)
  panchanga_dict['yoga'] = get_yoga(planets_dict_lon_only, date_dict)
  panchanga_dict['karana'] = get_karana(planets_dict_lon_only, date_dict)


  #print(f"panchanga_dict: {panchanga_dict}")
  return panchanga_dict


if __name__ == "__main__":
  

  #date = "2021/06/07"
  day_begins = "5:30"
  city = "hyderabad"
  tz = 5.5

  #curr_date = datetime.datetime.now(pytz.timezone("Asia/Calcutta"))
  curr_date = datetime.datetime(2020, 7, 1)
  curr_date_fmt = curr_date.strftime('%d-%m-%Y')
  date_swisseph_fmt_date = curr_date.strftime('%Y/%m/%d')
  planets_dict, houses_dict, planets_dict_lon_only, houses_dict_signlon, chart = calc_allpos(date_swisseph_fmt_date, day_begins, city, tz)
  date_dict = { "date": date_swisseph_fmt_date, "date_obj":curr_date, "date_fmt":curr_date_fmt, "day_begins": day_begins, "city": city, "tz": tz } 
  
  panchanga_dict = get_tithi(planets_dict_lon_only, date_dict)

  #print(month_panchanga)
  
