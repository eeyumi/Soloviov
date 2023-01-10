import sqlite3


class Connect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('LIBRARY.db')
        self.cursor = self.sqlite_connection.cursor()

    def delete_student(self, numer_grade_book):
        try:
            record = self.cursor.execute(f"SELECT id_record, return_date "
                                f"FROM records "
                                f"WHERE numer_grade_book={numer_grade_book}").fetchall()
            print(record, "this record")
            if len(record):
                for i in record:
                    if i[1] is None:
                        return "У студента на руках есть книги!\nДля уделаения студента их быть не должно!!!"
            if record is not None:
                for i in record:
                    print(record[1])
                    self.cursor.execute(f"DELETE FROM records WHERE numer_grade_book={numer_grade_book}")
                    print("Книга изъята")
            self.cursor.execute(f"DELETE FROM students WHERE numer_grade_book={numer_grade_book}")
            self.sqlite_connection.commit()
            return"Запись успешно удалена"
        except sqlite3.Error as error:
            print("Ошибка при удалении записи с SQLite:", error, "!!!!!!")

    def delete_book(self, id_books):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(f"DELETE FROM books WHERE id_books={id_books}")
            self.sqlite_connection.commit()
            print("Книга списанна")
            return"Запись успешно удалена"
        except sqlite3.Error as error:
            print("Ошибка при удалении записи с SQLite:", error, "!!!!!!")


    def get_student(self, fullname, squad, course):
        return self.cursor.execute(f"SELECT numer_grade_book "
                                   f"FROM students "
                                   f"WHERE fullname='{fullname}' AND squad='{squad}' AND course={course}").fetchone()

    def set_book_student(self, title, release, type_book):
        return self.cursor.execute(f"SELECT id_books "
                                   f"FROM books "
                                   f"WHERE title='{title}' AND release={release} AND type_book='{type_book}'").fetchone()

    def add_student(self, numer_grade_book, fullname, squad, course):
        value_line = f"{numer_grade_book}, '{fullname}', '{squad}', {course}"
        self.make_request("students", "numer_grade_book, fullname, squad, course", value_line)

    def add_book(self, title, after, type_book, release):
        value_line = f"'{title}',{release} , '{type_book}'"
        id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
        if id_author is None:
            self.make_request("authors", "name", f"'{after}'")
            id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
        id_books = self.cursor.execute(f"SELECT id_books "
                                       f"FROM books "
                                       f"WHERE title='{title}' AND release={release}").fetchone()
        if id_books is None:
            self.make_request("books", "title, release, type_book", value_line)
            id_books = self.cursor.execute(f"SELECT id_books "
                                           f"FROM books "
                                           f"WHERE title='{title}' AND release={release}").fetchone()
        info = self.cursor.execute(f"""
        SELECT id_books, id_author 
        FROM books_authors 
        WHERE id_books={id_books[0]} AND id_author={id_author[0]}"""
                                   ).fetchone()
        if info is None:
            self.make_request("books_authors", "id_books, id_author", f"{id_books[0]}, {id_author[0]}")

    def make_request(self, name_table, first_values, second_values):
        try:
            print("\n\tДанные:")
            print("\t", name_table)
            print("\t", first_values)
            print("\t", second_values, "\n\n")

            self.cursor.execute(f"""
            INSERT
            INTO
            {name_table}({first_values})
            VALUES({second_values});
            """)
            self.sqlite_connection.commit()
            print("Запись успешно вставлена", self.cursor.rowcount)
            # self.cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, "!!!!!!")

    def close(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    a = Connect()
    # print(a.set_book_student("Курс математического анализа. Том 1", "2020", "Математический анализ")[0])
    print(a.delete_book(3))
    a.close()
