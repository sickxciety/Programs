from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from PIL import Image, ImageTk
import json
import os
from random import randint
from datetime import *
from time import sleep
import threading

class Autorization(Toplevel):

    def __init__(self, master, main_app):
        super().__init__(master)
        self.master = master
        self.main_app = main_app
        self.geometry('350x250')
        self.title('Авторизация')
        self.resizable(False, False)
        self.icon = PhotoImage(file='logo.png')
        self.iconphoto(False, self.icon)

        self.login_text = ttk.Label(self, text='Логин', font=('Arial', 12))
        self.login_text.pack(anchor=CENTER, pady=10)

        self.login = ttk.Entry(self)
        self.login.pack(anchor=CENTER, ipadx=50, ipady=2)

        self.password_text = ttk.Label(self, text='Пароль', font=('Arial', 12))
        self.password_text.pack(anchor=CENTER, pady=10)

        self.password = ttk.Entry(self, show='*')
        self.password.pack(anchor=CENTER, ipadx=50, ipady=2)

        self.sign_in = ttk.Button(self, text='Вход', command=self.sign_in)
        self.sign_in.pack(anchor=CENTER, pady=20, ipady=2, ipadx=10)

        self.sign_up = ttk.Button(self, text='Зарегистрироваться', command=self.sign_up)
        self.sign_up.pack(anchor=CENTER, ipady=2, ipadx=15)

        self.users = 'json/account.json'

    def sign_in(self):
        login = self.login.get()
        password = self.password.get()

        if os.path.exists(self.users):
            with open(self.users, 'r') as user:
                users = json.load(user)
                if login in users and users[login] == password:
                    showinfo('Вход', 'Вход выполнен успешно!')
                    self.destroy()
                    self.main_app.main_window(login)
                else:
                    showerror('Вход', 'Неверное имя пользователя или пароль!')
        else:
            showerror('Вход', 'Такого пользователя не существует!')

    def sign_up(self):
        login = self.login.get()
        password = self.password.get()

        if not login or not password:
            showerror('Регистрация', 'Заполните все поля!')
            return

        if os.path.exists(self.users):
            with open(self.users, "r") as user:
                users = json.load(user)
        else:
            users = {}

        if login in users:
            showerror('Регистрация', 'Пользователь с таким именем уже существует!')
            return

        users[login] = password

        with open(self.users, "w") as user:
            json.dump(users, user)

        showinfo("Успех", "Регистрация успешна!")

class Circle_button(Canvas):
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

class Progressbar(Label):
    def __init__(self, master, width=125, height=125, image_prefix="progress_", num_images=100):
        Label.__init__(self, master, width=width, height=height)
        self.width = width
        self.height = height
        self.image_prefix = image_prefix
        self.num_images = num_images
        self.progress = 0
        self.full = False
        self.images = []
        self.load_images()
        self.configure(image=self.images[0])

    def load_images(self):
        try:
            for i in range(self.num_images):
                filename = f'progress_images/{self.image_prefix}{i}.png'
                img = Image.open(filename)
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)
        except FileNotFoundError as e:
             print(f'Ошибка. Проверьте файлы: {e}')

    def update_progress(self, progress):
        self.progress = progress
        if self.full:
           index = self.num_images - 1
        else:
           index = int(progress / 100 * (self.num_images - 1))

        self.configure(image=self.images[index])

    def increment_progress(self, water_drunk, water_goal):
        self.water_drunk = water_drunk
        self.water_goal = water_goal
        if not self.full:
            self.progress = int((self.water_drunk / self.water_goal) * 100)
            if self.progress >= 100:
                self.progress = 100
                self.full = True
            self.update_progress(self.progress)

