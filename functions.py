import pywikibot
import re
import requests
from bs4 import BeautifulSoup
import pywikibot
from math import floor
import datetime
import time
from random import choice as random
import pymysql
import csv
from html import unescape

def dictofpi():
	with open('tags_dup','r') as file:
		data = file.read()
	keys = re.findall(r'==(.+?)==',data)
	values = []
	try:
		for i in range(0,len(keys)):
			d = re.findall(r'=='+keys[i]+r'==(.*?)=='+keys[i+1]+'==',data,re.S)
			values.append(''.join(d))
	except IndexError:
		pass
	dictopi = {}
	for key,value in zip(keys,values):
		vlist = re.findall(r'({{.+?}})\s*\n',value)
		slist = []
		for i in vlist:
			p = re.findall(r'{{(.+?)}}',i)
			slist.append(p[0])
		dictopi.update({key:None})
		dictopi[key] = slist
	return dictopi

# Reading all the tags and categories that contain help-needed articles
with open('tags_dup','r') as tagfile:
	tags_dup = re.findall(r'(.+?)\n',tagfile.read())
with open('tags','r') as tagfile:
	tags = re.findall(r'{{(.+?)}}',tagfile.read())
with open('stubs','r') as stubfile:
	stubs = re.findall(r'(বিষয়শ্রেণী:.*?)\n',stubfile.read())

def postwarn(username,subpage=None,lastposttime=None,warncode=0):
	currenttime = datetime.datetime.utcnow().strftime('%H:%M')
	enum = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	bnum = ['১','২','৩','৪','৫','৬','৭','৮','৯','০']
	for i in range(0,10):
		currenttime = currenttime.replace(enum[i],bnum[i])
	if lastposttime:
		elapsedtime = str(int((time.time() - lastposttime)/(60*60)))
		for i in range(0,10):
			elapsedtime = elapsedtime.replace(enum[i],bnum[i])
	filename = 'warns/warning0'+str(warncode+1)
	try:
		with open(filename,'r') as file:
			warns = file.read()
			if lastposttime:
				warns = warns.replace(r'{{etime}}',str(elapsedtime))
			if subpage:
				try:
					warns = warns.replace(r'{{subpage}}','[['+subpage+'|'+re.sub('.*?:','',subpage)+']]')
				except Exception:
					pass
				try:
					warns = warns.replace(r'{{ctime}}',str(currenttime))
				except Exception:
					pass
	except Exception as e:
		print(e)
	page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),username)
	data = warns.replace('{{sign}}',suggestbotsign().replace('--',''))
	page.text = re.sub(r'{{\s*ব্যবহারকারী:পরামর্শবট/পরামর্শ.*?}}','',page.text,flags=re.DOTALL)
	page.text = page.text.__add__(data)
	try:
		page.save(u'পরামর্শবট ক্ষুদে বার্তা প্রেরণ করল ',botflag=True)
		return True
	except Expection:
		return False


def postRec(username,recmsg,note,frequency=None,update=None):
	update_and_replace = False
	page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),username)
	l = re.findall(r'==নিবন্ধগুলি আপনার পছন্দ হতে পারে, পরামর্শবটের পরামর্শ==.*?--\[\[ব্যবহারকারী:পরামর্শবট\|পরামর্শবট\]\] \(\[\[ব্যবহারকারী আলাপ:পরামর্শবট\|আলাপ\]\]\).*?\(ইউটিসি\)',page.text,re.S)
	if not frequency:
		page.text = re.sub(r'{{\s*ব্যবহারকারী:পরামর্শবট/পরামর্শ.*?}}','',page.text)

	#adding note if exists
	if note:
		finishing = "\n" + note.__add__(suggestbotsign())
		recmsg = recmsg.__add__(finishing)
	else:
		recmsg = recmsg.__add__(suggestbotsign())

	#section for update
	if update:
		if l:
			page.text = page.text.replace(l[-1],recmsg)
			update_and_replace = True
	elif not update:
		page.text = page.text.__add__(recmsg)

	#section to save page
	isSubpage = re.findall('/',username)
	if page.exists():
		if update_and_replace == True:
			page.save(u'পরামর্শবট সর্বশেষ প্রস্তাবনা হালনাগাদ করল ',botflag=True,force=True)
		else:
			page.save(u'পরামর্শবট নিবন্ধ প্রস্তাবনা প্রেরণ করল ',botflag=True,force=True)
		return True
	elif isSubpage:
		if update_and_replace == True:
			page.save(u'পরামর্শবট সর্বশেষ প্রস্তাবনা হালনাগাদ করল ',force=True,botflag=True)
		else:
			page.save(u'পরামর্শবট নিবন্ধ প্রস্তাবনা প্রেরণ করল ',force=True,botflag=True)
		return True
	return False

