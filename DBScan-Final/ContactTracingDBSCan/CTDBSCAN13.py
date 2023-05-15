from datetime import datetime, timedelta
import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from sklearn.cluster import DBSCAN
import mysql.connector
from mysql.connector import Error
import calendar
import serial
import schedule
from dateutil.relativedelta import relativedelta
import threading
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

root = Tk()
root.title("Contact Tracing")
root.resizable(False, False)
root.geometry("1440x800") #edit window

global is_header  
global is_home
global rfid_code
global temp
global arport
arport = "COM6"
temp = ""
rfid_code = ""
is_home = False
is_header = False

# creating widgets
# myLabel = Label(root, text='Hello World!') #for text
# for bisu image
image = Image.open("background.png")
resize_image = image.resize((800, 850))# edit background 
my_img = ImageTk.PhotoImage(resize_image)  # for images
my_img_label = Label(image=my_img)

# for bisu logo
logo = Image.open("logonobg.png")
logo_label = ImageTk.PhotoImage(logo)  # for images
logo_image = Label(image=logo_label)
# logo = image.resize((200, 200))

# text labels
myLabel = Label(root, text='BISU\nContact Tracing', font=('Times', 35))  # for text

# grouplabel = Label(root, text='Group 8', font = ('Times',16)) #for text

def sql_connection():
    global cursor
    global connection
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='contact_tracer',
                                             user='root',
                                             password='123456',
                                             port='3306')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

    except Error as e:
        print("Error while connecting to MySQL", e)

def header():
    global header_logo
    header_logo = ImageTk.PhotoImage(Image.open("logonobg.png"))  # for images
    header_logo_label = Label(image=header_logo)
    header_logo_label.pack(side="left", anchor="nw", padx=(450, 0))

    header_logo_label = Label(root, text='Bohol Island State University', font=('Times', 25))  # for text
    header_logo_label.pack(anchor="n", pady=30, side="left")
    header_logo_address_label = Label(root, text='Tagbilaran City Bohol', font=('Times', 20))  # for text
    header_logo_address_label.place(x=600, y=70)

    separator = ttk.Separator(root, orient='horizontal')
    separator.place(relx=0, rely=0.22, relwidth=1, relheight=1)


def start_program():
    global rfid
    global rfid_code
    global scan_button
    global is_home
    global rfid_pic
    global start_label
    global rfid_image_label

    global from_trace
    global is_header
    global temp
    temp = ""

    if not is_header:
        header()
        is_header = True

    start_label = Label(root, text="Please Scan RFID...", font=('Times', 30))
    start_label.place(x=580, y=140)

    rfid = Image.open("RFIDnobg.png")
    rfid_resized = rfid.resize((500, 500))
    rfid_pic = ImageTk.PhotoImage(rfid_resized)
    rfid_image_label = Label(image=rfid_pic)
    rfid_image_label.place(x=500, y=220)



    rfid_thread = threading.Thread(target = scan_id)#threading
    root.after(500, rfid_thread.start())
    # root.after(500, scan_id)

def admin_program():
    global contact_tracing_button
    global monitoring_button
    global exit_button
    global admin_label
    admin_label = Label(root, text="Welcome BISU Admin...", font=('Times', 30))
    admin_label.place(x=565, y=140)

    contact_tracing_button = Button(root, text="Contact Tracing", padx=10, pady=10, font=('Times', 30),
                                command=clear_start_contact_tracing)
    contact_tracing_button.place(x=585, y=300)

    monitoring_button = Button(root, text="Entrance Monitoring", padx=10, pady=10, font=('Times', 30),
                           command=clear_start_entrance_monitoring)
    monitoring_button.place(x=550, y=400)

    exit_button = Button(root, text="Exit", padx=10, pady=10, font=('Times', 30), command=exit_admin)
    exit_button.place(x=680, y=500)

def exit_admin():
    admin_label.destroy()
    monitoring_button.destroy()
    contact_tracing_button.destroy()
    exit_button.destroy()
    start_program()

def entrance_monitoring():
    global name_label
    global name_entry
    global trace_button
    global back_button2
    global traced_frame1
    global date_label
    global date_entry

    date_label = Label(root, text="Enter Date: ", font=('Times', 25))
    date_label.place(x=760, y=195)

    date_entry = ttk.Entry(root, width=16, font=('Times', 25))
    date_entry.place(x=920, y=195)

    trace_button = Button(root, text="Enter",padx=2, pady=2, font=('Times', 16), command=get_entrance_monitoring)
    trace_button.place(x=1206, y=195)

    traced_frame1 = LabelFrame(root, text="Entrance Monitoring", font=('Times', 20))
    traced_frame_canvas = Canvas(traced_frame1)
    traced_frame_canvas.pack(side=LEFT, fill="both", expand="yes")

    myscrollbar = ttk.Scrollbar(traced_frame1, orient="vertical", command=traced_frame_canvas.yview)
    myscrollbar.pack(side=RIGHT, fill="y")

    traced_frame_canvas.configure(yscrollcommand=myscrollbar.set)
    traced_frame_canvas.bind('<Configure>',
                             lambda e: traced_frame_canvas.configure(scrollregion=traced_frame_canvas.bbox('all')))

    myframe = Frame(traced_frame_canvas)
    traced_frame_canvas.create_window((0, 0), window=myframe, anchor="nw")
    traced_frame1.place(x=170, y=250, width=1100, height=500)

    back_button2 = Button(root, text="Back", padx=10, pady=10, font=('Times', 30), command=clear_entrance_monitoring)
    back_button2.place(x=1305, y=700)

    Label(myframe, text="No One").pack()