class Setting(Toplevel):
    def __init__(self, master, main_app, login, water_goal):
        super().__init__(master)
        self.icon = PhotoImage(file='logo.png')
        self.iconphoto(False, self.icon)
        self.title('Настройки')
        self.geometry('300x300')
        self.resizable(False, False)
        self.master = master
        self.main_app = main_app
        self.login = login
        self.water_goal = water_goal

        self.title_calculation = ttk.Label(self, text='Расчёт нормы', font=('Arial', 16))
        self.title_calculation.pack(pady=10)
        self.frame_calculate = ttk.Frame(self)
        self.frame_calculate.pack()
        self.text_calculation = ttk.Label(self.frame_calculate, text='Введите свой вес: ', font=('Arial', 12))
        self.text_calculation.pack(side=LEFT)
        self.input_weight = ttk.Entry(self.frame_calculate, width=4)
        self.input_weight.pack(side=LEFT, padx=8)
        self.button_calculate = ttk.Button(self, text='Расчёт', command=self.update)
        self.button_calculate.pack(pady=10)
        self.print_calculation = ttk.Label(self, text=f'Ваша норма: {self.water_goal}мл', font=('Arial', 10))
        self.print_calculation.pack()

        self.title_water_goal = ttk.Label(self, text='Ввод нормы', font=('Arial', 16))
        self.title_water_goal.pack(pady=10)
        self.frame_water_goal = ttk.Frame(self)
        self.frame_water_goal.pack(pady=10)
        self.text_water_goal = ttk.Label(self.frame_water_goal, text='Норма воды в мл: ', font=('Arial', 12))
        self.text_water_goal.pack(side=LEFT)
        self.input_water_goal = ttk.Entry(self.frame_water_goal, width=5)
        self.input_water_goal.pack(side=LEFT, padx=8)

        self.save_button = ttk.Button(self, text='Сохранить', command=self.save_setting)
        self.save_button.pack(pady=25)


    def calculation_water(self, weight):
        try:
            weight = int(weight)
            if 0 < weight <= 150:
                self.water_goal = weight * 30
                return self.water_goal
            else:
                return 'Введите верный вес'
        except ValueError:
            return 'Введите верный вес'

    def update(self):
        weight = self.input_weight.get()
        result = self.calculation_water(weight)

        if isinstance(result, (int, float)):
            self.water_goal = result
            self.print_calculation.config(text=f'Ваша норма: {self.water_goal}мл')
        else:
            print('Ошибка данных')

    def save_setting(self):
        try:
            new_goal = int(self.input_water_goal.get())
            if new_goal <= 0:
                showerror('Ошибка', 'Норма воды должна быть положительным числом.')
                return

            self.main_app.user_data[self.login]['water_goal'] = new_goal
            self.main_app.save_user_setting()

            showinfo('Успех', 'Настройки сохранены!')
            self.destroy()

        except ValueError:
            showerror('Ошибка', 'Неверный формат нормы воды. Введите число.')

class Calendar(Toplevel):
    def __init__(self, master, main_app, calendar_drunk, login):
        super().__init__(master)
        self.icon = PhotoImage(file='logo.png')
        self.iconphoto(False, self.icon)
        self.title('Календарь')
        self.geometry('300x300')
        self.resizable(False, False)
        self.master = master
        self.main_app = main_app
        self.login = login
        self.calendar_drunk = calendar_drunk
        self.data = self.load_calendar()

        for date, drunk in self.data[self.login].items():
            self.info_frame = ttk.Frame(self)
            self.info_frame.pack(pady=10, fill=BOTH)
            self.date_text = ttk.Label(self.info_frame, text=f'Дата: {date}', font=('Arial', 12))
            self.date_text.pack(side=LEFT)
            self.drunk_text = ttk.Label(self.info_frame, text=f'Выпито: {drunk}', font=('Arial', 12))
            self.drunk_text.pack(side=RIGHT)
            self.line = Canvas(self, bg='black', width=300, height=1)
            self.line.pack(anchor=N)

    def load_calendar(self):
        try:
            with open(self.calendar_drunk, 'r') as drunk:
                return json.load(drunk)
        except json.JSONDecodeError:
            showinfo('Нет данных', 'Пока в календаре пусто!')

