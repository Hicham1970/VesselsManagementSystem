from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os

con = None
mycurs = None
usernamentry = None
passwordentry = None


# Logic Part

def toplevel_data():
    global idEntry, nameEntry, flagEntry, imoEntry, cargoEntry, qtyEntry, clientEntry, doaEntry, dodEntry, screen
    screen = Toplevel()
    screen.geometry('335x490+03+185')
    screen.title('Update Vessel')
    screen.resizable(False, False)
    screen.grab_set()

    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=10, pady=8, sticky='w')
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    idEntry.grid(row=0, column=1, padx=5, pady=6)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=10, pady=8, sticky='w')
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    nameEntry.grid(row=1, column=1, padx=5, pady=6)

    flagLabel = Label(screen, text='Flag', font=('times new roman', 20, 'bold'))
    flagLabel.grid(row=3, column=0, padx=10, pady=8, sticky='w')
    flagEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    flagEntry.grid(row=2, column=1, padx=5, pady=6)

    imoLabel = Label(screen, text='Imo', font=('times new roman', 20, 'bold'))
    imoLabel.grid(row=2, column=0, padx=10, pady=8, sticky='w')
    imoEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    imoEntry.grid(row=3, column=1, padx=5, pady=6)

    cargoLabel = Label(screen, text='Cargo', font=('times new roman', 20, 'bold'))
    cargoLabel.grid(row=4, column=0, padx=10, pady=8, sticky='w')
    cargoEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    cargoEntry.grid(row=4, column=1, padx=5, pady=6)

    qtyLabel = Label(screen, text='Quantity', font=('times new roman', 14, 'bold'))
    qtyLabel.grid(row=5, column=0, padx=10, pady=8, sticky='w')
    qtyEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    qtyEntry.grid(row=5, column=1, padx=5, pady=6)

    clientLabel = Label(screen, text='Client', font=('times new roman', 14, 'bold'))
    clientLabel.grid(row=6, column=0, padx=10, pady=8, sticky='w')
    clientEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    clientEntry.grid(row=6, column=1, padx=5, pady=6)

    doaLabel = Label(screen, text='D O A', font=('times new roman', 14, 'bold'))
    doaLabel.grid(row=7, column=0, padx=10, pady=8, sticky='w')
    doaEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    doaEntry.grid(row=7, column=1, padx=5, pady=6)

    dodLabel = Label(screen, text='D O D', font=('times new roman', 14, 'bold'))
    dodLabel.grid(row=8, column=0, padx=10, pady=8, sticky='w')
    dodEntry = Entry(screen, font=('roman', 15, 'bold'), width=20)
    dodEntry.grid(row=8, column=1, padx=10, pady=10)

    updateButton = ttk.Button(screen, text='Update', command=update_data)
    updateButton.grid(row=9, column=1, padx=10, pady=10)


