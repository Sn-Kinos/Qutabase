
import csv
import os

from browser import document

rarity = ['N, N+, R, R+, SR, SR+, SSR, QR', 'N', 'N+', 'R', 'R+', 'SR', 'SR+', 'SSR', 'QR']
rareColor = ['BRONZE, BRONZE, SILVER, SILVER, GOLD, GOLD, RED', '#DDBC8B', '#DDBC8B', '#B6D8F5', '#B6D8F5', '#FFE746', '#FFE746', '#E10044', '#03C0DA']
rarefont = ['W, W, B, B, B, B, W, W', 'white', 'white', '#0A1533', '#0A1533', '#0A1533', '#0A1533', 'white', 'white']
color = ['BLUE, GREEN, RED', 'blue', 'green', 'red']
role = ['DEF, SPR, ATK', '방어', '회복', '공격']
skilltype = ['ACT, PAS', '액티브', '패시브']
faction = ['ORI, FAN, SF, MIS', '오리엔탈', '판타지', 'SF', '미스터리']
bind = ['+5%, +5%, +6%, +6%, +7%, +8%, +9%, +8%', 0.05, 0.05, 0.06, 0.06, 0.07, 0.08, 0.09, 0.08]

def func_db_load(name):
	with open('qurare.csv', 'rt') as qurare:
		cache = {}
		reader = csv.DictReader(qurare)
		for row in reader:
			cache = dict(row)
			if name == cache['name']:
				document["kodex_name"] = cache['name']
				document["kodex_rarity"] = rarity[int(cache['rarity'])]
				break;