def get_entrance_monitoring():
    global unique_id
    global tracename
    global tracedate
    global result_monitoring
    clean = False
    if date_entry.get() == "":
        messagebox.showwarning('Error', 'Please Fill in Date!')
    else:
        sql_connection()

        cursor.execute("SELECT NAME,course, transdate,room,temp from logs where DATE(`transdate`)=DATE('"+date_entry.get()+"')")#added course course ,

        result_monitoring = cursor.fetchall()

        if len(result_monitoring) >= 1:
            show_entrance_monitoring()

        if len(result_monitoring) == 0:
            messagebox.showwarning('Error', 'No Data Found!!')

def show_entrance_monitoring():
    global my_tree
    global back_button3
    global date_label
    Date_entry_label = date_entry.get()
    date_entry.destroy()
    date_label.destroy()
    trace_button.destroy()
    back_button2.destroy()
    traced_frame1.destroy()
    prim_key = 0

    date_label = Label(root, text="Enter Date: " + Date_entry_label, font=('Times', 25))
    date_label.place(x=760, y=195)

    my_tree = ttk.Treeview(root)

    my_tree['columns'] = ("Name","Course", "Date", "Room", "Temp")

    # format columns
    my_tree.column("#0", width=0, minwidth=50)
    my_tree.column("Name", anchor=W, width=100, minwidth=100)
    my_tree.column("Course", anchor=W, width=100, minwidth=150)
    my_tree.column("Date", anchor=W, width=300, minwidth=100)
    my_tree.column("Room", anchor=W, width=150, minwidth=150)
    my_tree.column("Temp", anchor=W, width=100, minwidth=150)
    

    # create headings
    my_tree.heading("#0", text="")
    my_tree.heading("Name", text="Name", anchor=W)
    my_tree.heading("Course", text="Course", anchor=W)
    my_tree.heading("Date", text="Date and Time", anchor=W)
    my_tree.heading("Room", text="Room", anchor=W)
    my_tree.heading("Temp", text="Temp", anchor=W)

    for row in result_monitoring:
        my_tree.insert(parent='', index='end', iid=prim_key, text="", values=(row[0], str(row[1]), row[2], str(row[3]),str(row[4])))
        prim_key += 1
        # my_tree.insert(parent='', index='end', iid=prim_key, text="", values=(row[0], str(row[1]), row[2], str(row[3])))
        # prim_key += 1

    my_tree.place(x=170, y=250, width=1100, height=500)

    back_button3 = Button(root, text="Back",  padx=10, pady=10, font=('Times', 30), command=clear_get_entrance_monitoring)
    back_button3.place(x=1305, y=700)

def scan_id():
    global admin_rfid
    admin_rfid = '0001093604'
    global rfid_code
    try:
        arduino = serial.Serial(arport, timeout=5)
        print("Connected RFID")
    except:
        print("Please Check Port")

    arduino.baudrate = 9600
    arduino.port = arport
    rfid_obtained = False

    while not rfid_obtained:
        sent = arduino.write(b'B')
        packet = arduino.readline()
        rfid_code = packet.decode('utf-8')
        print("SCANNING RFID")
        if len(rfid_code) > 3:
            rfid_obtained = True

    if (rfid_code != None and len(rfid_code) > 3):
        print(rfid_code)
        str_rfid_code = rfid_code.strip()
        if str_rfid_code == admin_rfid:
            print("ADMIN ACCESSED")
            clear_start_admin_program()
        else:
            sql_connection()
            cursor.execute("SELECT * from users where rfid='" + rfid_code + "'")
            result = cursor.fetchall()

            if len(result) >= 1:
                start_show_thread = threading.Thread(target=clear_start_show_details)  # threading
                start_show_thread.start()
                root.after(500, lambda: start_show_thread.join())
                # clear_start_show_details()
            else:
                clear_start_register()

def clear_start_admin_program():
    start_label.destroy()
    # scan_button.destroy()
    rfid_image_label.destroy()
    admin_program()

def clear_front_page():
    startButton.destroy()
    myLabel.destroy()
    logo_image.destroy()
    my_img_label.destroy()
    start_program()
    

def clear_start_contact_tracing():
    is_home = False
    admin_label.destroy()
    monitoring_button.destroy()
    contact_tracing_button.destroy()
    exit_button.destroy()
    contact_tracing()

def clear_get_entrance_monitoring():
    date_label.destroy()
    date_entry.destroy()
    my_tree.destroy()
    back_button3.destroy()
    admin_program()

def clear_entrance_monitoring():
    is_home = False
    date_label.destroy()
    date_entry.destroy()
    trace_button.destroy()
    back_button2.destroy()
    traced_frame1.destroy()
    admin_program()

