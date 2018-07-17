# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk
from datetime import datetime

class base(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, HomeScreen, today, bulk):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.intro_label = tk.Label(self,text="Welcome to the program")
        self.intro_label.pack()

        self.v = tk.StringVar(self, value="Enter Username")
        self.user_text = tk.Entry(self, textvariable=self.v)
        self.user_text.pack()

        self.c = tk.StringVar(self, value="Enter Password")
        self.pass_text = tk.Entry(self, textvariable=self.c)
        self.pass_text.pack()

        self.login_button = tk.Button(self,text="Login", command=self.login_check)
        self.login_button.pack()

    def login_check(self):
        if 2 > 1:
            self.login_success = tk.Label(self,text="Successful login, continue to the home screen.")
            self.login_success.pack()
            self.login_proceed = tk.Button(self, text="Proceed", command=lambda: self.controller.show_frame(HomeScreen))
            self.login_proceed.pack()


class HomeScreen(tk.Frame):

    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Homescreen")
        label.pack(pady=10, padx=10)

        self.today_label = tk.Button(self,text="Today", command=lambda: self.controller.show_frame(today))
        self.today_label.pack()

class today(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Today's Progress")
        label.pack(pady=10, padx=10)

        self.current_label = tk.Label(self,text="The current hour is (24hr layout):")
        self.current_label.pack()
        variable = datetime.now().strftime('%H:00')
        self.current_hour = tk.Label(self,text=variable)
        self.current_hour.pack()

        self.question_label = tk.Label(self, text="What are you working on?")
        self.question_label.pack()

        self.descriptive_label = tk.Label(self, text="Descriptive description of your current hour")
        self.descriptive_label.pack()

        self.back_homescreen = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(HomeScreen))
        self.back_homescreen.pack()

        self.bulk_fill = tk.Button(self, text="Bulk fill hours", command=lambda: self.controller.show_frame(bulk))
        self.bulk_fill.pack()

class bulk(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bulk fill your hours")
        label.pack(pady=10, padx=10)

        self.back_today = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(today))
        self.back_today.pack()

app = base()
app.mainloop()