def templatedata(pagename):
	response = requests.get('https://bn.wikipedia.org/w/api.php',params={'action': 'query','format': 'json','titles': pagename,'prop': 'revisions','rvprop': 'content'}).json()
	if next(iter(response['query']['pages'])) == '-1':
		return None, None, None, None, None
	elif next(iter(response['query']['pages'].values()))['pageid'] == '-1':
		return None, None, None, None, None
	text = next(iter(response['query']['pages'].values()))['revisions'][0]['*']
	template = re.findall(r'{{\s*ব্যবহারকারী:পরামর্শবট/পরামর্শ(.*?)}}',text,flags=re.DOTALL)
	if template:
		template = template[-1]
		list_data = re.findall(r'(.+?)[\n]',template.replace('|','\n').__add__('\n'))
		cats = re.findall(r'(.+?)[\n]',template.replace('|','\n').__add__('\n'))
		count = 0
		for i in range(0,len(list_data)):
			frequency_list = re.findall(r'\s*frequency\s*=\s*(\d+)',list_data[i],flags=re.I)
			if frequency_list:
				cats.pop(i - count)
				frequency = int(frequency_list[0])
				count += 1
			update_list = re.findall(r'.*?(update).*?',list_data[i],flags=re.I)
			if update_list:
				cats.pop(i - count)
				update = update_list[0]
				count += 1
			details_list = re.findall(r'.*?(details).*?',list_data[i],flags=re.I) or re.findall(r'\s*detail\s*',list_data[i],flags=re.I)
			if details_list:
				cats.pop(i - count)
				details = details_list[0]
				count += 1
	else:
		cats = []
	if 'frequency' not in locals():
		frequency = None
	if 'update' not in locals():
		update = None
	if 'details' not in locals():
		details = None
	months = ['জানুয়ারি','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','আগস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর']
	dt = re.findall(r'--\[\[ব্যবহারকারী:পরামর্শবট\|পরামর্শবট\]\] \(\[\[ব্যবহারকারী আলাপ:পরামর্শবট\|আলাপ\]\]\).*?(\d+:\d+, \d+ .*? \d+) \(ইউটিসি\)',text)
	try:
		date = dt[-1]
		for i in range(0,12):
			date = re.sub(months[i],str(i+1),date)
		shortdate = re.findall('(\d+):(\d+), (\d+) (\d+) (\d+)',date)
		Min, Hour, Day, Month, Year = int(shortdate[0][1]), int(shortdate[0][0]), int(shortdate[0][2]), int(shortdate[0][3]), int(shortdate[0][4])
	except Exception as e:
		pass
	if 'Year' in locals():
		extract_time = datetime.datetime(Year, Month, Day, Hour, Min, 0).timestamp()
	else:
		extract_time = None
	return frequency, update, cats, extract_time, details

def shouldPost(frequency=None,lastposttime=None):
	if frequency:
		if lastposttime:
			if (time.time()-lastposttime) >= (frequency*24*60*60):
				return True
			else:
				return False
		else:
			return True
	elif lastposttime:
		if (time.time()-lastposttime) < 86400:
			return 'warning'
	else:
		return True


def pageviews(page):
	url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/bn.wikipedia/all-access/all-agents/'+page+'/daily/'+str(int(datetime.datetime.utcnow().strftime('%Y%m%d00'))-10000) +'/' + datetime.datetime.utcnow().strftime('%Y%m%d00')
	response = requests.get(url)
	list = re.findall(r'[\'"]views[\'"]:(\d+)',unescape(response.text))
	if list:
		sum = 0
		for i in range(0,len(list)):
			sum = sum + int(list[i])
		return floor(sum/len(list))
	return 0