def update_data():
    query = 'update vessel set name=?, flag = ?, imo = ?, cargo=?, qty=?, client=?, doa=?, dod=? where vid=?'
    mycurs.execute(query, (
    nameEntry.get(), flagEntry.get(), imoEntry.get(), cargoEntry.get(), qtyEntry.get(), clientEntry.get(),
    doaEntry.get(), dodEntry.get(), idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id{idEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_vessel()


    indexing = vessel_table.focus()
    # print(indexing)
    content = vessel_table.item(indexing)
    # print(content)
    list_data = content['values']

    idEntry.insert(0, list_data[0])
    nameEntry.insert(0, list_data[1])
    flagEntry.insert(0, list_data[3])
    imoEntry.insert(0, list_data[2])
    cargoEntry.insert(0, list_data[4])
    qtyEntry.insert(0, list_data[5])
    clientEntry.insert(0, list_data[6])
    doaEntry.insert(0, list_data[7])
    dodEntry.insert(0, list_data[8])


def show_vessel():
    query = 'SELECT * FROM vessel'
    mycurs.execute(query)
    fetched_data = mycurs.fetchall()
    vessel_table.delete(*vessel_table.get_children())
    for data in fetched_data:
        vessel_table.insert('', END, values=data)


def delete_vessel():
    indexing = vessel_table.focus()
    content = vessel_table.item(indexing)
    content_id = content['values'][0]

    query = 'DELETE FROM vessel WHERE vid = ?'
    mycurs.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo('Deleted', f'Id: {content_id} is deleted successfully')
    query = 'SELECT * FROM vessel'
    mycurs.execute(query)
    fetched_data = mycurs.fetchall()
    vessel_table.delete(*vessel_table.get_children())
    for data in fetched_data:
        vessel_table.insert('', END, values=data)


def search_data():
    query = "SELECT * FROM (vessel) WHERE vid = ? or name = ? or flag = ? " \
            "or imo = ? or cargo = ? or qty = ? or client = ? or doa = ? " \
            "or dod = ? "
    mycurs.execute(query, (idEntry.get(), nameEntry.get(), flagEntry.get(), imoEntry.get(),
                           cargoEntry.get(), qtyEntry.get(), clientEntry.get(),
                           doaEntry.get(), dodEntry.get()))
    vessel_table.delete(*vessel_table.get_children())
    fetched_data = mycurs.fetchall()
    for data in fetched_data:
        # data_list = list(data)
        vessel_table.insert('', END, values=data)


def add_data():
    if idEntry.get() == '' or nameEntry.get() == '' or flagEntry.get() == '' or imoEntry.get() == '' \
            or cargoEntry.get() == '' or qtyEntry.get() == '' or clientEntry.get() == '' \
            or doaEntry.get() == '' or dodEntry.get() == '':
        messagebox.showerror('Error', 'Please fill up all the fields', parent=screen)
        return
    else:
        try:
            query = 'INSERT INTO vessel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            mycurs.execute(query,
                           (idEntry.get(), nameEntry.get(), flagEntry.get(), imoEntry.get(), cargoEntry.get(),
                            qtyEntry.get(), clientEntry.get(), doaEntry.get(), dodEntry.get()))
            con.commit()
            result = messagebox.askyesno('Question', 'Data add successfully ,\
             Do you want to clean the form?', parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                flagEntry.delete(0, END)
                imoEntry.delete(0, END)
                cargoEntry.delete(0, END)
                qtyEntry.delete(0, END)
                clientEntry.delete(0, END)
                doaEntry.delete(0, END)
                dodEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id cannot be duplicated', parent=screen)
            return
        # to fitch data into treeview
        query = 'SELECT * FROM (vessel)'
        mycurs.execute(query)
        fetched_data = mycurs.fetchall()
        vessel_table.delete(*vessel_table.get_children())
        for data in fetched_data:
            data_list = list(data)
            vessel_table.insert('', END, values=data_list)


def connect_database():
    global usernamentry, passwordentry

    def connect():
        global mycurs, con

        try:
            if usernamentry.get() == '' or passwordentry.get() == '':
                messagebox.showerror('Error', 'Fields cannot be empty')
                return
            if usernamentry.get() == 'Hicham' and passwordentry.get() == '1234':
                try:
                    bd_exists = False
                    if 'Operations.db' in os.listdir():
                        bd_exists = True

                    con = sqlite3.connect('Operations.db')
                    mycurs = con.cursor()
                    if not bd_exists:
                        # Create the vessel table
                        create_table_query = "create table if not exists vessel(vid integer not null primary key," \
                                             "name text varchar(30),flag text varchar(25),imo integer varchar(7)" \
                                             "cargo text varchar(12),qty integer varchar(7), client text varchar(10)," \
                                             "doa date varchar(14), dod date varchar(10))"
                        mycurs.execute(create_table_query)
                        con.commit()
                except Exception as e:
                    messagebox.showerror('Error', f'An error occurred {e}')
                    return
            else:
                messagebox.showerror('Error', 'The username or the password is wrong')
                return

            connectWindow.destroy()
            addVessel.config(state=NORMAL)
            searchVessel.config(state=NORMAL)
            updateVessel.config(state=NORMAL)
            showVessel.config(state=NORMAL)
            exportVessel.config(state=NORMAL)
            deleteVessel.config(state=NORMAL)
            connectButton.config(state=DISABLED)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred {e}')

    connectWindow = Toplevel()
    connectWindow.geometry('420x160+825+140')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)

    usernamelabel = Label(connectWindow, text='User Name', font=('arial', 14, 'bold'))
    usernamelabel.grid(row=0, column=0, padx=18, pady=10)
    usernamentry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernamentry.grid(row=0, column=1, padx=30, pady=10)
    usernamentry.focus()

    passwordlabel = Label(connectWindow, text='Password', font=('arial', 14, 'bold'))
    passwordlabel.grid(row=1, column=0, padx=18, pady=10)
    passwordentry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordentry.grid(row=1, column=1, padx=30, pady=10)

    connectbutton = ttk.Button(connectWindow, text='Connect', command=connect)
    connectbutton.grid(row=2, columnspan=2, pady=10)


count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]  # s
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    date = time.strftime('%d/%m/%Y')
    current_time = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date:{date}\nTime:{current_time}')
    datetimeLabel.after(300, clock)


# GUI Part Header
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('itft1')

root.geometry('1174x680+0+0')
root.title('Operations Management System')
root.state('zoomed')
root.resizable(False, False)

datetimeLabel = Label(root,
                      font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

s = 'Operations Management System'
sliderLabel = Label(root, text=s, width=30, fg='gray44',
                    font=('arial', 28, 'italic bold'))
sliderLabel.place(x=260, y=0)
slider()

connectButton = ttk.Button(root,
                           text='Connect Database',
                           command=connect_database,
                           state=NORMAL)
connectButton.place(x=1100, y=25)
connectButton.focus()
# GUI Part Left Frame
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logoImage = PhotoImage(file='sh.png')
logoLabel = Label(leftFrame, image=logoImage)
logoLabel.grid(row=0, column=0)

addVessel = ttk.Button(leftFrame, text='Add Vessel', width=25, state=DISABLED, command=toplevel_data)
addVessel.grid(row=1, column=0, pady=17)

searchVessel = ttk.Button(leftFrame, text='Search Vessel', width=25, state=DISABLED, command=toplevel_data)
searchVessel.grid(row=2, column=0, pady=17)

deleteVessel = ttk.Button(leftFrame, text='Delete Vessel', width=25, state=DISABLED, command=delete_vessel)
deleteVessel.grid(row=3, column=0, pady=17)

updateVessel = ttk.Button(leftFrame, text='update Vessel', width=25, state=DISABLED, command=toplevel_data)
updateVessel.grid(row=4, column=0, pady=17)

showVessel = ttk.Button(leftFrame, text='Show Vessel', width=25, state=DISABLED, command=show_vessel)
showVessel.grid(row=5, column=0, pady=17)

exportVessel = ttk.Button(leftFrame, text='Export Data', width=25, state=DISABLED)
exportVessel.grid(row=6, column=0, pady=17)

exitButton = ttk.Button(leftFrame, text='Exit', width=25)
exitButton.grid(row=7, column=0, pady=17)

# GUI Part Left Frame with the Treeview
rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=910, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

vessel_table = ttk.Treeview(rightFrame,
                            columns=('Id', 'Name', 'Flag', 'Imo', 'Cargo', 'Quantity', 'Client', 'D O A', 'D O D'),
                            xscrollcommand=scrollBarX.set,
                            yscrollcommand=scrollBarY.set)
scrollBarX.config(command=vessel_table.xview)
scrollBarY.config(command=vessel_table.yview)

vessel_table.pack(fill='both', expand=1)

vessel_table.heading('Id', text='Id')
vessel_table.heading('Name', text='Name')
vessel_table.heading('Flag', text='Flag')
vessel_table.heading('Imo', text='Imo')
vessel_table.heading('Cargo', text='Cargo')
vessel_table.heading('Quantity', text='Quantity')
vessel_table.heading('Client', text='Client')
vessel_table.heading('D O A', text='D O A')
vessel_table.heading('D O D', text='D O D')

vessel_table.column('Id', width=50, anchor=CENTER)
vessel_table.column('Name', width=150, anchor=CENTER)
vessel_table.column('Flag', width=150, anchor=CENTER)
vessel_table.column('Imo', width=100, anchor=CENTER)
vessel_table.column('Cargo', width=150, anchor=CENTER)
vessel_table.column('Quantity', width=100, anchor=CENTER)
vessel_table.column('Client', width=190, anchor=CENTER)
vessel_table.column('D O A', width=200, anchor=CENTER)
vessel_table.column('D O D', width=200, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview',
                rowheight=38,
                font=('arial', 12, 'bold'),
                foreground='black',
                background='white',
                fieldbackground='red')
style.configure('Treeview.heading',
                font=('arial', 15, 'bold'),
                foreground='gray64',
                background='purple')

vessel_table.config(show='headings')

scrollBarX.pack(fill='x')
scrollBarY.pack(fill='y')

root.mainloop()