def clear_start_entrance_monitoring():
    admin_label.destroy()
    monitoring_button.destroy()
    contact_tracing_button.destroy()
    exit_button.destroy()
    entrance_monitoring()

def clear_start_register():
    global is_home
    is_home = False
    start_label.destroy()
    rfid_image_label.destroy()
    # scan_button.destroy()
    register()
    # show_details()

def clear_start_show_details():
    global scan_temp_label
    global is_home
    is_home = False
    start_label.destroy()
    rfid_image_label.destroy()
    # scan_button.destroy()
    show_details()
    scan_temp_label = Label(root, text="Please Scan Temperature", font=('Times', 30))
    scan_temp_label.place(x=560, y=140)
    # temp_thread = threading.Thread(target=scan_temp)#threading
    # temp_thread.start()
    # root.after(500, lambda: temp_thread.join())
    root.after(500, scan_temp)

def clear_contact_tracing():
    global stop_thread
    stop_thread = False
    global is_home
    is_home = False
    name_label.destroy()
    name_entry.destroy()
    date_label.destroy()
    date_entry.destroy()
    trace_button.destroy()
    back_button1.destroy()
    traced_frame1.destroy()
    admin_program()

def clear_trace():
    name_label.destroy()
    name_entry.destroy()
    date_label.destroy()
    date_entry.destroy()
    trace_button.destroy()
    back_button1.destroy()
    traced_frame1.destroy()
    for widgets in traced_frame.winfo_children():
        widgets.destroy()

def clear_contact_traced():
    for widgets in traced_frame.winfo_children():
        widgets.destroy()
    name_label.destroy()
    name_entry.destroy()
    trace_button.destroy()
    traced_frame.destroy()
    back_button1.destroy()
    traced_frame_canvas.destroy()
    traced_frame1.destroy()
    back_button2.destroy()
    date_label.destroy()
    date_entry.destroy()
    label_email.destroy()
    entry_email.destroy()
    button_send.destroy()
    contact_tracing_list_final.clear()
    admin_program()

def trace_checker():
    global unique_id
    global tracename
    global tracedate
    global time_id
    global dateEntry
    global nameEntry
    clean = False
    if name_entry.get() == "" or date_entry.get() == "":
        messagebox.showwarning('Error', 'Please Fill in Name and Date!')
    else:
        sql_connection()
        # SELECT id, DATE_FORMAT(transdate, '%Y-%m-%d %H:%i') AS `formated_date`, DATE_FORMAT(transdate, '%Y-%m-%d') AS `newdate_date`, DATE(transdate)
        # FROM contact_tracer.logs
        # WHERE `name` = "Gesite, George Jr C." AND DATE(transdate) BETWEEN DATE_SUB("2023-04-26", INTERVAL 1 DAY) AND "2023-04-26";

        # INSERT INTO contact_tracer.logs (id, name, transdate, epoch, room, temp, course)
        # VALUES 
        # (1, 'John Doe', '2023-04-17', 1647633600, '101', 25.6, "BSCPE4A");
        dateEntry = date_entry.get()
        nameEntry = name_entry.get()

        # cursor.execute("SELECT id, DATE_FORMAT (transdate, '%Y-%m-%d %H:%i') AS `formated_date`,DATE_FORMAT(transdate, '%Y-%m-%d') AS `newdate_date`, date(transdate) from `logs` where `name`='"+name_entry.get()+"' and date(transdate)='"+date_entry.get()+"'")
        # cursor.execute("SELECT id, DATE_FORMAT (transdate, '%Y-%m-%d %H:%i') AS `formated_date`,DATE_FORMAT(transdate, '%Y-%m-%d') AS `newdate_date`, date(transdate) from `logs` where `name`='"+name_entry.get()+"' and AND DATE(transdate) BETWEEN DATE_SUB('"+dateEntry+"', INTERVAL 1 DAY) AND '"+dateEntry+"'")
        cursor.execute("SELECT id, DATE_FORMAT(transdate, '%Y-%m-%d %H:%i') AS `formated_date`, DATE_FORMAT(transdate, '%Y-%m-%d') AS `newdate_date`, DATE(transdate) from `logs` where `name`='"+name_entry.get()+"' AND DATE(transdate) BETWEEN DATE_SUB('"+dateEntry+"', INTERVAL 2 DAY) AND '"+dateEntry+"'")

        result = cursor.fetchall()

        if len(result) >= 1:
            for row in result:
                temp_id = row[0] #id    
                time_id = row[1] #formated date YY MM DD HH MM
                checkdate = row[2] #newdate YY MM DD
                tracedate = row[3] #transdate YY MM DD 
                unique_id =temp_id
                tracename = name_entry.get()
                trace()
            contacttracing_output()

        elif len(result) == 0:
            messagebox.showwarning('Error', 'No Name and Date Found!!')

