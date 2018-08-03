import tkinter as tk
from datetime import datetime
import sys

LARGE_FONT = ("Verdana", 12)


class Base(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = MenuBar(self)
        self.config(menu=menubar)

        self.frames = {}
        for F in (Initialize, Choose, Edit):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Initialize)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Program", underline=0, menu=fileMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=1, command=self.quit)

    def quit(self):
        sys.exit(0)


class Initialize(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global program_list
        program_list = []
        label = tk.Label(self, text="Init Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Initialize", command=self.load_file)
        button.pack()

    def load_file(self):
        # Load the contents of the main.text file into an list (main) for it to be used in the program
        with open('main.text', 'rt') as in_file:  # Open file lorem.txt for reading of text data.
            for line in in_file:  # For each line of text store in a string variable named "line", and
                program_list.append(line)  # add that line to our list of lines.
        print("Text file initialized. The list in memory is:\n", program_list)
        self.controller.show_frame(Choose)


class Choose(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Date Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Today", command=self.load_today)
        button1.pack()
        # TODO : add previous dates functionality

    def load_today(self):
        self.date_today = datetime.now().strftime('%d-%m-%Y')
        self.start_append = "{}start\n".format(self.date_today)
        self.end_append = "{}end\n".format(self.date_today)

        for self.count, self.elem in enumerate(program_list):

            if self.elem == self.start_append:
                global first_date_count
                first_date_count = self.count
                print("Found the first date index:", first_date_count)

            if self.elem == self.end_append:
                global last_date_count
                last_date_count = self.count
                print("Found the last date index:", last_date_count)
                print("Both indexes found, sending you to the next stage.")
                global temporary_list
                temporary_list = program_list[first_date_count + 1:last_date_count]
                self.controller.show_frame(Edit)
                break

            else:
                print("Date not found on this particular index, trying again.")
        else:
            print("Assuming that there isn't yet the entries for today's date in the list")
            print("Appending the entries for today's date now.")
            self.date_append = [self.start_append, '00:00\n', 'type:empty\n', '01:00\n', 'type:empty\n', '02:00\n',
                                'type:empty\n', '03:00\n', 'type:empty\n', '04:00\n', 'type:empty\n', '05:00\n',
                                'type:empty\n', '06:00\n', 'type:empty\n', '07:00\n', 'type:empty\n', '08:00\n',
                                'type:empty\n', '09:00\n', 'type:empty\n', '10:00\n', 'type:empty\n', '11:00\n',
                                'type:empty\n', '12:00\n', 'type:empty\n', '13:00\n', 'type:empty\n', '14:00\n',
                                'type:empty\n', '15:00\n', 'type:empty\n', '16:00\n', 'type:empty\n', '17:00\n',
                                'type:empty\n', '18:00\n', 'type:empty\n', '19:00\n', 'type:empty\n', '20:00\n',
                                'type:empty\n', '21:00\n', 'type:empty\n', '22:00\n', 'type:empty\n', '23:00\n',
                                'type:empty\n', self.end_append]

            for i in self.date_append:
                program_list.append(i)
            label = tk.Label(self, text="New date appended. Proceed to Edit page.\n")
            print(program_list)
            label.pack()
            self.restart_button = tk.Button(self, text="Continue", command=self.save_continue)
            self.restart_button.pack()

    def save_continue(self):
        print("Attempting save now")
        with open('main.text', 'w') as file:
            for list_value in program_list:
                file.write(list_value)
        print("Text file initialized. The list in memory is:\n", program_list)
        self.controller.show_frame(Edit)


class Edit(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Edit Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # insert type of work (from a list)
        self.OPTIONS = ['Blank(0)', 'Sleep(1)', 'University/Self-study(2)', 'Downtime(3)', 'Examinations(4)',
                        'Social(5)', 'Exercise(6)', 'Productivity(7)', 'Gaming(8)', 'Preparation(9)', 'Family(10)',
                        'Travel(11)', 'Unproductive(12)', 'Paid Work(13)', 'Work Experience(14)']
        self.default = tk.StringVar()
        self.default.set(self.OPTIONS[7])

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
        self.type_work = tk.OptionMenu(self, self.default, *self.OPTIONS)
        self.type_work.pack()
        button1 = tk.Button(self, text="Submit", command=self.append_stageone)
        button1.pack()
        button2 = tk.Button(self, text="Back to Choose", command=lambda: controller.show_frame(Choose))
        button2.pack()
        button3 = tk.Button(self, text="Print", command=self.test)
        button3.pack()
        button4 = tk.Button(self, text="Save", command=self.save_button)
        button4.pack()

    def append_stageone(self):
        self.var_counter = [self.zerozerovar.get(), self.zeroonevar.get(), self.zerotwovar.get(),
                            self.zerothreevar.get(), self.zerofourvar.get(), self.zerofivevar.get(),
                            self.zerosixvar.get(), self.zerosevenvar.get(), self.zeroeightvar.get(),
                            self.zeroninevar.get(), self.onezerovar.get(), self.oneonevar.get(),
                            self.onetwovar.get(), self.onethreevar.get(), self.onefourvar.get(),
                            self.onefivevar.get(), self.onesixvar.get(), self.onesevenvar.get(),
                            self.oneeightvar.get(), self.oneninevar.get(), self.twozerovar.get(),
                            self.twoonevar.get(), self.twotwovar.get(), self.twothreevar.get()]
        # List containing the state of the checkbuttons on the screen.

        self.zerotonine = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.tentotwentythree = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        for self.count, self.enum in enumerate(self.OPTIONS):
            if self.enum == self.default.get():  # Iterate through hour type array to find the hour type I selected
                self.bulkoption = self.count  # keep the index of the hour type I clicked on to bulk append later
                print("GOOD")
                self.append_stagetwo()
                break   # break as we only need to find the hour type once (one type to fill across a number of hrs)

    def append_stagetwo(self):
        print("exec stage_two")
        for self.countcontinue, self.enumcontinue in enumerate(self.var_counter):
            if self.enumcontinue == 1:   # Checks if a checkbox is ticked
                if self.countcontinue in self.zerotonine:
                    print("From 0 to 9")
                    self.hour_append = ('0%s:00\n' % self.countcontinue)  # we keep the index of the checkbox plus
                    #  '0:00\n' (the number of indexes in the var_counter array are the same as the number of hours
                    #  in the day - 23 (Start at 0) ~ 24 hrs) to find it in the temporary list later.
                    #  Add a '0' behind the string so it mimics the 24 hour format.
                    print(self.hour_append)
                    self.append_stagethree()
                if self.countcontinue in self.tentotwentythree:
                    print("From 10 to 23.")
                    self.hour_append = ('%s:00\n' % self.countcontinue)  # we keep the index of the checkbox
                    #  plus ':00\n' (the number of indexes in the var_counter array are the same as the number
                    #  of hours in the day - 23 (Start at 0) ~ 24 ) to find it in the temporary list later.
                    print(self.hour_append)
                    self.append_stagethree()

    def append_stagethree(self):
        print("exec stage_three")
        for self.countfinal, self.enumfinal in enumerate(temporary_list):
            if self.enumfinal == self.hour_append:
                temporary_list[self.countfinal+1] = ('%s\n' % self.bulkoption)    # the hour type next to the hour
                # (in terms of index) now equals the option (hour type) that the user clicked on (tkinter OptionMenu)
                print("Done-----")
                break
        else:
            print("Nah. ")

    def save_button(self):
        print("Saving the contents of the temporary list into main list.")
        global program_list

        # Deleting the contents of today's date in the main list in order
        # to append the new temporary (updated) list.
        del program_list[first_date_count + 1:last_date_count]

        # The main list now equals the main list up to the point of the start marker for today's date,
        # the contents of today's list and the rest of the main lists contents past the end marker (first date + 1).
        program_list = program_list[:first_date_count + 1] + temporary_list + \
            program_list[first_date_count + 1:]

        with open('main.text', 'w') as file:
            for i in program_list:
                file.write(i)

        print("The following has been written into the text file", program_list)

    def test(self):
        print("Temporary list\n", temporary_list)
        print("Main list\n", program_list)


app = Base()
app.mainloop()