def pagedata(page):
	response = requests.get('https://bn.wikipedia.org/w/api.php',params={'action': 'query','format': 'json','titles': page,'prop': 'revisions','rvprop': 'content'}).json()
	param = {'action': 'edit', 'title': None, 'undoafter': '0', 'undo': '0'}
	param['title'] = page
	res = requests.get('https://bn.wikipedia.org/w/index.php',params=param)
	if next(iter(response['query']['pages'].keys())) == '-1':
		return '-1', None, None, None
	text = next(iter(response['query']['pages'].values()))['revisions'][0]['*']

	#getting pageviews by calling pageviews function
	pageview_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/bn.wikipedia/all-access/all-agents/'+page+'/daily/'+str(int(datetime.datetime.utcnow().strftime('%Y%m%d00'))-10000) +'/' + datetime.datetime.utcnow().strftime('%Y%m%d00')
	response_for_pageview = requests.get(pageview_url)
	view_list = re.findall(r'"views":(\d+)',response_for_pageview.text)
	if view_list:
		sum = 0
		for i in range(0,len(view_list)):
			sum = sum + int(view_list[i])
		pageview = floor(sum/len(view_list))
	else:
		pageview = 0

	# page id section which is the primary key of the database
	pageid = next(iter(response['query']['pages'].values()))['pageid']

	# Predict class section which predicts the class of an article
	foundtags, foundstubs, potentualissues = [], [], []
	alltags = re.findall(r'<a.*?>টেমপ্লেট:(.+?)</a>',unescape(res.text),flags=re.I)
	for taglist in tags_dup:
		s = re.findall(r'{{(.*?)}}', taglist)
		for tag in s:
			for pagetag in alltags:
				if tag.lower() == pagetag.lower():
					foundtags.append(s[0])
	for k in range(0,1):
		list2 = re.findall(r'{{.*?অসম্পূর্ণ.*?}}|{{.*?অসমাপ্ত.*?}}|{{.*?অসম্পুর্ণ.*?}}|{{.*?Stub.*?}}|{{.*?stub.*?}}|\[\[বিষয়শ্রেণী:.*?অসম্পূর্ণ.*?\]\]|\[\[বিষয়শ্রেণী:.*?অসম্পুর্ণ.*?\]\]|\[\[Category:.*?অসম্পূর্ণ.*?\]\]',text,flags=re.I)
		if list2:
			foundstubs.append('অসম্পূর্ণ')

	dictopi = dictofpi()
	if foundstubs:
		if foundtags:
			potentualissues.append('বিশ্বকোষীয় রূপ')
		else:
			potentualissues.append('অসম্পূর্ণ')
	else:
		for pikeys in dictopi:
			for tag in dictopi[pikeys]:
				if tag in foundtags:
					potentualissues.append(pikeys)
	potentualissues = list(dict.fromkeys(potentualissues))

	# section for categories
	bncat = re.findall(r'\[\[বিষয়শ্রেণী:(.*?)[?:\|.*?]*?\]\]',text)
	encat = re.findall(r'\[\[Category:(.*?)[?:\|.*?]*?\]\]',text,flags=re.I)

	catlist = bncat + encat
	catlist = list(dict.fromkeys(catlist))

	return str(pageid), str(pageview), tuple(potentualissues), tuple(catlist)