def contact_tracing():
    global name_label
    global name_entry
    global trace_button
    global back_button1
    global traced_frame1
    global date_label
    global date_entry

    from_trace = True

    name_label = Label(root, text="Enter Name: ", font=('Times', 25))
    name_label.place(x=80+180, y=195)

    name_entry = ttk.Entry(root, width=18, font=('Times', 25))
    name_entry.place(x=230+200, y=195)

    date_label = Label(root, text="Enter Date: ", font=('Times', 25))
    date_label.place(x=490+270, y=195)

    date_entry = ttk.Entry(root, width=16, font=('Times', 25))
    date_entry.place(x=630+290, y=195)

    trace_button = Button(root, text="Trace", padx=2, pady=2,font=('Times', 16), command=trace_checker)
    trace_button.place(x=1206, y=195)

    traced_frame1 = LabelFrame(root, text="People Subject to Contact Tracing", font=('Times', 20))
    traced_frame_canvas = Canvas(traced_frame1)
    traced_frame_canvas.pack(side=LEFT, fill="both", expand="yes")

    myscrollbar = ttk.Scrollbar(traced_frame1, orient="vertical", command=traced_frame_canvas.yview)
    myscrollbar.pack(side=RIGHT, fill="y")

    traced_frame_canvas.configure(yscrollcommand=myscrollbar.set)

    traced_frame_canvas.bind('<Configure>',
                             lambda e: traced_frame_canvas.configure(scrollregion=traced_frame_canvas.bbox('all')))

    myframe = Frame(traced_frame_canvas)
    traced_frame_canvas.create_window((0, 0), window=myframe, anchor="nw")
    traced_frame1.place(x=170, y=250, width=1100, height=450)
    #back button contact tracing
    back_button1 = Button(root, text="Back", padx=10, pady=10, font=('Times', 30), command=clear_contact_tracing)
    back_button1.place(x=1305, y=700)

    Label(myframe, text="No One").pack()

contact_tracing_list_final =[] #final list of contact tracing

def trace():
  
    trace_button.destroy()
    global final_names


    sql_connection()

    # cursor.execute("SELECT id, NAME, epoch, room,course, DATE_FORMAT(transdate, '%Y-%m-%d %H:%i') AS transdate, DATE(transDate),temp,phone, address FROM LOGS")
    # cursor.execute("SELECT id,name,epoch,room,DATE(transdate) FROM logs")
    cursor.execute("SELECT id, NAME, epoch, room, course, DATE_FORMAT(transdate, '%Y-%m-%d %H:%i') AS transdate, DATE(transDate), temp, phone, address FROM LOGS WHERE DATE(transdate) BETWEEN DATE_SUB('"+dateEntry+"', INTERVAL 2 DAY) AND '"+dateEntry+"'")


    result = cursor.fetchall()

    all_id = [] #id
    all_name = []#name
    all_date_int = [] #epoch
    all_time_int = [] #room
    all_course =[]
    all_date = [] #date
    all_date_only =[]
    all_temp_int = [] #temp
    all_phone = []
    all_address = []

    for id, name, date_int, time_int,course, transdate, transDate,temp_int, phone, address in result:
        all_id.append(id)
        all_name.append(name)
        all_date_int.append(date_int)
        all_time_int.append(time_int)
        all_course.append(course)
        all_date.append(transdate)
        all_date_only.append(transDate)
        all_temp_int.append(temp_int)
        all_phone.append(phone)
        all_address.append(address)
    dic = {'id': all_id, 'datetime': all_date_int, 'room': all_time_int, 'name': all_name,'course': all_course, 'trans': all_date, 'transD':all_date_only,'temp': all_temp_int,'phone':all_phone, 'address': all_address } 
    df = pd.DataFrame(dic)
    connection.close()
    df.to_csv('exported.csv')
    cursor.close()

    df = pd.read_csv('exported.csv')

    def get_infected_names(unique_id):
        unique_id = int(unique_id)
        name_room = df[df['id'] == int(unique_id)]['room'].item() 
        epsilon = 1
        model = DBSCAN(eps=epsilon, min_samples=2, metric='haversine').fit(df[['room', 'datetime']])
        df['cluster'] = model.labels_.tolist()
        input_name_clusters = []
        for i in range(len(df)):
            if df['id'][i] == unique_id:
                if df['cluster'][i] in input_name_clusters:
                    pass
                else:
                    input_name_clusters.append(df['cluster'][i])

        infected_id = []
        for cluster in input_name_clusters:
            if cluster != -1:
                ids_in_cluster = df.loc[df['cluster'] == cluster, 'id']
                for i in range(len(ids_in_cluster)):
                    member_id = ids_in_cluster.iloc[i]
                    if (member_id not in infected_id) and (member_id != unique_id):
                        infected_id.append(member_id)
                    else:
                        pass
        final_infected_names = []
        for i in range(len(infected_id)):
            if (df[df['id'] == int(infected_id[i])]['transD'].item()) == tracedate.strftime("%Y-%m-%d"): #mo check if same day
                if (df[df['id'] == int(infected_id[i])]['name'].item()) != tracename:
                    if (df[df['id'] == int(infected_id[i])]['room'].item()) == name_room:
                        if not df[df['id'] == infected_id[i]]['name'].item() in final_infected_names:
                            name = df[df['id'] == infected_id[i]]['name'].item()
                            trans = df[df['id'] == infected_id[i]]['trans'].item()
                            trans_dt = datetime.strptime(trans, "%Y-%m-%d %H:%M")
                            time_id2 = datetime.strptime(time_id, "%Y-%m-%d %H:%M")
                            time_diff = abs(trans_dt - time_id2)
                            if time_diff <= timedelta(minutes=30):
                                room = df[df['id'] == infected_id[i]]['room'].item()
                                temp = df[df['id'] == infected_id[i]]['temp'].item()
                                course = df[df['id'] == infected_id[i]]['course'].item()
                                Phone = df[df['id'] == infected_id[i]]['phone'].item()
                                Address = df[df['id'] == infected_id[i]]['address'].item()
                                final_infected_names.append((name, trans, room, temp,course,Phone, Address))
                                contact_tracing_list_final.append((name, trans, room, temp,course,Phone, Address))
    
        return final_infected_names


    i_name = get_infected_names(unique_id)

