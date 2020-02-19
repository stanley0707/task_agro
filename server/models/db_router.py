from pony.orm import *

db = Database()
# db.bind(
# 	provider='postgres',
# 	user='',
# 	password='',
# 	host='',
# 	database=''
# 	)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)