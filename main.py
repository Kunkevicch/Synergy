import tkinter as TK
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main(TK.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Создание и работа с главным окном
    def init_main(self):
        toolbar = TK.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=TK.TOP, fill=TK.X)
        label_1 = TK.Label(self, text="Список сотрудников компании", font=(20))
        label_1.pack()

        ############################################################################################## КНОПКИ

        # ДОБАВИТЬ
        self.add_img = TK.PhotoImage(file="./img/add.png")
        btn_add = TK.Button(
            toolbar,
            bg="#d7d7d7",
            bd=2,
            text="Добавить сотрудника",
            image=self.add_img,
            command=self.open_add_window,
        )
        btn_add.pack(side=TK.LEFT)

        # РЕДАКТИРОВАТЬ
        self.upd_img = TK.PhotoImage(file="./img/update.png")
        btn_upd = TK.Button(
            toolbar,
            bg="#d7d7d7",
            bd=2,
            text="Редактировать выбранного сотрудника",
            image=self.upd_img,
            command=self.open_upd_window,
        )
        btn_upd.pack(side=TK.LEFT)

        # УДАЛИТЬ
        self.delete_img = TK.PhotoImage(file="./img/delete.png")
        btn_delete = TK.Button(
            toolbar,
            bg="#d7d7d7",
            bd=2,
            text="Удалить выбранных сотрудников",
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=TK.LEFT)

        # ПОИСК
        self.search_img = TK.PhotoImage(file="./img/search.png")
        btn_search = TK.Button(
            toolbar,
            bg="#d7d7d7",
            bd=2,
            text="Найти сотрудника",
            image=self.search_img,
            command=self.open_search_window,
        )
        btn_search.pack(side=TK.LEFT)

        # ОБНОВИТЬ
        self.refresh_img = TK.PhotoImage(file="./img/refresh.png")
        btn_refresh = TK.Button(
            toolbar,
            bg="#d7d7d7",
            bd=2,
            text="Обновить страницу",
            image=self.refresh_img,
            command=self.view_records,
        )
        btn_refresh.pack(side=TK.LEFT)
        ############################################################################################## Создание таблицы
        # Добавляем столбцы
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "full_name", "phone", "email", "salary"),
            height=45,
            show="headings",
        )

        # Параметры колонок
        self.tree.column("ID", width=45, anchor=TK.CENTER)
        self.tree.column("full_name", width=300, anchor=TK.CENTER)
        self.tree.column("phone", width=150, anchor=TK.CENTER)
        self.tree.column("email", width=150, anchor=TK.CENTER)
        self.tree.column("salary", width=150, anchor=TK.CENTER)
        # Подписи колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("full_name", text="ФИО")
        self.tree.heading("phone", text="Номер телефона")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Заработная плата")
        # Упаковка таблицы
        self.tree.pack(side=TK.LEFT)

    ############################################################################################## Методы
    # Запись в базу данных
    def add_record(self, full_name, phone, email, salary):
        self.db.add_employee(full_name, phone, email, salary)
        self.view_records()

    # Отображение данных в таблице
    def view_records(self):
        self.db.cur.execute(""" SELECT * FROM employes """)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

    def update_record(self, full_name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute(
            """ UPDATE employes SET full_name=?, phone=?, email=?, salary=? WHERE ID=? """,
            (full_name, phone, email, salary, id),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(
                """ DELETE FROM employes WHERE ID=? """, (self.tree.set(row, "#1"))
            )
            self.db.conn.commit()
            self.view_records()

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cur.execute(
            """ SELECT * FROM employes WHERE full_name LIKE ? """, (name,)
        )

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()]

    # Открытие диалогового окна добавления сотрудника
    def open_add_window(self):
        AddEmployee()

    # Открытие диалогового окна редактирования сотрудника
    def open_upd_window(self):
        UpdateEmployee()

    # Открытие окна поиска сотрудника
    def open_search_window(self):
        SearchEmployee()


##############################################################################################

# Класс добавления сотрудника
class AddEmployee(TK.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить сотрудника")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = TK.Label(self, text="ФИО")
        label_name.place(x=50, y=50)

        label_phone = TK.Label(self, text="Телефон")
        label_phone.place(x=50, y=80)

        label_email = TK.Label(self, text="E-mail")
        label_email.place(x=50, y=110)

        label_salary = TK.Label(self, text="Заработная плата")
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_add = ttk.Button(self, text="Добавить")
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind(
            "<Button-1>",
            lambda event: self.view.add_record(
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                self.entry_salary.get(),
            ),
        )


# Класс редактирования сотрудника
class UpdateEmployee(AddEmployee):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.default_data()

    def init_update(self):
        self.title("Редактировать позицию")
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text="Редактировать выделенную строку")
        self.btn_upd.bind(
            "<Button-1>",
            lambda event: self.view.update_record(
                self.entry_name.get(),
                self.entry_phone.get(),
                self.entry_email.get(),
                self.entry_salary.get(),
            ),
        )
        self.btn_upd.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_upd.place(x=180, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.view.db.cur.execute(""" SELECT * FROM employes WHERE ID=? """, (id))

        row = self.view.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Класс поиска сотрудника
class SearchEmployee(TK.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск по сотрудникам")
        self.geometry("300x100")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = TK.Label(self, text="ФИО")
        label_name.place(x=20, y=20)

        self.entry_name = TK.Entry(self)
        self.entry_name.place(x=70, y=20)

        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        # Кнопка поиска
        self.btn_search = ttk.Button(self, text="Найти сотрудника")
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind(
            "<Button-1>", lambda event: self.view.search_records(self.entry_name.get())
        )
        self.btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Класс базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("employes_db.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            """ CREATE TABLE IF NOT EXISTS employes(
                                ID INTEGER PRIMARY KEY NOT NULL,
                                full_name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary INTEGER) """
        )
        self.conn.commit()

    def add_employee(self, full_name, phone, email, salary):
        self.cur.execute(
            """ INSERT INTO employes (full_name, phone, email, salary) 
                        VALUES (?, ?, ?, ?)""",
            (full_name, phone, email, salary),
        )
        self.conn.commit()


# Задаем условие запуска программы
if __name__ == "__main__":
    root = TK.Tk()  # создаем корневой объект окна
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")  # Устанавливаем заголовок окна
    root.geometry("800x500")  # Устанавливаем размеры окна
    root.resizable(False, False)  # Запрещаем изменение размеров окна
    root.mainloop()  # Запускаем цикл обработки событий окна для взаимодействия с пользователем
