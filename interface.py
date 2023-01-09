import sqlite3


class Connect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('LIBRARY.db')
        self.cursor = self.sqlite_connection.cursor()

    def add_student(self, numer_grade_book, fullname, squad, course):
        value_line = f"{numer_grade_book}, '{fullname}', '{squad}', {course}"
        self.make_request("students", "numer_grade_book, fullname, squad, course", value_line)

    def add_book(self, after, title, release, type_book):
        value_line = f"'{title}',{release} , '{type_book}'"


        # добав запись книжки
        # получает id_author из authors
        id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
        print(id_author, "id_author")
        # создает запись в authors если её нет
        if id_author is None:
            print("id_author if true")
            self.make_request("authors", "name", f"'{after}'")
            print("make authors")
            id_author = self.cursor.execute(f"SELECT id_author FROM authors WHERE name='{after}'").fetchone()
            print(id_author, "id_author")
        # ПОЛУЧАЕТ id_books из books
        id_books = self.cursor.execute(
            f"SELECT id_books FROM books WHERE title='{title}' AND release={release}").fetchone()
        print(id_books, "id_books")
        # проверяет есть ли запись в books_authors с id_author и id_books
        if id_books is None:
            print("id_books if true")
            self.make_request("books", "title, release, type_book", value_line)
            print("make authors")
            id_books = self.cursor.execute(
                f"SELECT id_books FROM books WHERE title='{title}' AND release={release}").fetchone()
        info = self.cursor.execute(f"""
        SELECT id_books, id_author 
        FROM books_authors 
        WHERE id_books={id_books[0]} AND id_author={id_author[0]}"""
                                   ).fetchone()
        print(info, "info")
        # создает запись
        if info is None:
            print("info if true")
            self.make_request("books_authors", "id_books, id_author", f"{id_books[0]}, {id_author[0]}")
            # info = self.cursor.execute(f"""
            #         SELECT id_books, id_author
            #         FROM books_authors
            #         WHERE id_books={id_books[0]} AND id_author={id_author[0]}"""
            #                            ).fetchone()
        # print(info, "info <==")
        #
        #
        # value_line = f"{after}, '{title}', '{type_book}'"
        # self.make_request("books", "title, release, type_book", value_line)

        # pass

    def make_request(self, name_table, first_values, second_values):
        try:
            print("\n\tДанные:")
            print("\t", name_table)
            print("\t", first_values)
            print("\t", second_values, "\n\n")

            count = self.cursor.execute(f"""
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
    a.add_book("aorrrr", "nassss", "2332", "type")
    a.close()
