import tkinter
import tkinter.messagebox
import pickle
import datetime
from datetime import date
import numpy

today = datetime.date.today()

def task_window():
    def check_date(day, month, year):
        try:
            if(day == "" or month == "" or year == ""):
                tkinter.messagebox.showwarning(title="Warning!", message="Please enter valid date")
                return False
            some_day = datetime.date(int(year), int(month), int(day))
            if (today <= some_day):
                return True
            else: 
                tkinter.messagebox.showwarning(title="Warning!", message="Please enter valid date")
                return False
        except:
            tkinter.messagebox.showwarning(title="Warning!", message="Please enter valid date")
            return False

    def add_task(entry_task, day, month, year, description):
        if (entry_task != "" and check_date(day, month, year)):
            listbox_tasks.insert(tkinter.END, entry_task)
            listbox_dates.insert(tkinter.END, (datetime.date(int(year), int(month), int(day)))) 
            listbox_days_left.insert(tkinter.END, str((datetime.date(int(year), int(month), int(day)) - today).days))
            listbox_description.insert(tkinter.END, description)
            task_window.destroy()
            sort_list()
        if (entry_task == ""):
            tkinter.messagebox.showwarning(title="Warning!", message="Please enter task name")
            
    task_window = tkinter.Toplevel()
    canvas = tkinter.Canvas(task_window, height=500, width=800)
    canvas.pack()

    cancel_button = tkinter.Button(task_window, text="Cancel", command=task_window.destroy)
    cancel_button.place(relx=0.5, rely=0.9, relwidth=0.175, relheight=0.065, anchor="n")

    task_name_label = tkinter.Label(task_window, text="Task name:", font=("Artifakt Element", 18))
    task_name_label.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.075, anchor="w")

    enter_task = tkinter.Entry(task_window, font=("Malayalam MN", 18))
    enter_task.place(relx=1, rely=0.05, relwidth=0.8, relheight=0.075, anchor="e")
    enter_task.focus()

    due_date_label = tkinter.Label(task_window, text="Due Date", font=("Artifakt Element", 18))
    day_label = tkinter.Label(task_window, text="Day: ", font=("Artifakt Element", 18))
    month_label = tkinter.Label(task_window, text="Month: ", font=("Artifakt Element", 18))
    year_label = tkinter.Label(task_window, text="Year: ", font=("Artifakt Element", 18))

    due_date_label.place(relx=0, rely=0.125, relwidth=0.2, relheight=0.075, anchor="w")
    day_label.place(relx=0.15, rely=0.125, relwidth=0.2, relheight=0.075, anchor="w")
    month_label.place(relx=0.35, rely=0.125, relwidth=0.2, relheight=0.075, anchor="w")
    year_label.place(relx=0.55, rely=0.125, relwidth=0.2, relheight=0.075, anchor="w")

    due_date_day = tkinter.Entry(task_window, font=("Malayalam MN", 18))
    due_date_month = tkinter.Entry(task_window, font=("Malayalam MN", 18))
    due_date_year = tkinter.Entry(task_window, font=("Malayalam MN", 18))
    due_date_month.insert(tkinter.END, datetime.date.today().month)
    due_date_year.insert(tkinter.END, datetime.date.today().year)

    due_date_day.place(relx=0.4, rely=0.135, relwidth=0.1, relheight=0.075, anchor="e")
    due_date_month.place(relx=0.6, rely=0.135, relwidth=0.1, relheight=0.075, anchor="e")
    due_date_year.place(relx=0.8, rely=0.135, relwidth=0.1, relheight=0.075, anchor="e")

    description_label = tkinter.Label(task_window, text="Description: ", font=("Artifakt Element", 18))
    description_label.place(relx=0, rely=0.195, relwidth=0.2, relheight=0.075, anchor="w")

    description = tkinter.Text(task_window, font=("Malayalam MN", 18), height=50)
    description.place(relx=1, rely=0.18, relwidth=0.8, relheight=0.6, anchor="ne")

    button_add_task = tkinter.Button(task_window, text="Add task", width=48, command=lambda: add_task(enter_task.get(), due_date_day.get(), due_date_month.get(), due_date_year.get(), description.get("1.0", tkinter.END)), font=("Artifakt Element", 18))
    button_add_task.place(relx=0.5, rely=0.8, relwidth=1, relheight=0.08, anchor="n")

    task_window.bind('<Return>',lambda event: add_task(enter_task.get(), due_date_day.get(), due_date_month.get(), due_date_year.get(), description.get("1.0", tkinter.END)))

