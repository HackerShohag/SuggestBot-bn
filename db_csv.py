from functions import *
import csv
import time
t = time.time()
tm = t
print('Started working')
tagdata, stubdata, data = [], [], []

def readfile():
	read_data = []
	with open('databases.csv',newline='') as file:
		cr = csv.reader(file)
		for row in cr:
			read_data.append(row)
	return read_data

print('started for tags')
for tag in tags:
	print('started for টেমপ্লেট:'+tag)
	pagelist = WhatLinksHere('টেমপ্লেট:'+tag)
	tagdata = tagdata + pagelist
	print('found :'+str(len(tagdata)))
tag = len(tagdata)
print('Found: '+str(tag))

print('\nElapsed time:'+str(time.time()-t)+'\n\nstarted for stubs. ')
t = time.time()
for stub in stubs:
	print('started for '+stub)
	stublist = inCategory(stub)
	stubdata = stubdata + stublist
	print('found :'+str(len(stubdata)))
s = len(stubdata)	

print('\nElapsed time:'+str(time.time()-t)+'\nstarted reducing duplicates')
t = time.time()
pagenames = stubdata + tagdata
pagenames = list(dict.fromkeys(pagenames))
print('\nElapsed time:'+str(time.time()-t)+'\nreduced all duplicates')

print('Expected :'+ str(s+tag) +' Found:'+str(len(pagenames)) + '\n\nStarted making data ready to write')

t = time.time()
count = 0
for page in pagenames:
	check = False
	if isMainspace(page):
		pageid, pageview, pclass, cats = pagedata(page)
		try:
			rowdata = [pageid,page,pageviews,",".join(pclass),",".join(cats)]
			data.append(rowdata)
			count += 1
			check = True
		except Exception:
			pass
	if check == True:
		print('found '+page+' mainspaced')
	else:
		print('skiping '+page+' not mainspaced')

print('\nElapsed time:'+str(time.time()-t)+'\nMade data ready to write')
t = time.time()

print('Started writing to file')
with open('databases.csv','w') as file:
	cw = csv.writer(file,delimiter=',')
	cw.writerows(data)
	
print('\nElapsed time:'+str(time.time()-t)+'\nData write complete')
print('\n\nTotal time elapsed: ' + str(time.time()-tm) + '\nTotal mainspaced page write to file:'+str(count))
