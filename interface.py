import sqlite3


class Connect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('LIBRARY.db')
        self.cursor = self.sqlite_connection.cursor()

    def delete_student(self, numer_grade_book):
        try:
            record = self.cursor.execute(f"SELECT id_record "
                                         f"FROM records "
                                         f"WHERE numer_grade_book={numer_grade_book}").fetchall()
            for i in record:
                if i is not None:
                    return False
            self.cursor.execute(f"DELETE FROM records WHERE numer_grade_book={numer_grade_book}")
            self.cursor.execute(f"DELETE FROM students WHERE numer_grade_book={numer_grade_book}")
            print("Книга изъята")
            self.sqlite_connection.commit()
            return True
        except sqlite3.Error as error:
            print("Ошибка при удалении записи с SQLite:", error, "!!!!!!")

    def delete_record(self, numer_grade_book, id_book):
        try:
            self.cursor.execute(f"DELETE FROM records WHERE numer_grade_book={numer_grade_book} AND id_book={id_book}")
            self.sqlite_connection.commit()
            print("Запись удалена")
        except sqlite3.Error as error:
            print("Ошибка при удалении записи с SQLite:", error, "!!!!!!")

    def delete_book(self, id_books):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(f"DELETE FROM books WHERE id_books={id_books}")
            self.sqlite_connection.commit()
            print("Книга списанна")
            return "Запись успешно удалена"
        except sqlite3.Error as error:
            print("Ошибка при удалении записи с SQLite:", error, "!!!!!!")

    def get_bool_id_book(self, id_book, id_BOOK):
        return self.cursor.execute(f"SELECT id_books "
                                   f"FROM set_books "
                                   f"WHERE id_BOOK={id_book} AND id_books={id_BOOK}").fetchone()

    def get_id_book(self, title, release, type_book):
        return self.cursor.execute(f"SELECT id_books "
                                   f"FROM books "
                                   f"WHERE title='{title}' AND release={release} AND type_book='{type_book}'").fetchone()

    def get_student(self, fullname, squad, course):
        return self.cursor.execute(f"SELECT numer_grade_book "
                                   f"FROM students "
                                   f"WHERE fullname='{fullname}' AND squad='{squad}' AND course={course}").fetchone()

    def get_free_book(self, book, current_student, id_book):
        bool_con = self.cursor.execute(f"SELECT id_BOOK "
                                       f"FROM set_books "
                                       f"WHERE id_books={book} AND id_BOOK={id_book}").fetchone()
        if bool_con is not None:
            numer_grade_book = self.cursor.execute(f"SELECT numer_grade_book "
                                                   f"FROM students "
                                                   f"WHERE fullname='{current_student}'").fetchone()[0]
            result = self.cursor.execute(f"SELECT id_books "
                                         f"FROM records "
                                         f"WHERE id_books={id_book} AND  numer_grade_book={numer_grade_book}").fetchone()
            if result is not None:
                return True
            else:
                return False
        else:
            return False

    def get_record_free(self, id_book):
        if self.cursor.execute(f"SELECT numer_grade_book "
                               f"FROM records "
                               f"WHERE id_book={id_book}").fetchone() is not None:
            return False
        else:
            return True

    def get_numer_grade_book(self, fullname):
        return self.cursor.execute(f"SELECT numer_grade_book "
                                   f"FROM students "
                                   f"WHERE fullname='{fullname}'").fetchone()

    def set_book_student(self, title, release, type_book):
        return self.cursor.execute(f"SELECT id_books "
                                   f"FROM books "
                                   f"WHERE title='{title}' AND release={release} AND type_book='{type_book}'").fetchone()

    def add_student(self, numer_grade_book, fullname, squad, course):
        value_line = f"{numer_grade_book}, '{fullname}', '{squad}', {course}"
        self.make_request_insert("students", "numer_grade_book, fullname, squad, course", value_line)

    def add_record(self, numer_grade_book, id_book):
        self.make_request_insert("records", "numer_grade_book, id_book, date_receipt",
                                 f"{numer_grade_book}, {id_book}, date('now')")

    def add_itam_book(self, count, title, release):
        id_books = self.cursor.execute(f"SELECT id_books "
                                       f"FROM books "
                                       f"WHERE title='{title}' AND release={release}").fetchone()[0]
        for i in range(int(count)):
            self.make_request_insert("set_books", "id_books", f"{id_books}")

    def add_book(self, title, after, type_book, release):
        value_line = f"'{title}',{release} , '{type_book}'"
        id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
        if id_author is None:
            self.make_request_insert("authors", "name", f"'{after}'")
            id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
        id_books = self.cursor.execute(f"SELECT id_books "
                                       f"FROM books "
                                       f"WHERE title='{title}' AND release={release}").fetchone()
        if id_books is None:
            self.make_request_insert("books", "title, release, type_book", value_line)
            id_books = self.cursor.execute(f"SELECT id_books "
                                           f"FROM books "
                                           f"WHERE title='{title}' AND release={release}").fetchone()
        info = self.cursor.execute(f"""
        SELECT id_books, id_author 
        FROM books_authors 
        WHERE id_books={id_books[0]} AND id_author={id_author[0]}"""
                                   ).fetchone()
        if info is None:
            self.make_request_insert("books_authors", "id_books, id_author", f"{id_books[0]}, {id_author[0]}")

    def make_request_insert(self, name_table, first_values, second_values):
        try:
            print("\n\tДанные:")
            print("\t", name_table)
            print("\t", first_values)
            print("\t", second_values, "\n")
            self.cursor.execute(f"""
            INSERT
            INTO
            {name_table}({first_values})
            VALUES({second_values});
            """)
            self.sqlite_connection.commit()
            print("Запись успешно вставлена", self.cursor.rowcount)
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error, "!!!!!!")

    def close(self):
        if self.sqlite_connection:
            self.sqlite_connection.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    a = Connect()
    print(a.get_record_free(114452))
    a.add_itam_book(100, "Курс математического анализа. Том 2", "2019")
    a.close()
