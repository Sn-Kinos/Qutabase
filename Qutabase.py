import requests
import urllib.request
import re
import csv
import os
import json

from bs4 import BeautifulSoup as bs

def func_db_get(input):

	global html
	global htmls
	#global htmlatk
	#global htmlhp
	#global htmlspr

	if input == '1':
		r = requests.get('http://qurare.inven.co.kr/dataninfo/card/#.')
		html = r.text
	elif input == '123':
		r = requests.get('http://qurare.inven.co.kr/dataninfo/skill/')
		html = r.text
	else:
		r = requests.get('http://qurare.inven.co.kr/dataninfo/card/detail.php?code=' + input)
		htmls = r.text
		soup = bs(htmls, 'html.parser')
		th_data = soup.find_all('th')
		return str(th_data[len(th_data) - 1])[4:-5]

def func_db_data():

	level_rare = 3
	rarity = ['N, N+, R, R+, SR, SR+, SSR, QR', 'N', 'N+', 'R', 'R+', 'SR', 'SR+', 'SSR', 'QR']
	rareColor = ['BRONZE, BRONZE, SILVER, SILVER, GOLD, GOLD, RED', '#DDBC8B', '#DDBC8B', '#B6D8F5', '#B6D8F5', '#FFE746', '#FFE746', '#E10044', '#03C0DA']
	rarefont = ['W, W, B, B, B, B, W, W', 'white', 'white', '#0A1533', '#0A1533', '#0A1533', '#0A1533', 'white', 'white']
	roleColor = ['BLUE, GREEN, RED', 'blue', 'green', 'red']
	role = ['DEF, SPR, ATK', '방어', '회복', '공격']
	enrole = ['DEF, SPR, ATK', 'hp', 'spr', 'atk']
	skilltype = ['ACT, PAS', '액티브', '패시브']
	faction = ['ORI, FAN, SF, MIS', '오리엔탈', '판타지', 'SF', '미스터리']

	def maxfind(stat, lv):
		if yourData["max" + stat + str(lv)] != '-':
			cachestat = yourData['max' + stat + str(lv)]
			return int(cachestat)
		else:
			level_rare = lv - 1
			return maxfind(stat, level_rare)

	dic_kodex_data = {'Developer':'Sn Kinos'}
	dic_kodex_key = []
	arr_kodex_names = []
	raw_idName = re.compile('<td class="name"><a.+>[A-Za-z0-9 \.&\-가-힣®]+<\/a>')
	raw_data = re.compile("data-value='{.+}'")

	Kodex_ID = re.compile("\d+")
	name = re.compile(">[A-Za-z0-9 \.&\-가-힣®]+<")
	data = re.compile("{.+}")

	result_idName = raw_idName.findall(html)
	result_data = raw_data.findall(html)

	for i in range(0,len(result_data)):
		yourId = Kodex_ID.search(result_idName[i]).group()
		yourName = name.search(result_idName[i]).group()[1:-1]
		yourData = eval(data.search(result_data[i]).group())
		yourData['max'] = str( maxfind('hp', level_rare) + maxfind('atk', level_rare) )
		yourData['id'] = yourId
		yourData['name'] = yourName
		yourData['role'] = role[yourData['role']]
		yourData['skilltype'] = skilltype[yourData['skilltype']]
		yourData['faction'] = faction[yourData['faction']]

		#yourData['skill'] = func_db_get(yourId)
		del yourData['lv0']
		del yourData['lv1']
		del yourData['lv2']
		del yourData['maxlv0']
		del yourData['maxlv1']
		del yourData['maxlv2']
		del yourData['maxlv3']
		del yourData['atk1']
		del yourData['atk2']
		del yourData['hp1']
		del yourData['hp2']
		dic_kodex_data[yourName] = yourData
		arr_kodex_names.append(yourName)

	dic_kodex_key = list(dic_kodex_data['루시퍼'].keys())

	with open('qurare.csv', 'w', newline='') as qurare:
		fields = list(dic_kodex_key)
		writer = csv.DictWriter(qurare, fieldnames = fields)
		writer.writeheader()
		for i in arr_kodex_names:
			writer.writerow(dic_kodex_data[i])

def func_db_load(name):
	with open('qurareasdasd.csv', 'rt') as qurare:
		cache = {}
		reader = csv.DictReader(qurare)
		for row in reader:
			cache = dict(row)
			if name == cache['name']:
				print(cache)