def getRandomList(cursor,usercontribcat=None,usercat=None):
	'''A function which reads all databases and returns a list of 30 textnames randomly '''
	#section of random chosign function from database
	def nextfunction(read_data):
		wikify, unencyclopedic, merge, stub, link, expand, translate, addsource, update, cleanup = [], [], [], [], [], [], [], [], [], []
		for page in read_data:
			pi_list = page[3].split(",")
			if 'বিশ্বকোষীয় রূপ' in pi_list[0]:
				wikify.append(page)
			elif 'অবিশ্বকোষীয়' in pi_list[0]:
				unencyclopedic.append(page)
			elif 'একীকরণ' in pi_list[0]:
				merge.append(page)
			elif 'অসম্পুর্ণ' in pi_list[0]:
				stub.append(page)
			elif 'সংযোগ' in pi_list[0]:
				link.append(page)
			elif 'সম্প্রসারণ' in pi_list[0]:
				expand.append(page)
			elif 'অনুবাদ' in pi_list[0]:
				translate.append(page)
			elif 'উৎস যোগ' in pi_list[0]:
				addsource.append(page)
			elif 'হালনাগাদ' in pi_list[0]:
				update.append(page)
			elif 'পরিষ্করণ' in pi_list[0]:
				cleanup.append(page)
		li = []
		for i in range(0,3):
			if addsource:
				li.append(random(addsource))
		for i in range(0,3):
			if cleanup:
				li.append(random(cleanup))
		for i in range(0,3):
			if expand:
				li.append(random(expand))
		for i in range(0,3):
			if unencyclopedic:
				li.append(random(unencyclopedic))
		for i in range(0,3):
			if merge:
				li.append(random(merge))
		for i in range(0,3):
			if wikify:
				li.append(random(wikify))
		for i in range(0,3):
			if update:
				li.append(random(update))
		for i in range(0,3):
			if translate:
				li.append(random(translate))
		for i in range(0,3):
			if link:
				li.append(random(link))
		for i in range(0,3):
			if stub:
				li.append(random(stub))
		li = list(dict.fromkeys(li))
		if len(li) < 30:
			for i in range(0,(30-len(li))):
				if stub:
					li.append(random(stub))
		forward = [page for page in read_data if page not in li]
		return li, forward

	#section for function to work
	cursor.execute('SELECT * FROM Pages;')
	database = cursor.fetchall()

	if usercat:
		DB1 = []
		for cat in usercat:
			cursor.execute(r'SELECT * FROM Pages WHERE Categories LIKE "%' + str(cat) + r'%";')
			usercat_db = cursor.fetchall()
			cursor.execute(r'SELECT * FROM Pages WHERE PageName LIKE "%' + str(cat) + r'%";')
			userpage_db = cursor.fetchall()
			DB1 = DB1 + list(usercat_db) + list(userpage_db)
	if usercontribcat:
		DB2 = []
		for cat in usercontribcat:
			cursor.execute(r'SELECT * FROM Pages WHERE Categories LIKE "%' + str(cat) + r'%";')
			usercat_db = cursor.fetchall()
			cursor.execute(r'SELECT * FROM Pages WHERE PageName LIKE "%' + str(cat) + r'%";')
			userpage_db = cursor.fetchall()
			DB2 = DB2 + list(usercat_db) + list(userpage_db)
	if 'DB1' in locals():
		lis, forward1 = nextfunction(DB1)
		lis = list(dict.fromkeys(lis))
	if 'lis' in locals():
		if len(lis) < 30:
			if 'DB2' in locals():
				li2, forward2 = nextfunction(tuple(dict.fromkeys(DB2+forward1)))
				for i in range(0,(30-len(lis))):
					lis = list(lis) + [random(li2)]
				lis = list(dict.fromkeys(lis))
				if len(lis) < 30:
					for i in range(0,(30-len(lis))):
						lis = list(lis) + [random(forward2)]
					lis = list(dict.fromkeys(lis))
		if len(lis) < 30:
			li3, forward2 = nextfunction(database)
			for i in range(0,(30-len(lis))):
				lis = list(lis) + [random(li3)]
			lis = list(dict.fromkeys(lis))
			if len(lis) < 30:
				for i in range(0,(30-len(lis))):
					lis = list(lis) + [random(forward2)]
			lis = list(dict.fromkeys(lis))
			note = '\n<small>বি: দ্র: পরামর্শবট আপনার অবদান ইতিহাস থেকে বাছাইকৃত বিষয়বস্তু অথবা কাঙ্ক্ষিত বিষয়বস্তু অনুযায়ী সম্ভাব্য সকল নিবন্ধ তথ্যশালায় না থাকায়, হয়তো কিছু নিবন্ধ এলোমেলোভাবে বেছে নিয়েছে।</small>  '
	elif 'lis' not in locals():
		lis, forward2 = nextfunction(database)
		note = '\n<small>বি: দ্র: সম্ভবত আপনার অবদান ইতিহাস থেকে বাছাইকৃত বিষয়বস্তু এবং কাঙ্ক্ষিত বিষয়বস্তু অনুযায়ী সম্ভাব্য সকল নিবন্ধ তথ্যশালায় না থাকায়, পরামর্শবট নিবন্ধগুলোকে এলোমেলোভাবে বেছে নিয়েছে।</small>  '
	lis = list(dict.fromkeys(lis))
	if len(lis) < 30:
		note = '\n<small>বি: দ্র: তথ্যশালায় যথেষ্ট নিবন্ধ না থাকায়, হয়তো পরামর্শবট আপনাকে পর্যাপ্ত সংখ্যক নিন্বধ প্রস্তাবনা দিতে পারে নি।</small> '

	#checking in note exists assinging blank value
	if 'note' not in locals():
		note = None

	return lis, note

