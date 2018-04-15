import requests
import urllib.request
import re
import csv
import os
import json
import shutil
import pprint
import numpy as np

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
		print(html)
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
		yourData['max'] = str(maxfind('hp', level_rare) + maxfind('atk', level_rare))
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
	with open('qurare.csv', 'rt') as qurare:
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
	raw_skDes = re.compile('<span class="basic">.+<\/span>')

	skType = re.compile('".+"')
	data = re.compile('>.+<')

	for skroll in ['atk', 'hp', 'spr']:
		result_skName = raw_skName.findall(html)
		result_skType = raw_skType.findall(html)
		result_skDes = raw_skDes.findall(html)
		with open('skill_' + skroll + '.csv', 'wt', newline='') as qurare:
			writer = csv.DictWriter(qurare, fieldnames = ['Name', 'skilltype', 'role', 'Basic', 'Bonus'])
			writer.writeheader()
			for i in range(0, len(result_skName)):
				sklass = skType.search(result_skType[i]).group()[1:-1]
				sklass = sklass.split()
				if sklass[2] == 'def':
					sklass[2] = 'hp'
				elif sklass[2] == 'heal':
					sklass[2] = 'spr'
				if sklass[2] != skroll:
				    continue
				skName = data.search(result_skName[i]).group()[1:-1]
				skDes = data.search(result_skDes[i]).group()[1:-1]
				banus = skDes.split('</span><span class="leader">')
				writer.writerow({'Name':skName, 'skilltype':sklass[0], 'role':sklass[2], 'Basic':banus[0], 'Bonus':banus[1]})