def description_window(selection):
    def save_close():
        descriptions = listbox_description.get(0, listbox_description.size())
        listbox_description.delete(0, listbox_description.size())
        index = 0
        for description in descriptions:
            if index == selection:
                break
            listbox_description.insert(tkinter.END, description)
            index += 1
        listbox_description.insert(tkinter.END, description_text.get("1.0", tkinter.END))
        index += 1
        for description in descriptions[index::]:
            listbox_description.insert(tkinter.END, description)

        description_window.destroy()
    
    def on_description_closing():
        if ((description_text.get("1.0", tkinter.END)) != original_description):
            if tkinter.messagebox.askyesno(title="Save or discard changes", message="Would you like to save changes?"):
                descriptions = listbox_description.get(0, listbox_description.size())
                listbox_description.delete(0, listbox_description.size())
                index = 0
                for description in descriptions:
                    if index == selection:
                        break
                    listbox_description.insert(tkinter.END, description)
                    index += 1
                listbox_description.insert(tkinter.END, description_text.get("1.0", tkinter.END))
                index += 1
                for description in descriptions[index::]:
                   listbox_description.insert(tkinter.END, description)

                description_window.destroy()
            else:
                description_window.destroy()
        else:
            description_window.destroy()

    description_window = tkinter.Toplevel()
    canvas = tkinter.Canvas(description_window, height=500, width=800)
    canvas.pack()

    close_button = tkinter.Button(description_window, text="Close", command=description_window.destroy)
    close_button.place(relx=0.5, rely=0.875, relwidth=0.175, relheight=0.065, anchor="n")

    save_button = tkinter.Button(description_window, text="Save and close", command=save_close, font=("Artifakt Element", 18))
    save_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.1, anchor="n")

    description_label = tkinter.Label(description_window, text="Description ", font=("Artifakt Element", 18))
    description_label.place(relx=0.5, rely=0.02, relwidth=0.8, relheight=0.08, anchor="n")

    description_text = tkinter.Text(description_window, font=("Malayalam MN", 18), height=50)
    description_text.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.6, anchor="n")
    description_text.insert(tkinter.END, listbox_description.get(selection))

    original_description = description_text.get("1.0", tkinter.END)

    description_window.protocol("WM_DELETE_WINDOW", on_description_closing)


def delete_task():
    try:
        selection = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selection)
        listbox_dates.delete(selection)
        listbox_days_left.delete(selection)
        listbox_description.delete(selection)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Please select a task")

def load_tasks():
    try:
        tasks = pickle.load(open("/Users/nathan/Documents/Coding/To_do_data/Tasks.data", "rb"))
        dates = pickle.load(open("/Users/nathan/Documents/Coding/To_do_data/Dates.data", "rb"))
        #days_left = pickle.load(open("/Users/nathan/Documents/Coding/To_do_data/Days_left.data", "rb"))
        descriptions = pickle.load(open("/Users/nathan/Documents/Coding/To_do_data/Description.data", "rb"))
        clear_tasks()
        for task in tasks: 
            listbox_tasks.insert(tkinter.END, task)
        for date in dates:
            listbox_dates.insert(tkinter.END, date)
        for days in dates:
            date = days.split("-")
            listbox_days_left.insert(tkinter.END, str((datetime.date(int(date[0]), int(date[1]), int(date[2])) - today).days))
        for description in descriptions:
            listbox_description.insert(tkinter.END, description)
    except:
        tkinter.messagebox.showwarning(title="Warning!", message="Cannot find data files")

def save_tasks():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    dates = listbox_dates.get(0, listbox_tasks.size())
    days_left = listbox_days_left.get(0, listbox_tasks.size())
    descriptions = listbox_description.get(0, listbox_tasks.size())
    pickle.dump(tasks, open("/Users/nathan/Documents/Coding/To_do_data/Tasks.data", "wb"))
    pickle.dump(dates, open("/Users/nathan/Documents/Coding/To_do_data/Dates.data", "wb"))
    #pickle.dump(days_left, open("/Users/nathan/Documents/Coding/To_do_data/Days_left.data", "wb"))
    pickle.dump(descriptions, open("/Users/nathan/Documents/Coding/To_do_data/Description.data", "wb"))