class WaterTrecker:
    def __init__(self):
        self.root = Tk()
        self.root.config(bg='SystemButtonFace')
        self.root.resizable(False, False)
        self.icon = PhotoImage(file='logo.png')
        self.root.iconphoto(False, self.icon)
        self.root.title('Водяной: контроль выпитой воды')
        self.root.geometry('300x400')

        self.login = None
        self.water_goal = None
        self.water_drunk = None
        self.date = date.today()
        self.user_setting = 'json/setting.json'
        self.quotes_motivation = 'json/quotes.json'
        self.calendar_drunk = 'json/calendar.json'

        self.user_data = self.user_setting_load()
        self.drunk_data = self.user_calendar_load()

        self.reminder_timer = threading.Thread(target=self.timer, daemon=True)

        self.auth = Autorization(self.root, self)
        self.root.withdraw()

    def user_setting_load(self):
        if os.path.exists(self.user_setting):
            try:
                with open(self.user_setting, 'r') as setting:
                    data = json.load(setting)
                    return data
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def save_user_setting(self):
        try:
            with open(self.user_setting, 'w') as setting:
                json.dump(self.user_data, setting, indent=4)
                self.water_drunk = self.user_data[self.login]['water_drunk']
                self.water_goal = self.user_data[self.login]['water_goal']
                self.progress_goal_text.config(text=f'Ваша норма: {self.water_goal}мл')
                self.progress_drunk_text.config(text=f'Выпито: {self.water_drunk}/{self.water_goal}мл')
        except Exception as error:
            print(f'Ошибка при сохранении: {error}')

    def user_calendar_load(self):
        if os.path.exists(self.calendar_drunk):
            try:
                with open(self.calendar_drunk, 'r') as drunk:
                    data = json.load(drunk)
                    return data
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def save_user_calendar(self):
        try:
            if f'{self.date.day}.{self.date.month}.{self.date.year}' == self.drunk_data[self.login]:
                with open(self.calendar_drunk, 'w') as drunk:
                    json.dump(self.drunk_data, drunk, indent=4)
            else:
                self.drunk_data[self.login][f'{self.date.day}.{self.date.month}.{self.date.year}'] = self.water_drunk
                with open(self.calendar_drunk, 'w') as drunk:
                    json.dump(self.drunk_data, drunk, indent=4)
        except Exception as error:
            print(f'Ошибка при сохранении: {error}')

    def main_window(self, login):
        self.login = login
        self.root.deiconify()

        if self.login not in self.user_data:
            self.user_data[self.login] = {'water_goal': 2000, 'water_drunk': 0}

        if self.login not in self.drunk_data:
            self.drunk_data[self.login] = {f'{self.date.day}.{self.date.month}.{self.date.year}': self.water_drunk}

        if f'{self.date.day}.{self.date.month}.{self.date.year}' != self.drunk_data[self.login]:
            self.user_data[self.login]['water_drunk'] = 0
            self.save_user_setting()

        self.water_goal = self.user_data[self.login]['water_goal']
        self.water_drunk = self.user_data[self.login]['water_drunk']

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill=BOTH)
        self.button_setting = Circle_button(self.login_frame, radius=15, command=self.open_setting, color='LightSkyBlue3', hover_color='LightSkyBlue2')
        self.button_setting.pack(side=LEFT, anchor=NW, pady=20, padx=15)
        self.button_calendar = Circle_button(self.login_frame, radius=20, command=self.open_calendar, color='SteelBlue2', hover_color='SteelBlue1')
        self.button_calendar.pack(side=RIGHT, anchor=NE, pady=10, padx=15)
        self.name_user = ttk.Label(self.login_frame, text=self.login, font=('Arial', 14))
        self.name_user.pack(side=RIGHT, anchor=N, pady=20)

        self.progressbar_frame = ttk.Frame(self.root)
        self.progressbar_frame.pack(pady=25)
        self.progressbar = Progressbar(self.progressbar_frame, width=125, height=125, image_prefix='progress_', num_images=100)
        self.progressbar.pack(side=LEFT)
        self.progress_goal_text = ttk.Label(self.progressbar_frame, text=f'Ваша норма: {self.water_goal}мл', font=('Arial', 12))
        self.progress_goal_text.pack(pady=30)
        self.progress_drunk_text = ttk.Label(self.progressbar_frame, text=f'Выпито: {self.water_drunk}/{self.water_goal}мл', font=('Arial', 12))
        self.progress_drunk_text.pack()

        self.drink_frame = ttk.Frame(self.root)
        self.drink_frame.pack(fill=BOTH)
        self.drink_input = ttk.Entry(self.drink_frame, width=5)
        self.drink_input.pack(side=LEFT, anchor=W, padx=15)
        self.drink_button = ttk.Button(self.drink_frame, text='Выпить', command=self.drink_water, width=8)
        self.drink_button.pack(side=LEFT, anchor=W, padx=5)

        self.motivation_frame = ttk.Frame(self.root, width=200)
        self.motivation_frame.pack(anchor=CENTER, pady=40)
        self.drink_motivation = ttk.Label(self.motivation_frame, text='Вода — жизнь!', font=('Arial', 12))
        self.drink_motivation.pack()

    def drink_water(self):
        try:
            amount = int(self.drink_input.get())
            if amount <= 0:
                showerror('Ошибка', 'Введите положительное число.')
                return
            self.water_drunk += amount
            self.user_data[self.login]['water_drunk'] = self.water_drunk
            self.water_goal = self.user_data[self.login]['water_goal']
            self.save_user_setting()
            self.drunk_data[self.login][f'{self.date.day}.{self.date.month}.{self.date.year}'] = self.water_drunk
            self.save_user_calendar()
            self.progress_drunk_text.config(text=f'Выпито: {self.water_drunk}/{self.water_goal}мл')
            self.progressbar.increment_progress(self.water_drunk, self.water_goal)
            self.motivation_quotes()
        except ValueError:
            showerror('Ошибка', 'Введите корректное число!')

    def motivation_quotes(self):
        try:
            with open(self.quotes_motivation, 'r', encoding='utf-8') as quote:
                quotes = json.load(quote)
                self.drink_motivation.config(text=f'{quotes[str(randint(1, 20))]}')
        except json.JSONDecodeError:
            showerror('Ошибка', 'Возможно файл повреждён!')

    def reminder(self):
        showinfo('Напоминание', 'Пора выпить воды!')

    def timer(self):
        while True:
            sleep(3600)
            self.reminder()

    def open_setting(self):
        Setting(self.root, self, self.login, self.water_goal)

    def open_calendar(self):
        Calendar(self.root, self, self.calendar_drunk, self.login)

    def run(self):
        self.root.mainloop()
        self.reminder_timer.start()

if __name__ == '__main__':
    app = WaterTrecker()
    app.run()
