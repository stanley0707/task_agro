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

class Author(db.Entity):
	id = model.PrimaryKey(int, auto=True)
	first_name = model.Required(str, 40)
	last_name = model.Required(str, 40)
	books = model.Set('Book')
	model.composite_index(id, first_name, last_name)

class Book(db.Entity):
	id = model.PrimaryKey(int, auto=True)
	author = model.Required(Author)
	model.composite_index(id, author)

model.sql_debug(True)

db.generate_mapping(create_tables=True)