from functions import *
import csv
import time
import pymysql
import datetime

def update_db(cursor,count=0):
	# command to get all data from database
	command = "SELECT PageName FROM Pages;"
	cursor.execute(command)
	data = cursor.fetchall()

	# configuring pywikibot
	site = pywikibot.Site('bn','wikipedia')

	#checking if stuck in middle and overwriting from where its left
	if count:
		data = data[count:]

	# checking page and removing if doesn't exists
	for page in data:
		pageid, pageview, pclass, cats = pagedata(page[0])
		if pageid == '-1':
			delete_com = 'DELETE FROM Pages WHERE PageName="' + page[0] +'";'
			cursor.execute(delete_com)
			db.commit()
			print('Deleted page ' + page[0] + ' because of non-existance')
		elif not pclass:
			delete_com = 'DELETE FROM Pages WHERE PageName="' + page[0] +'";'
			cursor.execute(delete_com)
			db.commit()
			print('Deleted page ' + page[0] + ' because of no potential issues')
		else:
			update_com = 'UPDATE Pages SET PageID=' + str(pageid) + ', Pageviews=' + str(pageview) + ', Class="' + ', '.join(pclass) + '", Categories="' + ', '.join(cats) + '" WHERE PageName="' + page[0] + '";'
			cursor.execute(update_com)
			db.commit()
			print('Updated page ' + page[0])



		count += 1
		with open('count','w') as file:
			file.write(str(count))

	with open('count','w') as file:
		file.write('0')


def db_sql():
	t = time.time()
	tm = t
	print('Started working')
	tagdata, stubdata, data = [], [], []

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

	try:
		db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB')
	except pymysql.err.InternalError as e:
		db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo')
		db.cursor().execute('CREATE DATABASE s54497__SBB;')
		db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB')

	cursor = db.cursor()

	try:
		create_command = '''CREATE TABLE Pages (PageID int,PageName varchar(255),Pageviews int,Class varchar(255),Categories LONGTEXT,PRIMARY KEY (PageID));'''
		cursor.execute(create_command)
	except Exception as e:
		print(e)
	count = 0

	for page in pagenames:
		if isMainspace(page):
			if not cursor.execute('SELECT * FROM Pages WHERE PageName = "' + page + '"'):
				pageid, pageview, pclass, cats = pagedata(page)
				insert_com = 'INSERT INTO Pages (PageID, PageName, Pageviews, Class, Categories) VALUES (' + str(pageid) + ', "' + page + '", ' + str(pageview) + ', "' + ', '.join(pclass) + '", "' + ', '.join(cats) + '");'
				update_com = 'UPDATE Pages SET PageID=' + pageid + ', Pageviews=' + pageview + ', Class="' + ', '.join(pclass) + '", Categories="' + ', '.join(cats) + '" WHERE PageName="' + page + '";'
				try:
					cursor.execute(insert_com)
					db.commit()
					print(page + ' has been added to database')
					count += 1
				except Exception as e:
					print(e)
		else:
			print('Skipped page ' + page)



	print('\nElapsed time:'+str(time.time()-t)+'\nData write complete')
	print('\n\nTotal time elapsed: ' + str(time.time()-tm) + '\nTotal mainspaced page write to file:'+str(count))
	cursor.close()
	db.close()


if __name__ == '__main__':
	with open('count_time_for_update','r') as timefile:
		timedata = int(timefile.read())
	if (time.time() - int(timedata)) >= (24*60*60):
		with open('count_time_for_update','w') as timefile:
			timefile.write(str(int(time.time())))
		db_sql()
	else:
		print('Skipped adding to database')

        #definig database
	db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB')
	cursor = db.cursor()

	with open('count','r') as file:
		count = int(file.read())
	if count == 0:
		if (time.time() - int(timedata)) >= (24*60*60):
			print('Started updating database')
			update_db(cursor)
		else:
			print('Skipped updating database')
	else:
		print('Started updating database')
		update_db(cursor,count)
