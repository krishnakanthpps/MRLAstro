import swisseph as swe

swe.set_ephe_path('/usr/local/share/swisseph')

names = { swe.SURYA: 'Surya', swe.CHANDRA: 'Candra', swe.KUJA: 'Mangala',
            swe.BUDHA: 'Budha', swe.GURU: 'Guru', swe.SUKRA: 'Sukra',
            swe.SANI: 'Sani', swe.RAHU: 'Rahu', swe.URANUS: 'Uranus', swe.NEPTUNE: 'Neptune', swe.PLUTO: 'Pluto'}

signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

#get planet Sanskrit name
def get_planet_name(planet):
  return names[planet]

#return the z sign
def get_zodiac_sign(num):
	return signs[num]

#get julday
now = swe.julday(2019,1,29)

#get planet pos
def get_planet_pos(planet):
	p_deg = (swe.calc_ut(now, planet, flag = swe.FLG_SWIEPH)[0]) % 30
	return p_deg

##TESTS##
#iterate and print all planets and their positions
def print_all_pos():
	print ("\nPrinting planetary positions for 01-29-2019\n")
	for p in names.keys():
		p_pos = (swe.calc_ut(now, p, flag = swe.FLG_SWIEPH)[0]) % 30
		p_pos_z = int((swe.calc_ut(now, p, flag = swe.FLG_SWIEPH)[0]) / 30)
		print " "+names[p]+":"+str(p_pos)+", Sign:"+str(signs[p_pos_z])

if __name__ == "__main__":
	print_all_pos()

