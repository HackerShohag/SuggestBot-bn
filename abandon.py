from functions import *

def wikiitem(pagename):
	try:
		site = pywikibot.Site("bn", "wikipedia")
		page = pywikibot.Page(site, pagename)
		item = pywikibot.ItemPage.fromPage(page)
		return item.id
	except pywikibot.exceptions.NoPage:
		return False

def pageviews(pagename):
	wiki_item = wikiitem(pagename)
	if wiki_item:
		sum = 0; i = 0;
		site = pywikibot.Site("wikidata", "wikidata")
		repo = site.data_repository()
		item = pywikibot.ItemPage(repo, wiki_item)
		req = api.Request(site=site, parameters={'action': 'query','titles': item,'prop': 'pageviews'})
		s = req.submit()['query']['pages'][str(item.pageid)]['pageviews']
		for value in s:
			if s[value]:
				sum = sum + int(s[value])
				sum = sum + s[value]
				i += 1
		return floor(sum/i)
	return None

def templatedata(username):
	page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),'User talk:'+username)
	match = re.search(r'{{ব্যবহারকারী:পরামর্শবট/config.*?}}',page.text.replace('\n',''))
	if match:
		list = re.findall(r'.+',match.group().replace('|','\n'))
		return list
	return []

def frequency(username):
	list = templatedata(username)
	if list:
		for i in range(0,len(list)):
			match = re.findall('frequency\s*=\s*(\d+)',list[i],flags=re.I)
		return match[0]
	return None

def shouldPost(username):
	if extracttime(username):
		y1, m1, d1 = extracttime(username)
		t = datetime.datetime.utcnow()
		y, m, d = int(t.strftime('%Y')), int(t.strftime('%m')), (int(t.strftime('%d')) + (int(t.strftime('%H')) + (int(t.strftime('%M')) /60))/24)
		freq = frequency(username)
		if freq:
			if d1 >= (d - int(freq)) and m == m1 and y == y1:
				return True
			elif m>m1:
				return True
			elif y>y1:
				return True
			else:
				return False
		else:
			return True
	return True

def extracttime(username):
	page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),'User talk:' + username)
	enum = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
	bnum = ['১','২','৩','৪','৫','৬','৭','৮','৯','০']
	months = ['জানুয়ারি','ফেব্রুয়ারি','মার্চ','এপ্রিল','মে','জুন','জুলাই','আগস্ট','সেপ্টেম্বর','অক্টোবর','নভেম্বর','ডিসেম্বর']
	dt = re.findall(r'A\. Shohag.*?(\d+:\d+, \d+ .*? \d+) \(ইউটিসি\)',page.text)
	try:
		date = dt[-1]
		for i in range(0,12):
			if i<10:
				date = re.sub(bnum[i],enum[i],date)
			date = re.sub(months[i],str(i+1),date)
		shortdate = re.findall('(\d+):(\d+), (\d+) (\d+) (\d+)',date)
		return int(shortdate[0][4]), int(shortdate[0][3]), ((int(shortdate[0][1])/60)+int(shortdate[0][0]))/24+int(shortdate[0][2])
	except Exception:
		return None

def username(name):
	name = name.replace('User:','')
	name = re.sub(r'/.*?','',name)
	return name
