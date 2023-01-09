import sqlite3


class Connect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('LIBRARY.db')
        self.cursor = self.sqlite_connection.cursor()

    def add_student(self, numer_grade_book, fullname, squad, course):
        value_line = f"{numer_grade_book}, '{fullname}', '{squad}', {course}"
        self.make_request("students", "numer_grade_book, fullname, squad, course", value_line)

    def add_book(self, after, title, type_book):
        #  self.cursor.execute(f"SELECT EXISTS(SELECT title FROM type_book where title = )")
        info = self.cursor.execute(f"SELECT title FROM type_book WHERE title='{type_book}'").fetchone()
        print(info)
        if info is None:
            print("if true")
            self.make_request("type_book", "title", f"'{type_book}'")
            print("make type_book")
            return False
        else:
            print("if False")
            return True
        value_line = f"{after}, '{title}', '{type_book}'"
        self.make_request("books", "title, release, type_book", value_line)


        pass
    def make_request(self, name_table, first_values, second_values):
        try:
            print(name_table)
            print(first_values)
            print(second_values)
            count = self.cursor.execute(f"""
            INSERT
            INTO
            {name_table}({first_values})
            VALUES({second_values});
            """)
            self.sqlite_connection.commit()
            print("Запись успешно вставлена", self.cursor.rowcount)
            self.cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if self.sqlite_connection:
                self.sqlite_connection.close()
                print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    a = Connect()
    a.add_book("after", "title", "type_book")