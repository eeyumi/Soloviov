import sqlite3

sqlite_connection = sqlite3.connect('LIBRARY.db')
cursor = sqlite_connection.cursor()
cursor.execute(
"""CREATE TABLE IF NOT EXISTS books(
id_books INTEGER PRIMARY KEY AUTOINCREMENT,
title VARCHAR(60),
--author VARCHAR(40),
release INTEGER,
type_book INTEGER,
FOREIGN KEY (type_book)  REFERENCES type_book (id_type));
"""
)
sqlite_connection.commit()

cursor.execute(
"""CREATE TABLE IF NOT EXiSTS type_book(
id_type INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT UNIQUE);
"""
)
sqlite_connection.commit()

cursor.execute(
""" CREATE TABLE IF NOT EXISTS authors(
id_author INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT);
"""
)
sqlite_connection.commit()

cursor.execute(
""" CREATE TABLE IF NOT EXISTS books_authors(
id_books INTEGER,
id_author INTEGER,
FOREIGN KEY (id_books)  REFERENCES books (id_books),
FOREIGN KEY (id_author)  REFERENCES authors (id_author));
"""
)
sqlite_connection.commit()


cursor.execute(
""" CREATE TABLE IF NOT EXISTS students(
numer_grade_book INTEGER PRIMARY KEY,
fullname VARCHAR(40),
squad VARCHAR(6),
course INTEGER);
"""
)
sqlite_connection.commit()

cursor.execute(
"""CREATE TABLE IF NOT EXISTS records(
id_record INTEGER PRIMARY KEY AUTOINCREMENT,
numer_grade_book INTEGER,
id_book INTEGER UNIQUE,
date_receipt DATE,
return_date DATE,
FOREIGN KEY (numer_grade_book)  REFERENCES students (numer_grade_book),
FOREIGN KEY (id_book)  REFERENCES set_books (id_BOOK));
"""
)
sqlite_connection.commit()

cursor.execute(
""" CREATE TABLE IF NOT EXISTS set_books(
id_BOOK INTEGER PRIMARY KEY,
id_books INTEGER,
FOREIGN KEY (id_books)  REFERENCES books (id_books));
"""
)
sqlite_connection.commit()
cursor.close()