def func_db_skill():

	global html
	
	raw_skName = re.compile('<td class="name">.+<\/td>')
	raw_skType = re.compile('<tr class=".+">')
	raw_skDes= re.compile('<span class="basic">.+<\/span>')

	skType = re.compile('".+"')
	data = re.compile('>.+<')

	for skroll in ['atk', 'def', 'heal']:
		result_skName = raw_skName.findall(html)
		result_skType = raw_skType.findall(html)
		result_skDes = raw_skDes.findall(html)
		with open('skill_' + skroll + '.csv', 'wt', newline='') as qurare:
			writer = csv.DictWriter(qurare, fieldnames = ['Name', 'skilltype', 'role', 'Basic', 'Bonus'])
			writer.writeheader()
			for i in range(0, len(result_skName)):
				sklass = skType.search(result_skType[i]).group()[1:-1]
				sklass = sklass.split()
				if sklass[2] != skroll:
				    continue
				skName = data.search(result_skName[i]).group()[1:-1]
				skDes = data.search(result_skDes[i]).group()[1:-1]
				banus = skDes.split('</span><span class="leader">')
				writer.writerow({'Name':skName, 'skilltype':sklass[0], 'role':sklass[2], 'Basic':banus[0], 'Bonus':banus[1]})



def func_aw_write():

	def maxfind(stat, lv):
		if Kodex["max" + stat + str(lv)] != '-':
			cachestat = Kodex['max' + stat + str(lv)]
			return int(cachestat)
		else:
			level_rare = lv - 1
			return maxfind(stat, level_rare)
	
	rarity = ['N, N+, R, R+, SR, SR+, SSR, QR', 'N', 'N+', 'R', 'R+', 'SR', 'SR+', 'SSR', 'QR']
	rareColor = ['BRONZE, BRONZE, SILVER, SILVER, GOLD, GOLD, RED', '#DDBC8B', '#DDBC8B', '#B6D8F5', '#B6D8F5', '#FFE746', '#FFE746', '#E10044', '#03C0DA']
	rarefont = ['W, W, B, B, B, B, W, W', 'white', 'white', '#0A1533', '#0A1533', '#0A1533', '#0A1533', 'white', 'white']
	roleColor = {'MAIN':'BLUE, GREEN, RED', '방어':'#264BCC', '회복':'#20AD20', '공격':'#E62E2E'}
	enrole = {'MAIN':'DEF, SPR, ATK', '방어':'hp', '회복':'spr', '공격':'atk'}
	faction = ['ORI, FAN, SF, MIS', '오리엔탈', '판타지', 'SF', '미스터리']
	bind = ['+5%, +5%, +6%, +6%, +7%, +8%, +9%, +8%', 0.05, 0.05, 0.06, 0.06, 0.07, 0.08, 0.09, 0.08]
	enskill = {
		"AE":"AE36",
		"He":"HelloWorld",
		"KA":"KANGTA",
		"갈취":"Extortion",
		"강타":"Smite",
		"격노":"Rage",
		"격분":"Frenzy",
		"격앙":"Warmth",
		"격정":"Passion",
		"고냥":"EnNyance",
		"고양":"Enhance",
		"다이":"Dynamite",
		"맹폭":"Blind",
		"면역":"Immune",
		"분노":"Enrage",
		"분쇄":"Smash",
		"속공":"Swipe",
		"역공":"CounterATK",
		"역행":"Regress",
		"죽음":"Gunship",
		"진노":"Wrath",
		"차단":"Cancel",
		"타락":"Lucifer",
		"폭격":"Bombard",
		"폭쇄":"Baltar",
		"행운":"Lucky",
		"흡혈":"Drain",

		"간파":"Sidestep",
		"골절":"Crack",
		"근성":"Endurance",
		"난투":"Melee",
		"단결":"Solidarity",
		"도발":"Provoke",
		"돌진":"Charge",
		"반격":"CounterHP",
		"발뭉":"Balmung",
		"방어":"Protection",
		"불굴":"Indomitable",
		"선봉":"Valette",
		"소생":"Resurrect",
		"수호":"Guard",
		"억압":"Suppress",
		"역습":"Retaliate",
		"와장":"WA2000",
		"응원":"Support",
		"인내":"Fortitude",
		"재생":"Regenerate",
		"철벽":"Fortify",
		"회피":"Evade",

		"Me":"Mercury",
		"검은":"Wolf",
		"격려":"Encourage",
		"기도":"Prayer",
		"매직":"Hopeginger",
		"몽마":"Lilim",
		"보호":"Shield",
		"분리":"Recycle",
		"신성":"Sacred",
		"심문":"Interrogate",
		"아르":"Arcana",
		"안위":"Empower",
		"요정":"Fairy",
		"우정":"Friendship",
		"정화":"Purify",
		"조작":"Fixing",
		"징벌":"Punish",
		"참회":"Repent",
		"치료":"Cure",
		"치유":"Heal",
		"친목":"Amity",
		"평안":"Peace",
		"해제":"Dispel",
		"회개":"Contrite"

	}


	var_str_form = ''''''
	with open('qurare.csv', 'rt') as qurare:
		Kodex = {}
		reader = csv.DictReader(qurare)
		var_str_input = input("1. json 2. awiki\n\n >>>")

		if var_str_input == '0':
			for row in reader:
				Kodex = dict(row)
				try:
					path = 'd:/Documents/Visual Studio 2017/Projects/Qutabase/Qutabase/Kodex/' + enrole[Kodex['role']] + '/' + enskill[Kodex['skill'][:2]] + '/' + Kodex['rarity'] + '/' + Kodex['id']
					if not os.path.exists(path):
						os.makedirs(path)
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/" + Kodex['id'] + "an.jpg", path + '/' + Kodex['id'] + "an.jpg")
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/" + Kodex['id'] + "bn.jpg", path + '/' + Kodex['id'] + "bn.jpg")
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/" + Kodex['id'] + "cn.jpg", path + '/' + Kodex['id'] + "cn.jpg")
					urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardicon/" + Kodex['id'] + "an.jpg", path + "/small.jpg")
					print(Kodex['name'])
				except:
				    print(".",end='')

		elif var_str_input == '1':
			dic_kodex = {}
			for row in reader:
				level_rare = 3
				maxhp_bind = ['']
				maxatk_bind = ['']
				maxspr_bind = ['']
				Kodex = dict(row)
				maxhp_bind[0] = maxfind('hp', level_rare)
				maxatk_bind[0] = maxfind('atk', level_rare)
				maxspr_bind[0] = int((maxhp_bind[0] + maxatk_bind[0]) / 2)
				for x in range(1, 7):
					maxhp_bind.append(str(round(maxhp_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
					maxatk_bind.append(str(round(maxatk_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
					maxspr_bind.append(str(int(maxspr_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
				dic_kodex[Kodex['name']] = {}
				data = dic_kodex[Kodex['name']]
				data['id'] = Kodex['id']
				data['rarity'] = rarity[int(Kodex['rarity'])]
				data['role'] = Kodex['role']
				data['skilltype'] = Kodex['skilltype']
				data['faction'] = Kodex['faction']
				data['name'] = Kodex['name']
				data['rareColor'] = rareColor[int(Kodex['rarity'])]
				data['rarefont'] = rarefont[int(Kodex['rarity'])]
				data['cost'] = Kodex['cost']
				data['skill'] = Kodex['skill']
				data['enskill'] = enskill[Kodex['skill'][:2]]
				data['roleColor'] = roleColor[Kodex['role']]
				data['illustrator'] = Kodex['illustrator']
				data['hp0'] = Kodex['hp0']
				data['atk0'] = Kodex['atk0']
				data['spr0'] = str( round( (int(Kodex['hp0']) + int(Kodex['atk0'])) / 2 ) )
				data['HP'] = maxhp_bind
				data['ATK'] = maxatk_bind
				data['SPR'] = maxspr_bind
			with open('qurare.json', 'w', encoding="utf-8") as Jurare:
				json.dump(dic_kodex, Jurare, ensure_ascii=False, indent="\t")
	
		elif var_str_input == '2':
			for row in reader:
				maxhp_bind = ['']
				maxatk_bind = ['']
				maxspr_bind = ['']
				Kodex = dict(row)
				maxhp_bind[0] = maxfind('hp', level_rare)
				maxatk_bind[0] = maxfind('atk', level_rare)
				maxspr_bind[0] = int((maxhp_bind[0] + maxatk_bind[0]) / 2)
				for x in range(1, 6):
					maxhp_bind.append(str(round(maxhp_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
					maxatk_bind.append(str(round(maxatk_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
					maxspr_bind.append(str(int(maxspr_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))

				path = 'd:/Documents/Visual Studio 2017/Projects/Project QA/Project QA/Kodex/' +role[int(Kodex['role'])] + '/' + enskill[Kodex['skill'][:2]] + '/' + Kodex['rarity']
				if not os.path.exists(path):
					os.makedirs(path)
				with open(path + '/' + Kodex['id'] + ' - ' + Kodex['name'] + '.txt', 'w') as Adex:
					var_str_form = """==== """ + Kodex['name'] + """ ====
||<:><table bgcolor=#e3e4ee><table align=center><bgcolor=""" + rareColor[int(Kodex['rarity'])] + """>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:28px; color: """ + rarefont[int(Kodex['rarity'])] + """;">
""" + rarity[int(Kodex['rarity'])] + """
</span>}}}
||||||||||||||<:><bgcolor=""" + rareColor[int(Kodex['rarity'])] + """>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:28px; color: """ + rarefont[int(Kodex['rarity'])] + """;">
""" + Kodex['name'] + """
</span>}}}
||<:><bgcolor=#FFEB3B>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: #273869;">
COST<br>""" + Kodex['cost'] + """
</span>}}}
||
||||||<|2><:><bgcolor=""" + roleColor[int(Kodex['role'])] + """>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:40px; color: white;">
""" + Kodex['skill'] + """
</span>}}}
||<:>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
역할
</span>}}}
||||{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
""" + role[int(Kodex['role'])] + """
</span>}}}
||<:>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
속성
</span>}}}
||||{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
""" + skilltype[int(Kodex['skilltype'])] + """
</span>}}}
||
||<:>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
장르
</span>}}}
||||{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
""" + faction[int(Kodex['faction'])] + """
</span>}}}
||<:>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
그림
</span>}}}
||||{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
""" + Kodex['illustrator'] + """
</span>}}}
||
||||||<:><bgcolor=#FFEB3B>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
NORMAL
</span>}}}
||||||<:><bgcolor=#FFEB3B>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
MAX
</span>}}}
||||||<:><bgcolor=#FFEB3B>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
MAX+
</span>}}}
||
||||||[[파일:"""+Kodex['id']+"""an.jpg|width=250]]||||||[[파일:"""+Kodex['id']+"""bn.jpg|width=250]]||||||[[파일:"""+Kodex['id']+"""cn.jpg|width=250]]
||
||||<:><bgcolor=#5A688A>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: white;">
스탯
</span>}}}
||<:><bgcolor=#5A688A>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
Lv.1
</span>}}}
||<:><bgcolor=#5A688A>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
MAX
</span>}}}
||<:><bgcolor=#00B4FF>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
1결속
</span>}}}
||<:><bgcolor=#00B4FF>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
2결속
</span>}}}
||<:><bgcolor=#00B4FF>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
3결속
</span>}}}
||<:><bgcolor=#00B4FF>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
4결속
</span>}}}
||<:><bgcolor=#00B4FF>{{{#!html
<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
5결속
</span>}}}
||
||||<bgcolor=#5A688A>{{{#white HP}}}||<:>""" + Kodex['hp0'] + """||<:>""" + str(maxhp_bind[0]) + """||<:>""" + maxhp_bind[1] + """||<:>""" + maxhp_bind[2] + """||<:>""" + maxhp_bind[3] + """||<:>""" + maxhp_bind[4] + """||<:>""" + maxhp_bind[5] + """||
||||<bgcolor=#5A688A>{{{#white ATK}}}||<:>""" + Kodex['atk0'] + """||<:>""" + str(maxatk_bind[0]) + """||<:>""" + maxatk_bind[1] + """||<:>""" + maxatk_bind[2] + """||<:>""" + maxatk_bind[3] + """||<:>""" + maxatk_bind[4] + """||<:>""" + maxatk_bind[5] + """||
||||<bgcolor=#5A688A>{{{#white SPR}}}||<:>""" + str( round( (int(Kodex['hp0']) + int(Kodex['atk0'])) / 2 ) ) + """||<:>""" + str(maxspr_bind[0]) + """||<:>""" + maxspr_bind[1] + """||<:>""" + maxspr_bind[2] + """||<:>""" + maxspr_bind[3] + """||<:>""" + maxspr_bind[4] + """||<:>""" + maxspr_bind[5] + """||

"""
					Adex.write(var_str_form)

def func_menu():
	var_input = input("""
	1. get html\n
	2. get data\n
	3. get json/namu
	(name).display\n\n >>> """)
	if var_input == '0':
		return
	elif var_input == '1':
		var_input = input("1. ALL (id). search")
		func_db_get(var_input)
	elif var_input == '2':
		func_db_get('1')
		func_db_data()
	elif var_input == '3':
		func_aw_write()
	elif var_input == '123':
		func_db_get('123')
		func_db_skill()
	else:
		func_db_load(var_input)

	func_menu()

if __name__ == '__main__':
	func_menu()