import pytz
from functions import *

if __name__ == '__main__':
	from time import time
	db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB',charset='utf8',use_unicode=True)
	cursor = db.cursor()
	t = time()
	success, warned, mcandidates = main(cursor)
	success = success + userboxes(cursor,mcandidates)
	try:
		logSection(success, warned)
	except Exception:
		pass
	print('Elapsed time: '+ str(time()-t))
	print('run at ' + datetime.datetime.now(pytz.timezone('Asia/Dhaka')).strftime('%Y-%m-%d %H:%M:%S'))
