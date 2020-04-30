from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from geopy.geocoders import Nominatim
from natsort import natsorted


planets_dict_lon_only = {'Sun': ['Capricorn', 280.6207851104341], 'Moon': ['Capricorn', 279.0134285621015], 'Mars': ['Capricorn', 284.22091380947154], 'Mercury': ['Sagittarius', 259.5856274398878], 'Jupiter': ['Sagittarius', 241.2254528485053], 'Venus': ['Aquarius', 306.944335271235], 'Saturn': ['Sagittarius', 267.7701090407931], 'Uranus': ['Sagittarius', 250.16451338523655], 'Neptune': ['Gemini', 85.20635329394686], 'Pluto': ['Gemini', 75.24341806127518], 'Rahu': ['Sagittarius', 259.1370587759099], 'Ketu': ['Gemini', 79.1370587759099]}

sign_list = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

navamsa_dict = {}

planets_dict = {'Sun': ['Capricorn', [10, 37, 15]], 'Moon': ['Capricorn', [9, 0, 48]], 'Mars': ['Capricorn', [14, 13, 15]], 'Mercury': ['Sagittarius', [19, 35, 8]], 'Jupiter': ['Sagittarius', [1, 13, 32]], 'Venus': ['Aquarius', [6, 56, 40]], 'Saturn': ['Sagittarius', [27, 46, 12]], 'Uranus': ['Sagittarius', [10, 9, 52]], 'Neptune': ['Gemini', [25, 12, 23]], 'Pluto': ['Gemini', [15, 14, 36]], 'Rahu': ['Sagittarius', [19, 8, 13]], 'Ketu': ['Gemini', [19, 8, 13]]}

houses_dict = {'House1': ['Scorpio', [25, 55, 22]], 'House2': ['Sagittarius', [26, 42, 9]], 'House3': ['Aquarius', [2, 27, 5]], 'House4': ['Pisces', [8, 52, 7]], 'House5': ['Aries', [10, 10, 54]], 'House6': ['Taurus', [5, 13, 37]], 'House7': ['Taurus', [25, 55, 22]], 'House8': ['Gemini', [26, 42, 9]], 'House9': ['Leo', [2, 27, 5]], 'House10': ['Virgo', [8, 52, 7]], 'House11': ['Libra', [10, 10, 54]], 'House12': ['Scorpio', [5, 13, 37]]}

p_and_h_dict = {'Aries': ['V 10\'10"'], 'Taurus': ['VI 5\'13"', 'VII 25\'55"'], 'Gemini': ['Ke 19\'8"', 'Ne 25\'12"', 'Pl 15\'14"', 'VIII 26\'42"'], 'Cancer': [], 'Leo': ['IX 2\'27"'], 'Virgo': ['X 8\'52"'], 'Libra': ['XI 10\'10"'], 'Scorpio': ['I 25\'55"', 'XII 5\'13"'], 'Sagittarius': ['II 26\'42"', 'Ju 1\'13"', 'Me 19\'35"', 'Ra 19\'8"', 'Sa 27\'46"', 'Ur 10\'9"'], 'Capricorn': ['Ma 14\'13"', 'Mo 9\'0"', 'Su 10\'37"'], 'Aquarius': ['III 2\'27"', 'Ve 6\'56"'], 'Pisces': ['IV 8\'52"']}

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    print("#####NATURAL KEYS##### ")
    #print(atoi(c) for c in re.split(r'(\d+)', text)
    
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


#calculate navamsa sign where longitude falls
def getPrintableObjects(sign, planets_dict, houses_dict):
	#print('in funcs, zsign is: '+sign)
	p_list = []
	h_list = []
	test_list = []
	house_chars_dict = {'House1': 'I','House2': 'II','House3': 'III','House4': 'IV','House5': 'V','House6': 'VI','House7': 'VII','House8': 'VIII','House9': 'IX','House10': 'X','House11': 'XI','House12': 'XII',}

	#Get a list of printable planets with deg, mins
	for p,z in planets_dict.items():
		if z[0] == sign:
			#print("Getting planetary degrees and minutes for: "+sign)
			dg_mn = z[1][0:2]
			dg = dg_mn[0]
			mn = dg_mn[1]
			ns = p[0:2]+' '+str(dg)+' '+str(mn)
			test_list.append(ns)
			dgmn_str = p[0:2]+' '+str(dg)+"'"+str(mn)+'"'
			p_list.append(dgmn_str)
			#print(p_list)

	#Get a list of houses with house char, deg, mins
	for h,z in houses_dict.items():
		if z[0] == sign:
			dg_mn = z[1][0:2]
			dg = dg_mn[0]
			mn = dg_mn[1]
			#Get house symbol
			h = house_chars_dict[h]
			dgmn_str = h+' '+str(dg)+"'"+str(mn)+'"'
			h_list.append(dgmn_str)

	#Append the planet and house lists and return per zodiac sign
	p_and_h_list = p_list + h_list
	#p_and_h_list = natsorted(p_and_h_list)

	#print("##ORIGINAL LIST###")
	#print(test_list)
	#print("PYTHON SORT()")
	#print(test_list.sort())
	print("NATURAL SORT()")
	#print(natsorted(test_list))
	#print("#####")

	#print("NATURAL SORT WITH KEY")
	p_and_h_list = p_and_h_list.sort(key=natural_keys)
	#replace d,m with ' and "
	for o in p_and_h_list:
		o = o.replace()

	#print(p_and_h_list)


	return p_and_h_list
	
sign='Aries'
#navamsa_dict[sign] = navamsa_from_long(sign, planets_dict_lon_only)
#navamsa_from_long(sign, planets_dict_lon_only)
#print("#######NAVAMSA DICT#######")
#print(navamsa_dict)
print(getPrintableObjects('Gemini', planets_dict, houses_dict))
