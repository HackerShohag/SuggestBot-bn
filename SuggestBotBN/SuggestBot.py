from functions import *

if __name__ == '__main__':
	import sys
	from time import time
	db = pymysql.connect('tools.db.svc.eqiad.wmflabs','s54497','xVrO9dfWMwWiHPyo','s54497__SBB')
	cursor = db.cursor()
	t = time()
	main(cursor)
	userboxes(cursor)
	print('Elapsed time: '+ str(time()-t))

