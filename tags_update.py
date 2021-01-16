import re
import pywikibot

with open('tags','r') as tagfile:
	tags = re.findall(r'{{(.+?)}}',tagfile.read())
for tag in tags:
	page = pywikibot.Page(pywikibot.Site('bn','wikipedia'),'টেমপ্লেট:'+tag)
	if page.exists():
		if page.isRedirectPage():
			rp = page.getRedirectTarget().title()
			with open('tags_dup','r') as file:
				data = file.read()
			with open('tags','r') as file:
				data_t = file.read()
			with open('tags_dup','w') as file:
				data = data.replace('{{'+tag+'}}','{{'+rp+'}}|{{'+tag+'}}')
				file.write(data)
			with open('tags','w') as file:
				data_t = data_t.replace('{{'+tag+'}}','{{'+rp+'}}')
				file.write(data_t)
		if not page.isRedirectPage():
			url = 'https://bn.wikipedia.org/w/index.php?title=বিশেষ:সংযোগকারী_পৃষ্ঠাসমূহ/টেমপ্লেট:'+tag+'&hidetrans=1&hidelinks=1'
			response =re.get(url)
			redirs = re.findall(r'<li><a.*?>টেমপ্লেট:(.*?)?</a> \(পুনর্নির্দেশ\).*?</li>',response.text)
			with open('tags_dup','r') as file:
				data = file.read()
			match = re.search(r'{{'+tag+r'}}.*?\n',data)
			rpd = '{{'+tag+'}}|{{'+'}}|{{'.join(redirs)+'}}'
			data = data.replace(rpd,match.group())
			with open('tags_dup','w') as file:
				file.write(data)
	if not page.exists():
		with open('tags_dup','r') as file:
			data = file.read()
		data = data.replace('{{'+tag+'}}','')
		with open('tags_dup','w') as file:
			file.write(data)
		with open('tags','r') as file:
			data_t = file.read()
		data_t = data_t.replace('{{'+tag+'}}','')
		with open('tags','w') as file:
			file.write(data_t)
