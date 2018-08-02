# The code for changing pages was derived from:
# http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk
from datetime import datetime


class Base(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, HomeScreen, Today, Select, Bulk, ):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    program_list = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.intro_label = tk.Label(self, text="Welcome to the program")
        self.intro_label.pack(pady=10, padx=10)
        self.login_button = tk.Button(self, text="Initialize", command=self.load_file)
        self.login_button.pack()

    def load_file(self):
        # Load the contents of the main.text file into an list (main) for it to be used in the program
        with open('main.text', 'rt') as in_file:  # Open file lorem.txt for reading of text data.
            for line in in_file:  # For each line of text store in a string variable named "line", and
                self.program_list.append(line)  # add that line to our list of lines.
        print("Text file initialized. The list in memory is:\n", self.program_list)
        self.controller.show_frame(HomeScreen)


class HomeScreen(StartPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.date_today = None
        self.first_date_count = None
        self.last_date_count = None
        self.start_append = None
        self.end_append = None
        self.first_status = None
        self.last_status = None

        self.home_title = tk.Label(self, text="Home Screen")
        self.home_title.pack(pady=10, padx=10)
        self.today_path = tk.Button(self, text="Today", command=self.combined)
        self.today_path.pack()

    def combined(self):
        self.date_check()
        self.date_status()

    def date_check(self):
        # check if today's date is in the list. If: continue. If not: create a new pair of dates in the list

        self.date_today = datetime.now().strftime('%d-%m-%Y')
        self.start_append = "{}start\n".format(self.date_today)
        self.end_append = "{}end\n".format(self.date_today)

        for self.count, self.elem in enumerate(self.program_list):
            if self.elem == self.start_append:
                self.first_status = 1
                self.first_date_count = self.count
                print("Found the first date index:", self.first_date_count)
            if self.elem == self.end_append:
                self.last_status = 1
                self.last_date_count = self.count
                print("Found the last date index:", self.last_date_count)
                print("Both indexes found!!!")
                break
            else:
                print("Date not found on this particular index, trying again.")
        else:
            print("Assuming that there isn't yet the entries for today's date in the list")
            print("Appending the entries for today's date now.")
            self.program_list.append(self.start_append)
            self.program_list.append(self.end_append)
            label = tk.Label(self, text="Today's date which was previously not found, "
                                        "has now been appended to the list. Please click below to save to the main file"
                                        "again and start from the StartPage.")
            label.pack()
            self.restart_button = tk.Button(self, text="Restart", command=self.restart_save)
            self.restart_button.pack()

        return self.first_date_count, self.last_date_count

    def date_status(self):
        # this was made since the return (on line 113) ended up showing the frame of TodaySelect for some reason while
        #  I was on the Today screen. I don't know if the solution is the best as the for loop gets executed again since
        #  I needed to call the first and last date variables on line 187 (using '()' which calls it). Who knows.
        if self.first_status and self.last_status == 1:
            print("Good to go.")
            self.controller.show_frame(Select)

    def restart_save(self):
        self.save()
        self.controller.show_frame(Today)

    def save(self):
        print("Attempting save now")
        with open('main.text', 'w') as file:
            for list_value in self.program_list:
                file.write(list_value)
        print(self.program_list)


class Select(HomeScreen):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.intro_label = tk.Label(self, text="What would you like to do?")
        self.intro_label.pack()
        self.current_button = tk.Button(self, text="Fill in the current hour",
                                        command=lambda: self.controller.show_frame(Today))
        self.current_button.pack()
        self.bulk_button = tk.Button(self, text="Bulk fill the hours of the day",
                                     command=lambda: self.controller.show_frame(Bulk))
        self.bulk_button.pack()


class Today(HomeScreen):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Today's Progress")
        label.pack(pady=10, padx=10)

        self.current_label = tk.Label(self, text="The current hour is (24hr layout):")
        self.current_label.pack()
        self.hour_time = datetime.now().strftime('%H:00\n')
        self.current_hour = tk.Label(self, text=self.hour_time)
        self.current_hour.pack()

        self.question_label = tk.Label(self, text="What are you working on?")
        self.question_label.pack()

        # insert type of work (from a list)
        self.OPTIONS = ['Blank(0)', 'Sleep(1)', 'University/Self-study(2)', 'Downtime(3)', 'Examinations(4)',
                        'Social(5)', 'Exercise(6)', 'Productivity(7)', 'Gaming(8)', 'Preparation(9)', 'Family(10)',
                        'Travel(11)', 'Unproductive(12)', 'Paid Work(13)', 'Work Experience(14)']

        self.variable = tk.StringVar()
        self.variable.set(self.OPTIONS[7])
        self.type_work = tk.OptionMenu(self, self.variable, *self.OPTIONS)
        self.type_work.pack()
        self.submit_hour = tk.Button(self, text="Submit", command=self.append_hour)
        self.submit_hour.pack()
        self.save_button = tk.Button(self, text="Save", command=self.save)
        self.save_button.pack()
        self.back_home = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(Select))
        self.back_home.pack()

    def append_hour(self):
        self.first_date_count, self.last_date_count = self.date_check()
        print("\nFirst date pos\n", self.first_date_count)
        print("\nLast date pos\n", self.last_date_count)

        for count, enum in enumerate(self.OPTIONS):
            if enum == self.variable.get():
                self.optioncount = count    # keep the index of the hour type I clicked on to append later
                break

        # A temporary list is created as we cannot append to a specific index inside a slice. Temp list assumes that
        #  all of its list contents are that of the contents between today's date markers
        self.temporary_list = (self.program_list[self.first_date_count + 1:self.last_date_count])
        print(self.temporary_list)

        for count, enum in enumerate(self.temporary_list):
            if enum == self.hour_time:
                # the hour type next to the hour (in terms of index)
                #  now equals the option (hour type) that the user clicked on
                self.temporary_list[count+1] = ('%s\n' % self.optioncount)
                print("Now includes the new appended hour", self.temporary_list)
                break

        # Deleting the contents of today's date in the main list in order to append the new temporary (updated) list.
        del self.program_list[self.first_date_count + 1:self.last_date_count]

        # The main list now equals the main list up to the point of the start marker for today's date,
        # the contents of today's list and the rest of the main lists contents past the end marker (first date + 1).
        self.program_list = self.program_list[:self.first_date_count + 1] + self.temporary_list + \
            self.program_list[self.first_date_count+1:]


