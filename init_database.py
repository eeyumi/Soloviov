import sqlite3
from openpyxl import load_workbook as lw
import random



xl = lw(f"datadases/Studenty.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A" ,"1" : "B" ,"2" : "C"}

try:
    for i in range(2, 102):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()
        a = sheet_ranges["A" + f"{i}"].value
        result = f"{a}" + ","
        a = sheet_ranges["B" + f"{i}"].value
        result += f"'{a}'" + ","
        a = sheet_ranges["C" + f"{i}"].value
        result += f"'{a}'" + ","
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        result += '1'
        cursor.execute(f"""
                    INSERT
                    INTO
                    students(numer_grade_book, fullname, squad, course)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        print("Запись успешно вставлена", cursor.rowcount)
        cursor.close()
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

#===============================================
xl = lw("datadases/Avtory.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A" ,"1" : "B" ,"2" : "C"}


try:
    for i in range(2, 50):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        a = sheet_ranges["A" + f"{i}"].value
        result = f"'{a}'" + ","
        a = sheet_ranges["B" + f"{i}"].value
        result += f"'{a}'"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    authors(id_author, name)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        print("Запись успешно вставлена", cursor.rowcount)
        cursor.close()
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

#===============================================
xl = lw("datadases/Knigi.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A" ,"1" : "B" ,"2" : "C"}


try:
    for i in range(2, 54):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        a = sheet_ranges["B" + f"{i}"].value
        result = f"'{a}'" + ","
        a = sheet_ranges["C" + f"{i}"].value
        result += f"'{a}'" + ","
        a = sheet_ranges["D" + f"{i}"].value
        result += f"'{a}'"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    books(title, release, type_book)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        print("Запись успешно вставлена", cursor.rowcount)
        cursor.close()
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

#===============================================

xl = lw("datadases/Sovocupnost_knig.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A", "1" : "B", "2": "C"}


try:
    for i in range(2, 4917):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        a = sheet_ranges["B" + f"{i}"].value
        result = f"{a}" + ","
        a = sheet_ranges["A" + f"{i}"].value
        result += f"{a}"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    set_books(id_BOOK, id_books)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        cursor.close()

        # print("Запись успешно вставлена", cursor.rowcount)
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

#===============================================

xl = lw("datadases/ZAPISI.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A", "1": "B", "2": "C"}


try:
    for i in range(2, 103):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        # a = sheet_ranges["A" + f"{i}"].value
        # result = f"{a}" + ","
        a = sheet_ranges["B" + f"{i}"].value
        result = f"'{a}'" + ","
        a = sheet_ranges["C" + f"{i}"].value
        result += f"'{a}'" + ","
        a = str(sheet_ranges["D" + f"{i}"].value)
        print(type(a))
        result += f"'{a}'" + ","
        a = str(sheet_ranges["E" + f"{i}"].value)
        result += f"'{a}'"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    records(numer_grade_book, id_book, date_receipt, return_date)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        cursor.close()

        print("Запись успешно вставлена", cursor.rowcount)
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")


#===============================================

xl = lw("datadases/Tip_Knigi.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A", "1": "B", "2": "C"}


try:
    for i in range(2, 18):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        # a = sheet_ranges["A" + f"{i}"].value
        # result = f"{a}" + ","
        a = sheet_ranges["B" + f"{i}"].value
        result = f"'{a}'"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    type_book(title)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        cursor.close()

        print("Запись успешно вставлена", cursor.rowcount)
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

#===============================================

xl = lw("datadases/KnigaAVTOR.xlsx")
sheet_ranges = xl['Sheet1']
col = {"0": "A", "1": "B", "2": "C"}


try:
    for i in range(2, 65):
        sqlite_connection = sqlite3.connect('LIBRARY.db')
        cursor = sqlite_connection.cursor()

        a = sheet_ranges["A" + f"{i}"].value
        result = f"{a}" + ","
        a = sheet_ranges["B" + f"{i}"].value
        result += f"'{a}'"
        # for j in range(1, 3):
        #     # sheet_ranges[get_column_num(column, i)].value)
        #
        #     result += f"{a}" + ','
        cursor.execute(f"""
                    INSERT
                    INTO
                    books_authors(id_books, id_author)
                    VALUES({result});
                    """)
        sqlite_connection.commit()
        cursor.close()

        print("Запись успешно вставлена", cursor.rowcount)
except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)

finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")