def clear_tasks():
    listbox_tasks.delete(0, listbox_tasks.size())
    listbox_dates.delete(0, listbox_dates.size())
    listbox_days_left.delete(0, listbox_days_left.size())
    listbox_description.delete(0, listbox_description.size())

def multiple_yview(*args):
    listbox_tasks.yview(*args)
    listbox_days_left.yview(*args)
    listbox_dates.yview(*args)

def sort_list():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    dates = listbox_dates.get(0, listbox_tasks.size())
    days_left = listbox_days_left.get(0, listbox_tasks.size())
    descriptions = listbox_description.get(0, listbox_description.size())
    sorted_list = numpy.argsort(days_left)
    clear_tasks()
    for i in sorted_list:
        listbox_tasks.insert(tkinter.END, tasks[i])
        listbox_dates.insert(tkinter.END, dates[i]) 
        listbox_days_left.insert(tkinter.END, days_left[i])
        listbox_description.insert(tkinter.END, descriptions[i])

def on_closing():
    save_tasks()
    root.destroy()

#root GUI
root = tkinter.Tk()
root.title("To Do")

canvas = tkinter.Canvas(root, height=690, width=720)
canvas.pack()

tasks_label = tkinter.Label(root, text="Tasks", font=("Artifakt Element", 16), borderwidth=2, relief="solid")
tasks_label.place(relx=0, rely=0.025, relwidth=0.6, relheight=0.05, anchor="w")

days_left_label = tkinter.Label(root, text="Days left", font=("Artifakt Element", 16), borderwidth=2, relief="solid")
days_left_label.place(relx=0.6, rely=0.025, relwidth=0.175, relheight=0.05, anchor="w")

dates_label = tkinter.Label(root, text="Due date", font=("Artifakt Element", 16), borderwidth=2, relief="solid")
dates_label.place(relx=0.775, rely=0.025, relwidth=0.225, relheight=0.05, anchor="w")

frame_tasks = tkinter.Frame(root)
frame_tasks.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.625, anchor="n")

scrollbar_tasks = tkinter.Scrollbar(frame_tasks)

listbox_tasks = tkinter.Listbox(frame_tasks, font=("Artifakt Element", 20), yscrollcommand=scrollbar_tasks.set)
listbox_tasks.place(relx=0, rely=0.5, relwidth=0.6, relheight=1, anchor="w")

listbox_dates = tkinter.Listbox(frame_tasks, font=("Artifakt Element", 20), yscrollcommand=scrollbar_tasks.set)
listbox_dates.place(relx=1, rely=0.5, relwidth=0.225, relheight=1, anchor="e")

listbox_days_left = tkinter.Listbox(frame_tasks, font=("Artifakt Element", 20), yscrollcommand=scrollbar_tasks.set)
listbox_days_left.place(relx=0.775, rely=0.5, relwidth=0.175, relheight=1, anchor="e")

listbox_description = tkinter.Listbox(frame_tasks, font=("Artifakt Element", 20))
listbox_description.place(relx=0, rely=0, relwidth=0, relheight=0, anchor="n")

scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)
scrollbar_tasks.lift()
scrollbar_tasks.config(command=multiple_yview)

button_add_task = tkinter.Button(root, text="Add task", width=48, command=task_window, font=("Artifakt Element", 18))
button_add_task.place(relx=0.5, rely=0.68, relwidth=1, relheight=0.08, anchor="n")

button_delete_task = tkinter.Button(root, text="Delete task", width=48, command=delete_task, font=("Artifakt Element", 18))
button_delete_task.place(relx=0.5, rely=0.76, relwidth=1, relheight=0.08, anchor="n")

button_clear_tasks = tkinter.Button(root, text="Clear all tasks", width=48, command=clear_tasks, font=("Artifakt Element", 18))
button_clear_tasks.place(relx=0.5, rely=0.84, relwidth=1, relheight=0.08, anchor="n")

button_save = tkinter.Button(root, text="Save and quit", width=48, command=on_closing, font=("Artifakt Element", 18))
button_save.place(relx=0.5, rely=0.92, relwidth=1, relheight=0.08, anchor="n")

listbox_tasks.bind('<Double-1>', lambda x: description_window(listbox_tasks.curselection()[0]))

root.bind('<BackSpace>',lambda event: delete_task())

root.bind('<Return>',lambda event: task_window())

root.protocol("WM_DELETE_WINDOW", on_closing)

load_tasks()

sort_list()

root.mainloop()