def recMsg(pagenames,details=None):
	table_header = '{| class="wikitable sortable" border="1" style="text-align: center;"\n|-\n! scope="col" | পরিদর্শন/দিন\n! scope="col" | শিরোনাম\n! scope="col" | সম্ভাব্য সমস্যা\n'
	table_footer = '\n|}\n\'\'মন্তব্য:\'\' লক্ষ্য রাখবেন যে টেবিলটি সবগুলো কলাম অনুযায়ী সাজানো যায়। পরামর্শবট আপনার সম্পাদিত নিবন্ধের সমতুল্য কিছু কীওয়ার্ডের উপর ভিত্তি করে বিভিন্ন উপায়ে নিবন্ধ নির্বাচন করে। এটি কেবল সেইসব নিবন্ধগুলি বাছাই করে যেগুলো অন্যান্য উইকিপিডিয়ানরা কাজের প্রয়োজন হিসাবে চিহ্নিত করে থাকে। আপনার অবদান উইকিপিডিয়াকে আরও উন্নত করে তুলবে — সহায়তার জন্য ধন্যবাদ। \n\nপরামর্শবটের কোন সম্যসা (বাগ রিপোর্ট) অথবা পরামর্শবট সম্পর্কে আপনার যেকোন মতামত বা একে কিভাবে আরও উন্নত করা যায় সে সম্পর্কিত যে কোন পরামর্শ [[ব্যবহারকারী আলাপ:পরামর্শবট|পরামর্শবটের আলাপ পাতায়]] জানাতে পারেন। পরামর্শবট ব্যবহারের জন্য [[ব্যবহারকারী:ShohagS|সোহাগ]] ([[ব্যবহারকারী আলাপ:ShohagS|আলাপ]])-এর পক্ষ থেকে আপনাকে ধন্যবাদ, পরামর্শবটের তত্ত্বাবধায়ক। '
	pagedata = '\n==নিবন্ধগুলি আপনার পছন্দ হতে পারে, পরামর্শবটের পরামর্শ==\n[[ব্যবহারকারী:পরামর্শবট|পরামর্শবট]] আপনার সম্পাদনার জন্য এই নিবন্ধগুলি বাছাই করেছে। আশা করছি আপনার পছন্দ হবে। শুভ সম্পাদনা!\n'+ table_header

	for pagename in pagenames:
		if details:
			if r'বিশ্বকোষীয় রূপ' in pagename[3]:
				lp = pagename[3].split(",")
				try:
					lp.remove('অবিশ্বকোষীয়')
				except ValueError:
					pass
				pis = ', '.join(lp)
			else:
				pis = pagename[3]
		else:
			lp = pagename[3].split(",")
			pis = lp[0]
		pagedata = pagedata.__add__('\n|- style="text-align: center; height: 30px;"\n| style="text-align: right;" | {{formatnum:'+ str(pagename[2]) +'}}\n| style="text-align: left;" | [['+ str(pagename[1]) +']] <small>([[আলাপ:'+ str(pagename[1]) +'|আলাপ]])</small>\n| ' + str(pis))
	pagedata = pagedata.__add__(table_footer)
	return pagedata

def inCategory(categoryname):
	http = re.findall(r'https://',categoryname)
	if http:
		url = categoryname
	else:
		url = 'https://bn.wikipedia.org/wiki/' + categoryname
	response = requests.get(url)
	l = BeautifulSoup(unescape(response.text), "html.parser").find_all("div",{"id": "mw-pages"})
	pages = re.findall('<li><a.*?>(.*?)</a></li>', l.__str__())
	next = [i.get("href") for i in BeautifulSoup(unescape(response.text), "html.parser").find_all("a") if i.text == "পরবর্তী পাতা"]
	if next:
		pages = pages + inCategory('https://bn.wikipedia.org/'+next[0])
	return pages