def func_aw_write():

	#def maxfind(stat, lv):
	#	if Kodex["max" + stat + str(lv)] != '-':
	#		cachestat = Kodex['max' + stat + str(lv)]
	#		return int(cachestat)
	#	else:
	#		level_rare = lv - 1
	#		return maxfind(stat, level_rare)
	
	rarity = ['N, N+, R, R+, SR, SR+, SSR, QR', 'N', 'N+', 'R', 'R+', 'SR', 'SR+', 'SSR', 'QR']
	maxLv = ['40, 45, 70, 75, 100, 105, 130, 130', 40, 45, 70, 75, 100, 105, 130, 130]
	rareColor = ['BRONZE, BRONZE, SILVER, SILVER, GOLD, GOLD, RED', '#DDBC8B', '#DDBC8B', '#B6D8F5', '#B6D8F5', '#FFE746', '#FFE746', '#E10044', '#03C0DA']
	rarefont = ['W, W, B, B, B, B, W, W', 'white', 'white', '#0A1533', '#0A1533', '#0A1533', '#0A1533', 'white', 'white']
	roleColor = {'MAIN':'BLUE, GREEN, RED', '방어':'#264BCC', '회복':'#20AD20', '공격':'#E62E2E'}
	enrole = {'MAIN':'DEF, SPR, ATK', '방어':'hp', '회복':'spr', '공격':'atk'}
	faction = ['ORI, FAN, SF, MIS', '오리엔탈', '판타지', 'SF', '미스터리']
	bind = ['+5%, +5%, +6%, +6%, +7%, +8%, +9%, +8%', 0.05, 0.05, 0.06, 0.06, 0.07, 0.08, 0.09, 0.08]
	with open('enskill.json', encoding='utf-8-sig') as ens:
		enskill = json.load(ens)['skill']

	var_str_form = ''''''
	with open('qurare.csv', 'rt') as qurare:
		Kodex = {}
		reader = csv.DictReader(qurare)
		var_str_input = input("0. img get 1. json 2.1. thumbnail moving 2.2 small image moving 3. awiki \n\n >>>")

		if var_str_input == '0123121312312312': # don't need inven data
			for row in reader:
				Kodex = dict(row)
				try:
					path = 'd:/Documents/Visual Studio 2017/Projects/Qutabase/Qutabase/Kodex/' + enrole[Kodex['role']] + '/' + enskill[Kodex['skill'][:2]] + '/' + Kodex['rarity'] + '/' + Kodex['id']
					if not os.path.exists(path):
						os.makedirs(path)
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/"
					#+ Kodex['id'] + "an.jpg", path + '/' + Kodex['id'] + "an.jpg")
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/"
					#+ Kodex['id'] + "bn.jpg", path + '/' + Kodex['id'] + "bn.jpg")
					#urllib.request.urlretrieve("http://static.inven.co.kr/image_2011/site_image/qurare/cardimage/"
					#+ Kodex['id'] + "cn.jpg", path + '/' + Kodex['id'] + "cn.jpg")
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
				maxhp_bind[0] = int(Kodex['maxhp0'])
				maxatk_bind[0] = int(Kodex['maxatk0'])
				maxspr_bind[0] = int((maxhp_bind[0] + maxatk_bind[0]) / 2)
				for x in range(1, 7):
					maxhp_bind.append(round(maxhp_bind[0] * (1 + x * bind[int(Kodex['rarity'])])))
					maxatk_bind.append(round(maxatk_bind[0] * (1 + x * bind[int(Kodex['rarity'])])))
					maxspr_bind.append(int(maxspr_bind[0] * (1 + x * bind[int(Kodex['rarity'])])))
				dic_kodex[Kodex['name']] = {}
				data = dic_kodex[Kodex['name']]
				data['id'] = Kodex['id']
				data['rarity'] = rarity[int(Kodex['rarity'])]
				data['lv'] = maxLv[int(Kodex['rarity'])]
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
				data['hp0'] = int(Kodex['hp0'])
				data['hpLv'] = (maxhp_bind[0] - data['hp0']) / (data['lv'] - 1)
				data['atk0'] = int(Kodex['atk0'])
				data['atkLv'] = (maxatk_bind[0] - data['atk0']) / (data['lv'] - 1)
				data['spr0'] = round((int(Kodex['hp0']) + int(Kodex['atk0'])) / 2)
				data['HP'] = maxhp_bind
				data['ATK'] = maxatk_bind
				data['SPR'] = maxspr_bind
				data['engname'] = Kodex['engname']
				data['engskill'] = Kodex['engskill']
			with open('qurare.json', 'w', encoding="utf-8") as Jurare:
				json.dump(dic_kodex, Jurare, ensure_ascii=False, indent="\t")



		elif var_str_input == '2.1':
			thumb_raw_path = 'd:\\Documents\\MOMO PLAYER\\Misc\\files\\files\\Documents\\assetbundles\\Android\\CardNew\\Thumb\\Thumb\\raw\\'
			thumb_small_path = 'd:\\Documents\\MOMO PLAYER\\Misc\\files\\files\\Documents\\assetbundles\\Android\\CardNew\\Thumb\\Thumb\\small\\'
			dest_path = 'd:\\Documents\\Visual Studio 2017\\Projects\\Qutabase\\Qutabase\\Kodex\\'
			list_thumb = os.listdir(thumb_raw_path)
			for row in reader:
				Kodex = dict(row)
				for cache in list_thumb:
					if cache[:-6] == Kodex['id']:
						if not os.path.exists(dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']):
							os.makedirs(dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id'])
						if not os.path.isfile(dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']+'/raw.png') or not os.path.isfile(dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']+'/small.png'):
							shutil.copy(thumb_raw_path+cache, dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']+'/raw.png')
							shutil.copy(thumb_small_path+cache, dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']+'/small.png')
							print(cache+" Done")



		elif var_str_input == '2.2':
			thumb_path = 'd:\\Documents\\MOMO PLAYER\\Misc\\files\\files\\Documents\\assetbundles\\Android\\CardNew\\Small\\Small\\'
			dest_path = 'd:\\Documents\\Visual Studio 2017\\Projects\\Qutabase\\Qutabase\\Kodex\\'
			list_thumb = os.listdir(thumb_path)
			for row in reader:
				Kodex = dict(row)
				for cache in list_thumb:
					if cache[:-6] == Kodex['id']:
						os.renames(thumb_path+cache, dest_path+enrole[Kodex['role']]+'/'+enskill[Kodex['skill'][:2]]+'/'+Kodex['rarity']+'/'+Kodex['id']+'/'+cache[:-4]+'.jpg')
						print(cache+" Done")



#		elif var_str_input == '3123132233': # We don't use Awiki
#			for row in reader:
#				maxhp_bind = ['']
#				maxatk_bind = ['']
#				maxspr_bind = ['']
#				Kodex = dict(row)
#				maxhp_bind[0] = maxfind('hp', level_rare)
#				maxatk_bind[0] = maxfind('atk', level_rare)
#				maxspr_bind[0] = int((maxhp_bind[0] + maxatk_bind[0]) / 2)
#				for x in range(1, 6):
#					maxhp_bind.append(str(round(maxhp_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
#					maxatk_bind.append(str(round(maxatk_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))
#					maxspr_bind.append(str(int(maxspr_bind[0] * (1 + x * bind[int(Kodex['rarity'])]))))

#				path = 'd:/Documents/Visual Studio 2017/Projects/Qutabase/Qutabase/Kodex/' + role[int(Kodex['role'])] + '/' + enskill[Kodex['skill'][:2]] + '/' + Kodex['rarity']
#				if not os.path.exists(path):
#					os.makedirs(path)
#				with open(path + '/' + Kodex['id'] + ' - ' + Kodex['name'] + '.txt', 'w') as Adex:
#					var_str_form = """==== """ + Kodex['name'] + """ ====
#||<:><table bgcolor=#e3e4ee><table align=center><bgcolor=""" + rareColor[int(Kodex['rarity'])] + """>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:28px; color: """ + rarefont[int(Kodex['rarity'])] + """;">
#""" + rarity[int(Kodex['rarity'])] + """
#</span>}}}
#||||||||||||||<:><bgcolor=""" + rareColor[int(Kodex['rarity'])] + """>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:28px; color: """ + rarefont[int(Kodex['rarity'])] + """;">
#""" + Kodex['name'] + """
#</span>}}}
#||<:><bgcolor=#FFEB3B>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: #273869;">
#COST<br>""" + Kodex['cost'] + """
#</span>}}}
#||
#||||||<|2><:><bgcolor=""" + roleColor[int(Kodex['role'])] + """>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:40px; color: white;">
#""" + Kodex['skill'] + """
#</span>}}}
#||<:>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#역할
#</span>}}}
#||||{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#""" + role[int(Kodex['role'])] + """
#</span>}}}
#||<:>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#속성
#</span>}}}
#||||{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#""" + skilltype[int(Kodex['skilltype'])] + """
#</span>}}}
#||
#||<:>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#장르
#</span>}}}
#||||{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#""" + faction[int(Kodex['faction'])] + """
#</span>}}}
#||<:>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#그림
#</span>}}}
#||||{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#""" + Kodex['illustrator'] + """
#</span>}}}
#||
#||||||<:><bgcolor=#FFEB3B>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#NORMAL
#</span>}}}
#||||||<:><bgcolor=#FFEB3B>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#MAX
#</span>}}}
#||||||<:><bgcolor=#FFEB3B>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: #0A1533;">
#MAX+
#</span>}}}
#||
#||||||[[파일:""" + Kodex['id'] + """an.jpg|width=250]]||||||[[파일:""" + Kodex['id'] + """bn.jpg|width=250]]||||||[[파일:""" + Kodex['id'] + """cn.jpg|width=250]]
#||
#||||<:><bgcolor=#5A688A>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:21px; color: white;">
#스탯
#</span>}}}
#||<:><bgcolor=#5A688A>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#Lv.1
#</span>}}}
#||<:><bgcolor=#5A688A>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#MAX
#</span>}}}
#||<:><bgcolor=#00B4FF>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#1결속
#</span>}}}
#||<:><bgcolor=#00B4FF>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#2결속
#</span>}}}
#||<:><bgcolor=#00B4FF>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#3결속
#</span>}}}
#||<:><bgcolor=#00B4FF>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#4결속
#</span>}}}
#||<:><bgcolor=#00B4FF>{{{#!html
#<span style="font-weight: bold;font-family: '나눔스퀘어 ', '맑은 고딕' !important; font-size:18px; color: white;">
#5결속
#</span>}}}
#||
#||||<bgcolor=#5A688A>{{{#white HP}}}||<:>""" + Kodex['hp0'] + """||<:>""" + str(maxhp_bind[0]) + """||<:>""" + maxhp_bind[1] + """||<:>""" + maxhp_bind[2] + """||<:>""" + maxhp_bind[3] + """||<:>""" + maxhp_bind[4] + """||<:>""" + maxhp_bind[5] + """||
#||||<bgcolor=#5A688A>{{{#white ATK}}}||<:>""" + Kodex['atk0'] + """||<:>""" + str(maxatk_bind[0]) + """||<:>""" + maxatk_bind[1] + """||<:>""" + maxatk_bind[2] + """||<:>""" + maxatk_bind[3] + """||<:>""" + maxatk_bind[4] + """||<:>""" + maxatk_bind[5] + """||
#||||<bgcolor=#5A688A>{{{#white SPR}}}||<:>""" + str(round((int(Kodex['hp0']) + int(Kodex['atk0'])) / 2)) + """||<:>""" + str(maxspr_bind[0]) + """||<:>""" + maxspr_bind[1] + """||<:>""" + maxspr_bind[2] + """||<:>""" + maxspr_bind[3] + """||<:>""" + maxspr_bind[4] + """||<:>""" + maxspr_bind[5] + """||

#"""
#					Adex.write(var_str_form)

def func_rewards():
    
	reward_img = {
		"인쇄 티켓":"tik_pri",
		"SP 포션":"pot_sp",
		"우정포인트":"Fp",
		"전투 부활 포션":"pot_rev",
		"3성 마도서":"kod_ran",
		"4성 마도서":"kod_ran",
		"마력석":"Cash",
		"환상석":"illusion",
		"정예 소환석":"sum_eli",
		"시즌 탐색권":"tik_skp",
		"일반 성장서":"nor_exp",
		"일반 해석서":"nor_int",
		"일반 재화서":"nor_mny",
		"레어 성장서":"rar_exp",
		"레어 해석서":"rar_int",
		"레어 재화서":"rar_mny",
		"지식의 파편":"kno_p",
		"지식의 결정":"kno_c",
		"우주의 파편":"uni_p",
		"우주의 결정":"uni_c",
		"초차원의 파편":"dim_p",
		"SR 성장서":"spr_exp",
		"프리미엄 SR손상서":"5_ran",
		"프리미엄 SR+손상서":"6_ran",
		"불확정의 상징물":"sym_nor",
		"응축된 불확정의 상징물":"sym_con",
		"손상된 금서":"5_ran",
		"한정 인쇄 SR+ 손상서":"6_ran"
		}

	var_input = input("1. inf rewards 2. event rewards\n >>> ")

	def func_rewarder(mode):
		with open('rew_'+mode+'R.csv', 'rt') as qurare:
			reader = csv.DictReader(qurare)
			with open('rew_'+mode+'.csv', 'wt', newline='') as magic:
				writer = csv.DictWriter(magic, fieldnames=['num', 'reward', 'quan', 'img'])
				writer.writeheader()
				for row in reader:
					reward = dict(row)
					reward['img'] = reward_img[reward['reward']]
					writer.writerow({'num':reward['num'], 'reward':reward['reward'], 'quan':reward['quan'], 'img':reward['img']})

		with open('rew_'+mode+'.csv', 'rt') as qurare:
			reader = csv.DictReader(qurare)
			dic_reward = {}
			for row in reader:
				reward = dict(row)
				dic_reward[reward['num']] = reward
				reward['quan'] = int(reward['quan'])
			with open('rew_'+mode+'.json', 'wt', encoding='utf-8') as Jurare:
			    json.dump(dic_reward, Jurare, ensure_ascii=False, indent="\t")

	if var_input == '1':
		func_rewarder('inf')
	elif var_input == '2':
		func_rewarder('event')

def func_skill():

	def func_skill_skill():
		with open('skill.csv', 'rt') as qurare:
			reader = csv.DictReader(qurare)
			dic_skill = {}
			for row in reader:
				skill = dict(row)
				def floater(args):
					if skill[args] != '' and skill[args] != 'lea':
						skill[args] = float(skill[args])
					else:
						pass
				floater('static1')
				floater('static2')
				floater('static3')
				floater('dynamic1')
				floater('dynamic2')
				floater('dynamic3')
				floater('Static1')
				floater('Static2')
				floater('Static3')
				floater('Dynamic1')
				floater('Dynamic2')
				floater('Dynamic3')
				dic_skill[skill['name']] = skill
			with open('skill.json', 'wt', encoding='utf-8') as Jurare:
				json.dump(dic_skill, Jurare, ensure_ascii=False, indent="\t")

	def func_skill_effect():
		with open('effect.csv', 'rt') as qurare:
			reader = csv.DictReader(qurare)
			dic_effect = {}
			for row in reader:
				effect = dict(row)
				dic_effect[effect['name']] = effect
			with open('effect.json', 'wt', encoding='utf-8') as Jurare:
			    json.dump(dic_effect, Jurare, ensure_ascii=False, indent='\t')

	var_input = input('1. skill 2. effect\n >>> ')

	if var_input == '1':
	    func_skill_skill()
	elif var_input == '2':
		func_skill_effect()



def func_lvUp():
	
	with open('qurare.json', encoding='utf-8-sig') as Jdex:
		Jdex	=	json.load(Jdex)

	rarity	=	{
					'N':1
				,	'N+':2
				,	'R':3
				,	'R+':4
				,	'SR':5
				,	'SR+':6
				,	'SSR':7
				,	'QR':8
				}
	bind	=	{
					'N':0.05
				,	'N+':0.05
				,	'R':0.06
				,	'R+':0.06
				,	'SR':0.07
				,	'SR+':0.08
				,	'SSR':0.09
				,	'QR':0.08
				}
	global lvF
	lvF		=	open('lv_inp.txt', 'r')
	resultT	=	['RESULT  TRUE', 0, 0, 0, 0, 0, 0, 0, 0]
	resultF	=	['RESULT FALSE', 0, 0, 0, 0, 0, 0, 0, 0]

	def func_lving():
		global lvF
		try:
			dex			=	Jdex[lvF.readline()[:-1]]
		except KeyError:
			print(sum(resultT[1:]), resultT)
			print(sum(resultF[1:]), resultF)
			return
		dexLv		=	int(lvF.readline())
		dexBind		=	1	+	bind[dex['rarity']]	*	int(lvF.readline())
		dexStat		=	lvF.readline().split()
		dexStat[0]	=	int(dexStat[0])
		dexStat[1]	=	int(dexStat[1])
		
		#while True:
		#	var_str_input	=	input("마도서 이름을 입력 >> ")
		#	if var_str_input == '끝':
		#		return
		#	try:
		#		dex	=	Jdex[var_str_input]
		#	except KeyError:
		#		continue
		#	break

		#while True:
		#	try:
		#		dexLv	=	int(input("현재 레벨: "))
		#	except ValueError:
		#		continue
		#	break
		#while True:
		#	try:
		#		dexBind	=	1	+	bind[dex['rarity']]	*	int(input("결속도: "))
		#	except ValueError:
		#		continue
		#	break

		#dexLvRH	=	['LEVEL RANK ON HP', 4.004, 4.004, 5.0043, 5 + 4/8/100, 6 + 5/9/100, 6 + 6/9/100, 6 + 7/9/100, 7.007]
		#dexLvRA	=	['LEVEL RANK ON ATK', 4.004, 4.004, 5.0043, 5 + 4/8/100, 6 + 5/9/100, 6 + 6/9/100, 6 + 7/9/100, 7.007]

		#resH	=	(
		#				(
		#					dexLvRH[rarity[dex['rarity']]]
		#					*	(dexLv		-	1)
		#					/	(dex['lv']	-	1)

		#					+	1
		#				)
		#				*	dex['hp0']

		#			)	*	dexBind
		#resA	=	(
		#				(
		#					dexLvRA[rarity[dex['rarity']]]
		#					*	(dexLv		-	1)
		#					/	(dex['lv']	-	1)

		#					+	1
		#				)
		#				*	dex['atk0']

		#			)	*	dexBind

		dexLvRH	=	float(
						dex['HP'][0]
						/	dex['hp0']
					)
		dexLvRA	=	float(
						dex['ATK'][0]
						/	dex['atk0']
					)

		resH	=	(
						(
							(dexLvRH	-	1)
							*	(dexLv		-	1)
							/	(dex['lv']	-	1)

							+	1
						)
						*	dex['hp0']

					)	*	dexBind
		resA	=	(
						(
							(dexLvRA	-	1)
							*	(dexLv		-	1)
							/	(dex['lv']	-	1)

							+	1
						)
						*	dex['atk0']

					)	*	dexBind

		res		=	np.array([resH, resA])
		res		=	np.rint(res)
		if list(res) == dexStat:
			resultT[rarity[dex['rarity']]]	+= 1
		else:
			resultF[rarity[dex['rarity']]]	+= 1
		func_lving()

	func_lving()
	lvF.close()



def func_qtCsv():
	
	var_input	= input("1. qt to csv | 2. csv to qt\n >>> ")
	var_fName	= input("Filename\n >>> ")
	
	def func_qtToCsv():
		with open(var_fName, encoding='utf-8-sig') as qt:
			mainQt	= json.load(qt)
		mainKey		= list(mainQt[0].keys())
		with open(var_fName[:-2] + 'csv', 'wt', encoding='utf-8-sig', newline='') as qsv:
			writer	= csv.DictWriter(qsv, fieldnames=mainKey)
			writer.writeheader()
			for row in mainQt:
				writer.writerow(row)
					

	if var_input == '1':
	    func_qtToCsv()


def func_menu():
	var_input = input("""
	QUTABASE\n
	1. get html
	2. get data\n
	3. get json/namu & move img
	4. get rewards\n
	5. get skills\n
	6. get lvl data\n
	7. qt to csv to qt\n
	(name).display\n\n >>> """)
	if var_input == '0':
		return
	elif var_input == '1':
		var_input = input("1. ALL (id). search")
		func_db_get(var_input)
	elif var_input == '3213213232121322': # We didn't need inven data
		func_db_get('1')
		func_db_data()
	elif var_input == '3':
		func_aw_write()
	elif var_input == '4':
		func_rewards()
	elif var_input == '5':
		func_skill()
	elif var_input == '6':
		func_lvUp()
	elif var_input == '7':
		func_qtCsv()
	elif var_input == '1233212313212123': # We didn't need inven data
		func_db_get('123')
		func_db_skill()
	else:
		func_db_load(var_input)

	func_menu()

if __name__ == '__main__':
	func_menu()