def contacttracing_output():
    final_names = contact_tracing_list_final
    print(len(contact_tracing_list_final))
    pdf_filename = create_pdf(final_names)
    global myframe
    global traced_frame
    global my_button
    global traced_frame_canvas
    global back_button2
    global label_email
    global entry_email
    global button_send

    for widgets in traced_frame1.winfo_children():
        widgets.destroy()
    traced_frame = LabelFrame(root, text="People Subject to Contact Tracing", font=('Times', 20))
    traced_frame_canvas = Canvas(traced_frame)
    traced_frame_canvas.pack(side=LEFT, fill="both", expand="yes")

    myscrollbar = ttk.Scrollbar(traced_frame, orient="vertical", command=traced_frame_canvas.yview)
    myscrollbar.pack(side=RIGHT, fill="y")

    traced_frame_canvas.configure(yscrollcommand=myscrollbar.set)

    traced_frame_canvas.bind('<Configure>',
                             lambda e: traced_frame_canvas.configure(scrollregion=traced_frame_canvas.bbox('all')))

    myframe = Frame(traced_frame_canvas)
    traced_frame_canvas.create_window((0, 0), window=myframe, anchor="nw")

    traced_frame.place(x=170, y=250, width=1100, height=450)
    back_button2 = Button(root, text="Back", padx=10, pady=10, font=('Times', 30), command=clear_contact_traced)
    back_button2.place(x=1305, y=700)

    label_email = Label(root, text="Email List:", font=('Times', 25))
    label_email.place(x=260+100+25, y=720)

    entry_email = ttk.Entry(root, font=('Times', 25), width=25)
    entry_email.place(x=360+100+80, y=720)
    button_send = Button(root, text="Send List", padx=2, pady=2, font=('Times', 16), command=send_email)
    button_send.place(x=800+100+80, y=720)

    if len(final_names) > 0:
        for i in final_names:
            my_button = Button(myframe, text=f"Name: {i[0]}     DateTime: {i[1]}     Temp: {i[3]}      \nRoom: {i[2]}      Course: {i[4]}", width=75, font=('Times', 20), command=lambda button_text=i[0]: click_name(button_text)).pack()

    else:
        Label(myframe, text="No One", font=('Times', 15)).pack()


def click_name(text):
    new = Toplevel(root)
    new.title("Description")
    new.resizable(False, False)
    new.geometry("1200x400")
    # Create a Label in New window
    Label(new, text="User Details", font=('Helvetica 17 bold')).pack(pady=30)

    global clicked_image
    global clicked_image_label

    sql_connection()

    from_db = []
    cursor.execute("SELECT * FROM users where `name` = '"+text+"'")  # add where clause
    results = cursor.fetchall()
    connection.close()
    cursor.close()
    for result in results:
        result = list(result)
        from_db.append(result)
        clicked_image = result[6] #column 6 for image

        convert_data(clicked_image, "user.jpg")

    columns = ["id", "rfid", "name", "course", "address","phone","image"]
    df = pd.DataFrame(from_db, columns=columns)

    clicked_rfid_text = df[df['name'] == text]['rfid'].item()
    clicked_name_text = text
    clicked_course_text = df[df['name'] == text]['course'].item()
    clicked_address_text = df[df['name'] == text]['address'].item()
    clicked_phone_text =df[df['name'] == text]['phone'].item()
    # print(clicked_address_text + " " + clicked_name_text + " " + clicked_course_text + " " + clicked_rfid_text)

    clicked_rfid = Image.open("user.jpg")
    clicked_rfid_resized = clicked_rfid.resize((300, 300))
    clicked_image = ImageTk.PhotoImage(clicked_rfid_resized)
    clicked_image_label = Label(new,image=clicked_image)
    clicked_image_label.place(x=80, y=80)

    clicked_rfid_label = Label(new, text="RFID: ", font=('Times', 18))
    clicked_rfid_label.place(x=450, y=100)
    clicked_rfid = Label(new, text=clicked_rfid_text, font=('Times', 18))
    clicked_rfid.place(x=550, y=100)
    clicked_name_label = Label(new, text="Name: ", font=('Times', 18))
    clicked_name_label.place(x=450, y=140)
    clicked_name = Label(new, text=clicked_name_text, font=('Times', 18))
    clicked_name.place(x=550, y=140)
    clicked_course_label = Label(new, text="Course: ", font=('Times', 18))
    clicked_course_label.place(x=450, y=180)
    clicked_course = Label(new,text=clicked_course_text, font=('Times', 18))
    clicked_course.place(x=550, y=180)
    clicked_address_label = Label(new, text="Address: ", font=('Times', 18))
    clicked_address_label.place(x=450, y=220)
    clicked_address = Label(new, text=clicked_address_text, font=('Times', 18))
    clicked_address.place(x=550, y=220)
    clicked_phone_label = Label(new, text="phone: ", font=('Times', 18))
    clicked_phone_label.place(x=450, y=260)
    clicked_phone = Label(new, text=clicked_phone_text, font=('Times', 18))
    clicked_phone.place(x=550, y=260)