def isMainspace(pagename):
	unlist = re.findall(r'উইকিপিডিয়া:.*?',pagename) or re.findall(r'টেমপ্লেট:.*?',pagename) or re.findall(r'ব্যবহারকারী:.*?',pagename) or re.findall(r'উইকিপিডিয়া আলাপ:.*?',pagename) or re.findall(r'টেমপ্লেট আলোচনা:.*?',pagename) or re.findall(r'ব্যবহারকারী আলাপ:.*?',pagename) or re.findall(r'আলাপ:.*?',pagename) or re.findall(r'সাহায্য:.*?',pagename) or re.findall(r'বিষয়শ্রেণী:.*?',pagename)
	if unlist:
		return False
	return True

def username(name):
	name = re.sub(r'.*?:','',name)
	name = re.sub(r'/.*','',name)
	return name

def suggestbotsign():
	sign = ' --~~~~ '
	return sign


def WhatLinksHere(pagename):
	#A function returns a list of all items from what links here as transcluded
	http = re.findall(r'https://',pagename)
	if http:
		url = pagename
	else:
		url = 'https://bn.wikipedia.org/w/index.php?title=Special:WhatLinksHere/'+ pagename + '&hidelinks=1&limit=5000'
	response = requests.get(url)
	list = re.findall(r'<li><a.*?>(.*?)?</a> \(অন্তর্ভুক্তি\).*?</li>',unescape(response.text))
	next = [i.get("href") for i in BeautifulSoup(unescape(response.text), "html.parser").find_all("a") if i.text == "পরবর্তী ৫,০০০টি"]
	if next:
		next_link = 'https://bn.wikipedia.org' + next[0]
		list = list + WhatLinksHere(next_link)
	return list

def catFromContrib(username):
	url = r'https://bn.wikipedia.org/w/index.php?title=%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%87%E0%A6%B7:%E0%A6%85%E0%A6%AC%E0%A6%A6%E0%A6%BE%E0%A6%A8/'+username+'&offset=&limit=500'
	response = requests.get(url)
	div = BeautifulSoup(unescape(response.text), "html.parser").find_all("ul",{"class": "mw-contributions-list"})
	pagenamelist = re.findall(r'<a.*?class="mw-contributions-title".*?>(.*?)</a>',div.__str__())
	pagenamelist = [page for page in pagenamelist if isMainspace(page)]
	pagenamelist = list(dict.fromkeys(pagenamelist))
	catlist = []

	for page in pagenamelist:
		response = requests.get('https://bn.wikipedia.org/w/api.php',params={'action': 'query','format': 'json','titles': page,'prop': 'revisions','rvprop': 'content'}).json()
		data = next(iter(response['query']['pages'].values()))['revisions'][0]['*']
		l = re.findall(r'\[\[বিষয়শ্রেণী:(.*?)\]\]',data)
		catlist = catlist + l
	catlist = list(dict.fromkeys(catlist))
	return catlist

def main(cursor):
	candidates = WhatLinksHere('ব্যবহারকারী:পরামর্শবট/পরামর্শ')
	success, warned = [], []
	for candidate in candidates:
		frequency, update, usercat, lastposttime, details = templatedata(candidate)
		if shouldPost(frequency,lastposttime) == True:
			usercontribcat = catFromContrib(username(candidate))
			pagenames, note = getRandomList(cursor,usercontribcat,usercat)
			rec = recMsg(pagenames,details=details)
			posted = postRec(candidate,rec,note,frequency=frequency,update=update)
			if posted:
				print('Sent message to ' + username(candidate))
				isSubpage = re.findall('/',candidate)
				if isSubpage:
					postwarn('User talk:'+username(candidate),subpage=candidate,warncode=1)
			success.append(candidate)
		elif shouldPost(frequency,lastposttime) == 'warning':
			warncheck = postwarn(candidate,lastposttime=lastposttime,warncode=0)
			if warncheck:
				print('Warned ' + username(candidate) + ' because of less than 24hrs for template')
				warned.append(candidate)
		else:
			print('Skipped ' + username(candidate) + ' because of being ' + str((time.time()-lastposttime)/(24*60*60)) + ' days for template')
	candidates = [username(candidate) for candidate in candidates]
	return success, warned, candidates
