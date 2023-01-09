import sqlite3


class Connect:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('LIBRARY.db')
        self.cursor = self.sqlite_connection.cursor()

    def add_student(self, numer_grade_book, fullname, squad, course):
        value_line = f"{numer_grade_book}, '{fullname}', '{squad}', {course}"
        self.make_request_to_add_student()
        return "student", "numer_grade_book, fullname, squad, course", value_line

    def make_request_to_add_student(self, numer_grade_book, fullname, squad, course):
        try:
            count = self.cursor.execute(f"""
            INSERT
            INTO
            students(numer_grade_book, fullname, squad, course)
            VALUES({numer_grade_book}, '{fullname}', '{squad}', {course});
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
    a.make_request_to_add_student(122233, "дж ыв ыфф", "ЦТ", 3)
    a = Connect()
    a.make_request_to_add_student(122243, "дшж ызшв ыффыф", "ЦТ", 3)
    a = Connect()
    a.make_request_to_add_student(122253, "дж ыв ыфф", "ЦТ", 3)
    a = Connect()
    a.make_request_to_add_student(122263, "дшж ызш ыффыф", "ЦТ", 4)
    a = Connect()
    a.make_request_to_add_student(122453, "дшж ызш ыффф", "ВТ", 4)
    a = Connect()
    a.make_request_to_add_student(120023, "дшж ыззз ыффф", "ВТ", 1)