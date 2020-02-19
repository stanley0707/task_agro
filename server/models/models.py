from datetime import date
import pony.orm as model

db = model.Database()
# db.bind(
# 	provider='postgres',
# 	user='',
# 	password='',
# 	host='',
# 	database=''
# 	)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

# class Author(db.Entity):
# 	id = model.PrimaryKey(int, auto=True)
# 	first_name = model.Required(str, 40)
# 	last_name = model.Required(str, 40)
# 	books = model.Set('Book')
# 	model.composite_index(id, first_name, last_name)

class Book(db.Entity):
	id = model.PrimaryKey(int, auto=True)
	year = model.Required(date)
	name = model.Required(str, max_len=40, unique=True)
	description = model.Required(str, max_len=1000)
	author = model.Required(str, max_len=60)
	model.composite_index(id, name)

model.sql_debug(True)

db.generate_mapping(create_tables=True)