def userboxes(cursor, mcandidates):
	candidates = WhatLinksHere('ব্যবহারকারী:পরামর্শবট/ব্যবহারকারী বাক্স')
	candidates = [candidate for candidate in candidates if username(candidate) not in mcandidates]
	success = []
	for candidate in candidates:
		candidate = candidate.replace('ব্যবহারকারী:','ব্যবহারকারী আলাপ:')
		frequency, update, usercat, lastposttime, details = templatedata(candidate)
		if shouldPost(frequency,lastposttime,) == True:
			usercontribcat = catFromContrib(username(candidate))
			pagenames, note = getRandomList(cursor,usercontribcat,usercat)
			rec = recMsg(pagenames,details=None)
			posted = postRec(candidate,rec,note,frequency=frequency,update=update)
			if posted:
				print('Sent message to ' + username(candidate))
				isSubpage = re.findall('/',candidate)
				if isSubpage:
					postwarn('User talk:'+username(candidate),subpage=candidate,warncode=1)
			success.append(candidate)
		elif shouldPost(frequency,lastposttime) == 'warning':
			#postwarn(candidate,warncode=0)
			print('Skipped ' + username(candidate) + ' because of less than 24hrs for userbox')
		else:
			print('Skipped ' + username(candidate) + ' because of being ' + str((time.time()-lastposttime)/(24*60*60)) + ' days for userbox')
	return success
def logSection(success, warned):
	section_title = datetime.datetime.utcnow().strftime('%d %B %Y, %A  %H:%M')
	log_page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),'ব্যবহারকারী:পরামর্শবট/লগ')
	enum = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	bnum = ['১','২','৩','৪','৫','৬','৭','৮','৯','০']
	emonths = ['January','February','March','April','May','June','July','August','September','October','November','December']
	bmonths = ['জানুয়ারি','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','আগস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর']
	eweekday = ['Saturday', 'Sunday', 'Monday', 'Tuesday','Wednesday','Thursday','Friday']
	bweekday = ['শনিবার', 'রবিবার', 'সোমবার', 'মঙ্গলবার','বুধবার','বৃহস্পতিবার','শুক্রবার']
	for i in range(0,12):
		if i<7:
			section_title = section_title.replace(eweekday[i],bweekday[i])
		if i<10:
			section_title = section_title.replace(enum[i],bnum[i])
		section_title = section_title.replace(emonths[i],bmonths[i])
	logged = False

	if success:
		log_page.text = log_page.text.__add__('\n==' + section_title + '==\n\n')
		check = log_page.text
		for cand in success:
			log_page.text = log_page.text.__add__('# [[ব্যবহারকারী:' + username(cand) + '|' + username(cand) + ']]' + '-কে অনুরোধের ভিত্তিতে বার্তা প্রেরণ সফল। ')
		if check != log_page.text:
			logged = True
		if warned:
			for cand in warned:
				log_page.text = log_page.text.__add__('# [[ব্যবহারকারী:' + username(cand) + '|' + username(cand) + ']]' + '-কে অসময়ে অনুরোধের কারণে সতর্কবার্তা প্রেরণ করা হয়েছে। ')
	else:
		log_page.text = log_page.text.__add__('\n==' + section_title + '==\n\n')
		check = log_page.text
		if warned:
			for cand in warned:
				log_page.text = log_page.text.__add__(' [[ব্যবহারকারী:' + username(cand) + '|' + username(cand) + ']]' + '-কে অসময়ে অনুরোধের কারণে সতর্ক করা হয়েছে ')
		if check != log_page.text:
			logged = True
	if logged:
		log_page.save(u'প্রেরিত বার্তার ডেটা লগিং')
		print('Logged data have been saved!')
	else:
		print('Didn\'t log because of no message was sent!')


if __name__ == '__main__':
	db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB',charset='utf8',use_unicode=True)
	cursor = db.cursor()
	success, warned, mcandidates = main(cursor)
	success = success + userboxes(cursor,mcandidates)
	try:
		logSection(success, warned)
	except Exception:
		pass
