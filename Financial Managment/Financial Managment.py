import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CircleButton(tk.Canvas):
    def __init__(self, master, radius, command=None, color=None, hover_color=None):
        self.radius = radius
        self.command = command
        self.color = color
        self.hover_color = hover_color

        width = 2 * radius
        height = 2 * radius
        super().__init__(master, width=width, height=height, highlightthickness=0, bg='SystemButtonFace')

        self.button = self.create_oval(0, 0, width, height, fill=color, outline='')

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)

    def on_enter(self, event):
        self.itemconfig(self.button, fill=self.hover_color)

    def on_leave(self, event):
        self.itemconfig(self.button, fill=self.color)

    def on_click(self, event):
        if self.command:
            self.command()

class Autorization(tk.Toplevel):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.master = master
        self.main_app = main_app
        self.geometry('350x250')
        self.title('Авторизация')
        self.resizable(False, False)

        self.login_text = ttk.Label(self, text='Логин', font=('Arial', 12))
        self.login_text.pack(anchor='center', pady=10)

        self.login_entry = ttk.Entry(self)
        self.login_entry.pack(anchor='center', ipadx=50, ipady=2)

        self.password_text = ttk.Label(self, text='Пароль', font=('Arial', 12))
        self.password_text.pack(anchor='center', pady=10)

        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack(anchor='center', ipadx=50, ipady=2)

        self.sign_in = ttk.Button(self, text='Вход', command=self.sign_in)
        self.sign_in.pack(anchor='center', pady=20, ipady=2, ipadx=10)

        self.sign_up = ttk.Button(self, text='Зарегистрироваться', command=self.sign_up)
        self.sign_up.pack(anchor='center', ipady=2, ipadx=15)

        self.users_file = 'json/users.json'

    def sign_in(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
                if login in users and users[login] == password:
                    messagebox.showinfo('Вход', 'Вход выполнен успешно!')
                    self.destroy()
                    self.main_app.show_main_window(login)
                else:
                    messagebox.showerror('Вход', 'Неверное имя пользователя или пароль!')
        else:
            messagebox.showerror('Вход', 'Такого пользователя не существует!')

    def sign_up(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror('Регистрация', 'Заполните все поля!')
            return

        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                users = json.load(f)
        else:
            users = {}

        if login in users:
            messagebox.showerror('Регистрация', 'Пользователь с таким именем уже существует!')
            return

        users[login] = password

        with open(self.users_file, "w") as f:
            json.dump(users, f)

        messagebox.showinfo("Успех", "Регистрация успешна!")

class SettingsWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.title('Настройки')
        self.geometry('300x200')
        self.resizable(False, False)
        self.app = app

        ttk.Label(self, text="Тема:", font=('Arial', 12)).pack(pady=5)
        
        self.theme_var = tk.StringVar(value=self.app.current_theme)
        ttk.Radiobutton(self, text="Светлая", variable=self.theme_var, value="light").pack()
        ttk.Radiobutton(self, text="Темная", variable=self.theme_var, value="dark").pack()
        
        ttk.Button(self, text="Применить", command=self.apply_settings).pack(pady=20)

    def apply_settings(self):
        self.app.current_theme = self.theme_var.get()
        self.app.apply_theme()
        self.app.save_data()
        self.destroy()

class AddIncomeWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.title('Добавить доход')
        self.geometry('300x250')
        self.resizable(False, False)
        self.app = app

        ttk.Label(self, text="Добавить доход", font=('Arial', 14)).pack(pady=10)

        ttk.Label(self, text="Получено:").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="От кого:").pack()
        self.source_entry = ttk.Entry(self)
        self.source_entry.pack(pady=5)

        ttk.Label(self, text="Категория:").pack()
        self.category_combo = ttk.Combobox(self, values=self.app.categories["Доходы"], state="readonly")
        self.category_combo.current(0)
        self.category_combo.pack(pady=5)

        ttk.Button(self, text="Добавить", command=self.add_income).pack(pady=10)

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            source = self.source_entry.get().strip()
            
            if amount <= 0:
                messagebox.showerror('Ошибка', 'Сумма должна быть положительной')
                return
            
            if not source:
                messagebox.showerror('Ошибка', 'Укажите источник дохода')
                return
            
            transaction = {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "type": "Доход",
                "category": self.category_combo.get(),
                "amount": amount,
                "description": source
            }
            
            self.app.transactions.append(transaction)
            self.app.save_data()
            self.app.update_balance()
            self.app.update_chart()
            self.destroy()
            messagebox.showinfo('Успех', 'Доход добавлен')
            
        except ValueError:
            messagebox.showerror('Ошибка', 'Некорректная сумма')

class AddExpenseWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.title('Добавить расход')
        self.geometry('300x250')
        self.resizable(False, False)
        self.app = app

        ttk.Label(self, text="Добавить расход", font=('Arial', 14)).pack(pady=10)

        ttk.Label(self, text="Потрачено:").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(pady=5)

        ttk.Label(self, text="На что:").pack()
        self.purpose_entry = ttk.Entry(self)
        self.purpose_entry.pack(pady=5)

        ttk.Label(self, text="Категория:").pack()
        self.category_combo = ttk.Combobox(self, values=self.app.categories["Расходы"], state="readonly")
        self.category_combo.current(0)
        self.category_combo.pack(pady=5)

        ttk.Button(self, text="Добавить", command=self.add_expense).pack(pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            purpose = self.purpose_entry.get().strip()
            
            if amount <= 0:
                messagebox.showerror('Ошибка', 'Сумма должна быть положительной')
                return
            
            if not purpose:
                messagebox.showerror('Ошибка', 'Укажите, на что потрачены деньги')
                return
            
            transaction = {
                "date": datetime.now().strftime("%d.%m.%Y"),
                "type": "Расход",
                "category": self.category_combo.get(),
                "amount": amount,
                "description": purpose
            }
            
            self.app.transactions.append(transaction)
            self.app.save_data()
            self.app.update_balance()
            self.app.update_chart()
            self.destroy()
            messagebox.showinfo('Успех', 'Расход добавлен')
            
        except ValueError:
            messagebox.showerror('Ошибка', 'Некорректная сумма')

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        # Инициализация данных
        self.transactions = []
        self.categories = {
            "Доходы": ["Зарплата", "Премия", "Подарок", "Инвестиции", "Другое"],
            "Расходы": ["Еда", "Транспорт", "Жилье", "Развлечения", "Здоровье", "Одежда", "Техника", "Другое"]
        }
        self.current_theme = "light"
        self.logged_in_user = ""
        
        # Загрузка данных
        self.load_data()
        
        # Окно авторизации
        self.auth_window = Autorization(self.root, self)
    
    def show_main_window(self, username):
        self.logged_in_user = username
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Копеечка")
        self.main_window.geometry("600x600")
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Верхняя панель с кнопками
        top_panel = ttk.Frame(self.main_window)
        top_panel.pack(fill=tk.X, padx=10, pady=10)
        
        # Круглые кнопки
        self.theme_btn = CircleButton(top_panel, radius=15, 
                                    command=self.toggle_theme,
                                    color='LightSkyBlue3', 
                                    hover_color='LightSkyBlue2')
        self.theme_btn.pack(side=tk.LEFT, padx=5)
        
        self.settings_btn = CircleButton(top_panel, radius=15, 
                                       command=self.show_settings,
                                       color='SteelBlue2', 
                                       hover_color='SteelBlue1')
        self.settings_btn.pack(side=tk.RIGHT, padx=5)
        
        # Логин пользователя
        self.user_label = ttk.Label(top_panel, text=self.logged_in_user, font=('Arial', 12))
        self.user_label.pack(side=tk.RIGHT, padx=10)
        
        # Баланс
        self.balance_label = ttk.Label(self.main_window, text="Доходы: 0р. Расходы: 0р.", font=('Arial', 12))
        self.balance_label.pack(pady=10)
        
        # График расходов
        self.chart_frame = ttk.Frame(self.main_window)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Кнопки добавления операций
        buttons_frame = ttk.Frame(self.main_window)
        buttons_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ttk.Button(buttons_frame, text="Добавить доход", command=self.show_add_income_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Добавить расход", command=self.show_add_expense_window).pack(side=tk.RIGHT, padx=5)
        
        # Обновление данных
        self.update_balance()
        self.update_chart()
        self.apply_theme()
    
    def apply_theme(self):
        """Применяет выбранную тему"""
        if self.current_theme == "light":
            self.main_window.configure(bg="#f0f0f0")
            style = ttk.Style()
            style.configure(".", background="#f0f0f0", foreground="black")
        else:
            self.main_window.configure(bg="#2d2d2d")
            style = ttk.Style()
            style.configure(".", background="#2d2d2d", foreground="white")
    
    def toggle_theme(self):
        """Переключает тему между светлой и темной"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()
        self.save_data()
    
    def show_settings(self):
        """Показывает окно настроек"""
        SettingsWindow(self.main_window, self)
    
    def show_add_income_window(self):
        """Показывает окно добавления дохода"""
        AddIncomeWindow(self.main_window, self)
    
    def show_add_expense_window(self):
        """Показывает окно добавления расхода"""
        AddExpenseWindow(self.main_window, self)
    
    def update_balance(self):
        """Обновляет отображение баланса"""
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Доход")
        total_expense = sum(t["amount"] for t in self.transactions if t["type"] == "Расход")
        
        self.balance_label.config(text=f"Доходы: {total_income:.2f}р. Расходы: {total_expense:.2f}р.")
    
    def update_chart(self):
        """Обновляет график расходов"""
        # Очистка предыдущего графика
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if not self.transactions:
            ttk.Label(self.chart_frame, text="Нет данных для отображения").pack(expand=True)
            return
        
        # Получаем данные по расходам
        expenses = [t for t in self.transactions if t["type"] == "Расход"]
        if not expenses:
            ttk.Label(self.chart_frame, text="Нет данных о расходах").pack(expand=True)
            return
        
        # Группируем по категориям
        expense_data = {}
        for expense in expenses:
            expense_data[expense["category"]] = expense_data.get(expense["category"], 0) + expense["amount"]
        
        # Создаем график
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(expense_data.values(), labels=expense_data.keys(), autopct="%1.1f%%")
        ax.set_title("Расходы по категориям")
        
        # Встраиваем в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def save_data(self):
        """Сохраняет данные в файл"""
        data = {
            "transactions": self.transactions,
            "categories": self.categories,
            "theme": self.current_theme,
            "user": self.logged_in_user
        }
        
        try:
            with open("finance_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_data(self):
        """Загружает данные из файла"""
        try:
            if os.path.exists("finance_data.json"):
                with open("finance_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                self.transactions = data.get("transactions", [])
                self.categories = data.get("categories", {
                    "Доходы": ["Зарплата", "Премия", "Подарок", "Инвестиции", "Другое"],
                    "Расходы": ["Еда", "Транспорт", "Жилье", "Развлечения", "Здоровье", "Одежда", "Техника", "Другое"]
                })
                self.current_theme = data.get("theme", "light")
                self.logged_in_user = data.get("user", "")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.transactions = []
            self.categories = {
                "Доходы": ["Зарплата", "Премия", "Подарок", "Инвестиции", "Другое"],
                "Расходы": ["Еда", "Транспорт", "Жилье", "Развлечения", "Здоровье", "Одежда", "Техника", "Другое"]
            }
            self.current_theme = "light"
            self.logged_in_user = ""
    
    def on_close(self):
        """Обработчик закрытия приложения"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.save_data()
            self.main_window.destroy()
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