def create_pdf(array):
    # Create a new PDF file
    global pdf_filename
    pdf_filename = "Contact_Tracing.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    story = []

    # Set the font sizes
    header_font_size = 10
    title_font_size = 16
    content_font_size = 12

    # Header
    header_style = ParagraphStyle(name='Header', fontSize=header_font_size, leading=14, alignment=TA_CENTER,fontName='Helvetica-Bold')
    header_text = "RFID-BASED ENTRANCE MONITORING SYSTEM WITH TEMPERATURE SCANNER AND COVID-19 CONTACT TRACING USING MACHINE LEARNING"
    header_paragraph = Paragraph(header_text, header_style)
    story.append(header_paragraph)

    # Title
    title_style = ParagraphStyle(name='Title', fontSize=title_font_size, leading=18, spaceAfter=10, alignment=TA_CENTER,fontName='Helvetica-Bold')
    title_text = "CONTACT TRACING LIST"
    title_paragraph = Paragraph(title_text, title_style)
    story.append(title_paragraph)

    # Name of Positive Cased Person and Date of Contact Tracing
    name_style = ParagraphStyle(name='Name', fontSize=content_font_size, leading=14, spaceAfter=5)
    name_text = "Positive Cased Person: " + nameEntry
    name_paragraph = Paragraph(name_text, name_style)
    story.append(name_paragraph)

    date_style = ParagraphStyle(name='Date', fontSize=content_font_size, leading=14, spaceAfter=5)
    date_text = "Date of Contact Tracing: " + dateEntry
    date_paragraph = Paragraph(date_text, date_style)
    story.append(date_paragraph)

    # Write the contents of the array to the PDF
    content_style = ParagraphStyle(name='Content', fontSize=content_font_size, leading=14, spaceAfter=5)
    for content in array:
        content_text = str(content)  # Convert the tuple element to a string
        content_paragraph = Paragraph(content_text, content_style)
        story.append(content_paragraph)

    doc.build(story)

    return pdf_filename