class Bulk(HomeScreen):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Welcome to da bulk page. Useful for checking in your sleep hours")
        self.label.pack()

        self.label = tk.Label(self, text="Which hours do you wish to fill in?")
        self.label.pack()

        self.zerozerovar = tk.IntVar()
        self.zeroonevar = tk.IntVar()
        self.zerotwovar = tk.IntVar()
        self.zerothreevar = tk.IntVar()
        self.zerofourvar = tk.IntVar()
        self.zerofivevar = tk.IntVar()
        self.zerosixvar = tk.IntVar()
        self.zerosevenvar = tk.IntVar()
        self.zeroeightvar = tk.IntVar()
        self.zeroninevar = tk.IntVar()
        self.onezerovar = tk.IntVar()
        self.oneonevar = tk.IntVar()
        self.onetwovar = tk.IntVar()
        self.onethreevar = tk.IntVar()
        self.onefourvar = tk.IntVar()
        self.onefivevar = tk.IntVar()
        self.onesixvar = tk.IntVar()
        self.onesevenvar = tk.IntVar()
        self.oneeightvar = tk.IntVar()
        self.oneninevar = tk.IntVar()
        self.twozerovar = tk.IntVar()
        self.twoonevar = tk.IntVar()
        self.twotwovar = tk.IntVar()
        self.twothreevar = tk.IntVar()

        self.zerozero_check = tk.Checkbutton(self, text="00:00", variable=self.zerozerovar)
        self.zerozero_check.pack()
        self.zeroone_check = tk.Checkbutton(self, text="01:00", variable=self.zeroonevar)
        self.zeroone_check.pack()
        self.zerotwo_check = tk.Checkbutton(self, text="02:00", variable=self.zerotwovar)
        self.zerotwo_check.pack()
        self.zerothree_check = tk.Checkbutton(self, text="03:00", variable=self.zerothreevar)
        self.zerothree_check.pack()
        self.zerofour_check = tk.Checkbutton(self, text="04:00", variable=self.zerofourvar)
        self.zerofour_check.pack()
        self.zerofive_check = tk.Checkbutton(self, text="05:00", variable=self.zerofivevar)
        self.zerofive_check.pack()
        self.zerosix_check = tk.Checkbutton(self, text="06:00", variable=self.zerosixvar)
        self.zerosix_check.pack()
        self.zeroseven_check = tk.Checkbutton(self, text="07:00", variable=self.zerosevenvar)
        self.zeroseven_check.pack()
        self.zeroeight_check = tk.Checkbutton(self, text="08:00", variable=self.zeroeightvar)
        self.zeroeight_check.pack()
        self.zeronine_check = tk.Checkbutton(self, text="09:00", variable=self.zeroninevar)
        self.zeronine_check.pack()
        self.onezero_check = tk.Checkbutton(self, text="10:00", variable=self.onezerovar)
        self.onezero_check.pack()
        self.oneone_check = tk.Checkbutton(self, text="11:00", variable=self.oneonevar)
        self.oneone_check.pack()
        self.onetwo_check = tk.Checkbutton(self, text="12:00", variable=self.onetwovar)
        self.onetwo_check.pack()
        self.onethree_check = tk.Checkbutton(self, text="13:00", variable=self.onethreevar)
        self.onethree_check.pack()
        self.onefour_check = tk.Checkbutton(self, text="14:00", variable=self.onefourvar)
        self.onefour_check.pack()
        self.onefive_check = tk.Checkbutton(self, text="15:00", variable=self.onefivevar)
        self.onefive_check.pack()
        self.onesix_check = tk.Checkbutton(self, text="16:00", variable=self.onesixvar)
        self.onesix_check.pack()
        self.oneseven_check = tk.Checkbutton(self, text="17:00", variable=self.onesevenvar)
        self.oneseven_check.pack()
        self.oneeight_check = tk.Checkbutton(self, text="18:00", variable=self.oneeightvar)
        self.oneeight_check.pack()
        self.onenine_check = tk.Checkbutton(self, text="19:00", variable=self.oneninevar)
        self.onenine_check.pack()
        self.twozero_check = tk.Checkbutton(self, text="20:00", variable=self.twozerovar)
        self.twozero_check.pack()
        self.twoone_check = tk.Checkbutton(self, text="21:00", variable=self.twoonevar)
        self.twoone_check.pack()
        self.twotwo_check = tk.Checkbutton(self, text="22:00", variable=self.twotwovar)
        self.twotwo_check.pack()
        self.twothree_check = tk.Checkbutton(self, text="23:00", variable=self.twothreevar)
        self.twothree_check.pack()

        self.bulk_submit = tk.Button(self, text="Submit", command=self.bulk_append)
        self.bulk_submit.pack()

    def bulk_append(self):
        print("!")

app = Base()
app.mainloop()