def send_email():
    recipient_email = entry_email.get()
    # Email settings
    sender_email = "bisucontacttracing2023@gmail.com"
    sender_password = "lpvgdvstrligcmdn"

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Contact Tracing List Update"

    # Attach the PDF file to the email
    with open(pdf_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {pdf_filename}")

    message.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
    
    messagebox.showinfo("Email Sent", "The email has been sent successfully.")

def clear_register():
    b2.destroy()
    enter_course_entry.destroy()
    enter_name_entry.destroy()
    enter_address_entry.destroy()
    enter_phone_entry.destroy()
    traced_label.destroy()
    upload_button.destroy()
    enter_name_label.destroy()
    enter_course_label.destroy()
    enter_address_label.destroy()
    enter_phone_label.destroy()
    register_button.destroy()
    start_program()

def register():
    global enter_course_entry
    global enter_name_entry
    global enter_address_entry
    global enter_phone_entry
    global filename
    global traced_label
    global upload_button
    global enter_name_label
    global enter_course_label
    global enter_address_label
    global enter_phone_label
    global register_button
    global rfid_code

    filename = ""
    traced_label = Label(root, text="Register", font=('Times', 40))
    traced_label.place(x=650, y=120)
    upload_button = Button(root, text="Upload Photo", font=('Times', 20), command=upload_photo)
    upload_button.place(x=170+100, y=320)
    enter_name_label = Label(root, text="Name: ", font=('Times', 20))
    enter_name_label.place(x=430+100, y=220+10+50)
    enter_name_entry = ttk.Entry(root, width=45, font=('Times', 20))
    enter_name_entry.place(x=530+100, y=220+50)
    enter_course_label = Label(root, text="Course: ", font=('Times', 20))#edit course year and section
    enter_course_label.place(x=430+100, y=260+10+10+50)
    enter_course_entry = ttk.Entry(root, width=45, font=('Times', 20))
    enter_course_entry.place(x=530+100, y=260+10+10+50)
    enter_address_label = Label(root, text="Address: ", font=('Times', 20))
    enter_address_label.place(x=430+100, y=300+10+10+10+50)
    enter_address_entry = ttk.Entry(root, width=45, font=('Times', 20))
    enter_address_entry.place(x=530+100, y=300+10+10+10+50)
    enter_phone_label = Label(root, text="Phone: ", font=('Times', 20))
    enter_phone_label.place(x=430+100, y=340+10+10+10+10+50)
    enter_phone_entry = ttk.Entry(root, width=45, font=('Times', 20))
    enter_phone_entry.place(x=530+100, y=340+10+10+10+10+50)
    register_button = Button(root, text="Register", font=('Times', 30), command=register_details)
    register_button.place(x=700+100+80, y=450+50)

def upload_photo():
    global img
    global filename
    global b2
    f_types = [('Jpg Files', '*.jpg'),('Jpeg Files', '*.jpeg'),('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if filename:
        upload_image = Image.open(filename)
        resize_img = upload_image.resize((350, 350))
        img = ImageTk.PhotoImage(resize_img)
        b2 = Label(root, image=img)  # using Button
        b2.place(x=100, y=230)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def register_details():
    global rfid_code

    if enter_name_entry.get() == "" or enter_course_entry.get() == "" or enter_address_entry.get() == "" or enter_phone_entry.get() == "":
        messagebox.showwarning('Error', 'Error: Please Fill up Data!')
    else:
        if filename == "":
            messagebox.showwarning('Error', 'Error: Please Add Photo!')
        else:
            try:
                file = convertToBinaryData(filename)
                sql_connection()
                sql = "INSERT INTO users (rfid, name, course, address, phone, image) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (rfid_code, enter_name_entry.get(), enter_course_entry.get(), enter_address_entry.get(), enter_phone_entry.get(), file)
                result = cursor.execute(sql, val)
                connection.commit()
                tkinter.messagebox.showinfo(title="Success!", message="Image and data successfully inserted!")

            except mysql.connector.Error as error:
                tkinter.messagebox.showerror(title="Failed!", message=error)

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                    clear_register()

def clear_show_details():
    image_label.destroy()
    detail_id_label.destroy()
    detail_id.destroy()
    detail_name_label.destroy()
    detail_name.destroy()
    detail_course_label.destroy()
    detail_course.destroy()
    detail_address_label.destroy()
    detail_address.destroy()
    detail_time_label.destroy()
    detail_time.destroy()
    detail_temp_label.destroy()
    detail_temp.destroy()
    detail_room_label.destroy()
    detail_room_entry.destroy()
    # save_button.destroy()
    # scan_temp_button.destroy()
    start_program()

from tkinter import messagebox

def save_details():
    if room_entry == "" or temp_text == "\N{DEGREE SIGN}C":
        messagebox.showwarning('Error', 'Error: Please Fill up Data!')
    else:
        try:
            sql_connection()
            sql = "INSERT INTO logs (name, transdate, epoch, room,temp,course,phone, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (name_text, currentDateAndTime, epoch, room_entry, temp_text, course_text, phone_text, address_text)
            result = cursor.execute(sql, val)
            connection.commit()
            print("Image and data successfully inserted!")
            temp = ""
            rfid_code = ""
            show_success()

        except mysql.connector.Error as error:
            print("Error: ", error)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                clear_show_details()

def show_success():
    success_window = tk.Toplevel()
    success_window.geometry("400x100")
    success_window.title("Success")
    
    success_label = tk.Label(success_window, text="Data has been saved. Thank you!",font=("Times", 16))
    success_label.pack(pady=10)

    # Destroy the success window after 3 seconds (3000 milliseconds)
    success_window.after(3000, success_window.destroy)

def convert_data(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def show_details():
    global rfid_code
    global image
    global image_label
    global name_text
    global course_text
    global currentDateAndTime
    global address_text
    global phone_text
    global temp_text
    global rfid_image_label
    global detail_id_label
    global detail_id
    global detail_name_label
    global detail_name
    global detail_course_label
    global detail_course
    global detail_address_label
    global detail_address
    global detail_time_label
    global detail_time
    global detail_temp_label
    global detail_temp
    global detail_room_label
    global detail_room_entry
    # global save_button
    global epoch
    global temp
    global temp_obtained
    global room_entry
    # global scan_temp_button

    currentDateAndTime = datetime.now()
    t = datetime(currentDateAndTime.year, currentDateAndTime.month, currentDateAndTime.day, currentDateAndTime.hour,
                 currentDateAndTime.minute, currentDateAndTime.second)
    epoch = calendar.timegm(t.timetuple())
    currentTime = currentDateAndTime.strftime("%H:%M:%S")

    now = datetime.now()

    sql_connection()

    from_db = []
    cursor.execute("SELECT * FROM users u WHERE u.rfid = '" + rfid_code + "'") #add where clause
    results = cursor.fetchall()
    connection.close()
    cursor.close()
    for result in results:
        result = list(result)
        from_db.append(result)
        image = result[6]

        convert_data(image, "user.jpg")

    columns = ["id", "rfid", "name", "course", "address" ,"phone","image"]
    df = pd.DataFrame(from_db, columns=columns)

    name_text = df[df['rfid'] == rfid_code]['name'].item()
    course_text = df[df['rfid'] == rfid_code]['course'].item()
    address_text = df[df['rfid'] == rfid_code]['address'].item()
    phone_text = df[df['rfid'] == rfid_code]['phone'].item()

    rfid = Image.open("user.jpg")
    rfid_resized = rfid.resize((350, 350))
    image = ImageTk.PhotoImage(rfid_resized)
    image_label = Label(image=image)
    image_label.place(x=100+200, y=230)

    temp_text = temp#+"\N{DEGREE SIGN}C" for python degress celsius sign
    room_entry = get_room_number(course_text)

    detail_id_label = Label(root, text="RFID: ", font=('Times', 25))
    detail_id_label.place(x=500+40+200, y=180+10+20)
    detail_id = Label(root, text=rfid_code, font=('Times', 25))
    detail_id.place(x=600+40+200, y=180+10+20)
    detail_name_label = Label(root, text="Name: ", font=('Times', 25))
    detail_name_label.place(x=500+40+200, y=220+10+10+20)
    detail_name = Label(root, text=name_text, font=('Times', 25))
    detail_name.place(x=600+40+200, y=220+10+10+20)
    detail_course_label = Label(root, text="Course: ", font=('Times', 25))
    detail_course_label.place(x=500+40+200, y=260+10+10+10+20)
    detail_course = Label(root,text=course_text, font=('Times', 25))
    detail_course.place(x=600+40+20+200, y=260+10+10+10+20)
    detail_address_label = Label(root, text="Address: ", font=('Times', 25))
    detail_address_label.place(x=500+40+200, y=300+10+10+10+10+20)
    detail_address = Label(root, text=address_text, font=('Times', 25))
    detail_address.place(x=600+40+20+200, y=300+10+10+10+10+20)
    detail_time_label = Label(root, text="Time: ", font=('Times', 25))
    detail_time_label.place(x=500+40+200, y=340+10+10+10+10+10+20)
    detail_time = Label(root, text=currentTime, font=('Times', 25))
    detail_time.place(x=600+40+200, y=340+10+10+10+10+10+20)
    detail_temp_label = Label(root, text="Temperature: ", font=('Times', 25))
    detail_temp_label.place(x=500+40+200, y=380+10+10+10+10+10+10+20)
    detail_temp = Label(root, text=temp_text, font=('Times', 25))
    detail_temp.place(x=640+40+20+20+200, y=380+10+10+10+10+10+10+20)
    detail_room_label = Label(root, text="Room: ", font=('Times', 25))
    detail_room_label.place(x=500+40+200, y=420+10+10+10+10+10+10+10+20)
    detail_room_entry = Label(root, text=room_entry, font=('Times', 25))
    detail_room_entry.place(x=600+40+200, y=425+70+20)

def scan_temp():
    global temp
    try:
        arduino = serial.Serial(arport, timeout=5)
        print("Connected TEMP")
    except:
        print("Please Check Port")

    arduino.port = arport
    i = 0
    while i < 3:
        counter = 0
        while True:
            sent = arduino.write(b'A')
            packet = arduino.readline()
            temp = packet.decode('utf-8')
            if len(temp) > 3:
                break
            if counter == 2:
                break
            counter += 1

        if len(temp) > 3:
            break

        if counter == 2:
            break
        i += 1

        if len(temp) > 3:
            break
    
    if (temp != None and len(temp) > 3):
        clear_temp_scan()


def clear_temp_scan():
    image_label.destroy()
    detail_id_label.destroy()
    detail_id.destroy()
    detail_name_label.destroy()
    detail_name.destroy()
    detail_course_label.destroy()
    detail_course.destroy()
    detail_address_label.destroy()
    detail_address.destroy()
    detail_time_label.destroy()
    detail_time.destroy()
    detail_temp_label.destroy()
    detail_temp.destroy()
    detail_room_label.destroy()
    detail_room_entry.destroy()
    # save_button.destroy()
    # scan_temp_button.destroy()
    scan_temp_label.destroy()
    show_details()
    root.after(1500, save_details)

def get_room_number(course_text):
    current_day = datetime.now().strftime("%A")  # Get the current day
    current_time_str = datetime.now().strftime("%I:%M %p")  # Get the current time


    sql_connection()

    # Retrieve the class schedule data from the database
    query = "SELECT day, time, room_number FROM class_schedule WHERE section = %s"
    values = (course_text,)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    # Close the database connection
    cursor.close()
    connection.close()

    closest_time_diff = timedelta.max
    closest_room_number = None

    for row in rows:
        day = row[0]
        time = row[1]
        room_number = row[2]

        if current_day == day:
            class_time = datetime.strptime(time, "%I:%M %p")
            current_time = datetime.strptime(current_time_str, "%I:%M %p")

            time_diff = abs(class_time - current_time)
            if time_diff < closest_time_diff:
                closest_time_diff = time_diff
                closest_room_number = room_number

    return closest_room_number


# button labels
startButton = Button(root, text="Start", padx=10, pady=10, font=('Times', 30), command=clear_front_page)

# puting label into the root
my_img_label.pack(side=LEFT, anchor="w", fill=BOTH)
logo_image.pack(anchor="center", pady=40)
myLabel.pack(anchor="n")
# grouplabel.pack()
startButton.pack(anchor="center", pady=50)

root.mainloop()

# automate scanning of rfid and temp (no more user press) - Worked
# automatically enter room number based on class schedule - Worked
# automatically save - WORKED
# added address and phone to contact tracing list - worked
# can export the contact tracing list -worked
#export contact tracing via email - worked

# lahi na rfid para mo gawas ang entrance monitoring and contact tracing - WORKED
# redesign UI for scanning temp- WORKED
