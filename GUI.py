import tkinter as tk
from pathlib import Path
import tkinter.messagebox as messagebox
from tkinter import *
from tkinter import ttk 
import pandas as pd
from datetime import time
from datetime import datetime as dt
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time as sleeper
from selenium.common.exceptions import WebDriverException

username = ""
MeetingTime = []
MeetingId = []
user = [] 

def key_press(event,s):
    if(len(s.get()) > 20):
        s.configure(highlightcolor = "red")
    else:
        s.configure(highlightcolor = "green")

def saveF(window,Nentry,Nlabel,f):
    name = Nentry.get()
    if len(name) <= 20 and len(name) != 0:
        global username 
        username = name
        Nentry.destroy()
        Nlabel.destroy()
        f.destroy()
        MLabel = Label(window , text = "Metting Id" , bg = "white" ,font = ("Times New Roman" , 12) , width = 200 , anchor = "w" )
        TLabel = Label(window , text = "Time",bg = "white" ,font = ("Times New Roman" , 12) , width = 200 , anchor = "w")
        MLabel.place(x = 10 , y = 150)
        TLabel.place(x=10,y=250)
        
        Mentry = tk.Entry(window , bd = 0 , highlightthickness = 2 , highlightcolor = "green" , width = 27)
        Mentry.place(x=315 , y = 155)
        n = tk.StringVar() 
        hourchoosen = ttk.Combobox(window, width = 27, textvariable = n)
        timelist = []
        for i in range(8,19):
            if i <= 11:
                timelist.append(str(i) + " AM")
            else:
                timelist.append(str(i) + " PM")
        hourchoosen['values'] = tuple(timelist)
        hourchoosen.place(x = 315 , y = 255)

        btn = Button(window,text="Add",fg = "white",command = lambda: saveobj(hourchoosen,Mentry),relief = "groove" , width = 20 , bg = "#4285f4" , bd = 0 , height = 1, font = ("Times New Roman" , 20))
        btnR = Button(window,text="Reset",command = lambda: ResetValue(hourchoosen,Mentry),fg = "white"  , relief = "groove" , width = 20 , bg = "#e62017" , bd = 0 , height = 1, font = ("Times New Roman" , 20))
        btn.place(x = 294 , y = 355)
        btnR.place(x=0,y = 355)         
    else:
        l = Label(window,text = "The name should be less than 20 character", fg = "black" , bg = 'white', font = ("Times New Roman" , 15) , width = 200, anchor = 'w')
        l.place(x = 10,y=220)


def makenewtimetable():
    window = tk.Tk()
    window.title("Attendance Portal")
    window.geometry('600x400')
    window.resizable(False,False)
    window.configure(bg = 'white')
    Wlabel = Label(window,text = "Welcome to the Portal" , fg = "white" , bg = '#4285f4', font = ("Times New Roman" , 25) , width = 500 , anchor = 'w' , height = 3)
    Wlabel.place(x=0,y=0)
    Nlabel = Label(window , text = "Name(will be used while login):" , fg = "black" , bg = 'white', font = ("Times New Roman" , 15) , width = 200, anchor = 'w')
    Nlabel.place(x=10,y=150)
    f = Frame(window , bg = "white" , bd = 0 , width = 100 , height = 100) 
    f.place(x = 500 , y = 155)
    Nentry = tk.Entry(window , bd = 0 , highlightthickness = 2 , highlightcolor = "green" , width = 20)
    Nentry.insert(0,"Required Once")
    Nentry.place(x = 315 , y = 155)
    Nentry.bind('<Key>' , lambda a : key_press(a,Nentry))
    btnSave = Button(f,text="Save",command = lambda: saveF(window,Nentry,Nlabel,f) , fg = "white"  , relief = "groove" , width = 10 , bg = "#4285f4" , bd = 0 , height = 1, font = ("Times New Roman" , 10))
    btnSave.pack(side = BOTTOM)
    window.mainloop()

def ResetValue(times , meeting):
    times.delete(0, 'end')
    times.insert(0, "")
    meeting.delete(0,'end')
    meeting.insert(0,"")

def saveobj(times,meeting):
    if(len(times.get()) != 0 and len(meeting.get()) != 0):
        MeetingI = meeting.get()
        MeetingT = times.get()
        MeetingT = MeetingT[:2].replace(" ", "")
        global MeetingId , MeetingTime,username,user
        MeetingId.append(MeetingI)
        MeetingTime.append(MeetingT)
        user.append(username)
        messagebox.showinfo("Saved Value", "Time: {} \nMeeting Id: {}".format(times.get() , MeetingI))
        ResetValue(times,meeting)

def runclock():
    df = pd.read_csv("data.csv")
    df.sort_values(by = ['Meeting Time'])
    window = tk.Tk()
    window.geometry('600x400')
    window.configure(bg = 'white')
    window.resizable(False,False)
    names = df["Username"][0]
    Wlabel = Label(window,text = "Username: {}".format(names) , fg = "white" , bg = '#4285f4', font = ("Times New Roman" , 25) , width = 20 , anchor = 'w' , height = 1)
    Wlabel.grid(row = 0 , column = 0 , pady = (0,1))
    window.title("Classes Scheduler")
    makeframe(df,window)
    window.after(1000, lambda : makeframe(df,window)) 
    window.mainloop()

def openchrome(Id,name):
    driver = webdriver.Chrome('./chromedriver')
    SStart = "https://meet.teamlink.co/room/"
    SID = str(Id)
    SEnd = "?i=true&fbclid=IwAR2z9qFjTIJOnMSgJZNs9Kt4R2Ru-v17ZaqTfhONLeLoEb5rdBKbM-QYNaI"
    s = SStart + SID + SEnd  
    driver.get(s)
    sleeper.sleep(10)
    inputRoll = driver.find_element_by_css_selector("input.ant-input.msg-input.false")
    text = inputRoll.text
    inputRoll.send_keys(str(name))
    checkBox = driver.find_elements_by_css_selector("input.ant-checkbox-input")
    for i in checkBox:
        text = i.text
        if i != checkBox[0]:
            i.click()
    inputElement = driver.find_elements_by_css_selector("div.button-large.undefined")
    for i in inputElement:
        text = i.text
        if text == "OK":
            i.click()
            while True:
                try:
                    driver.title
                except WebDriverException:
                    break

def openchromebtn(Id,name,i,windowopen):
    windowopen[i] = False
    openchrome(Id,name)

def makeframe(df,window):
    MeetingId = list(df['Meeting Id'])
    MeetingTime = list(df['Meeting Time'])
    username = list(df['Username'])
    done = [True for i in range(len(username))]
    color = ['#72c419' , '#ffcc33' , '#ff9900','#cc3333','#4075e1']
    windowopen = [True for i in range(len(username))]
    for Id,Time,i,status in zip(MeetingId,MeetingTime,range(len(MeetingTime)),done):
        if status:
            Time = time(Time,0,0,0)
            system_time = dt.now().time()
            dateTimeA = datetime.datetime.combine(datetime.date.today(), Time)
            dateTimeB = datetime.datetime.combine(datetime.date.today(), system_time)
            Time_remaing = (dateTimeA - dateTimeB).total_seconds()
            f = Frame(window,bg = color[i%len(color)], bd = 0 , width = 600)
            s = "Meeting Id: {}".format(Id)
            n = Time_remaing
            hour = n // 3600
            n %= 3600
            minutes = n // 60
            n %= 60
            seconds = n 
            s1 = "Time Remaining: {} Hour {} Minutes {} Seconds".format(int(hour),int(minutes),int(seconds))
            l = Label(f,fg = "white" , bg = color[i%len(color)] , text = s , anchor = 'w' , width = 49, height = 1,font = ("Times New Roman" , 15))
            if Time_remaing > 0 :
                l1 = Label(f,fg = "white" , bg = color[i%len(color)] , text = s1 , anchor = 'w' , width = 50, height = 1,font = ("Times New Roman" , 10))
            else:
                windowopen[i] = False
                l1 = Label(f,fg = "white" , bg = color[i%len(color)] , text = "Completed" , anchor = 'w' , width = 100, height = 1,font = ("Times New Roman" , 10))
           
            l.grid(row = 0 , column = 0 , sticky = W , padx = (0,0) , pady = (0,0))
            l1.grid(row = 1 , column = 0 , sticky = W , padx = (0,0) , pady = (0,0))

            if Time_remaing > 0 :
                btn = Button(f,text="Go",command = lambda: openchromebtn(Id,username[0],i,windowopen) , fg = color[i%len(color)]  , relief = "groove" , bg = "white" , bd = 0 , font = ("Times New Roman" , 20))              
                btn.grid(row = 0 , column = 1 , columnspan = 2 , sticky = N+W+E+S , padx = (0,0) , pady = (0,0))
            
            f.grid(row = i+1 , column = 0 ,pady = (1,1), sticky = W)    
            if Time_remaing <= 300 and windowopen[i] and Time_remaing > 0:
                windowopen[i] = False
                openchrome(Id,username[0])
    if True in done:
        window.after(1000, lambda : makeframe(df,window)) 

def timetable(w):
    w.destroy()
    makenewtimetable()
    if len(MeetingId) != 0:
        df = pd.DataFrame(list(zip(MeetingId , MeetingTime,user)) , columns = ['Meeting Id' , 'Meeting Time','Username'])
        df.to_csv('data.csv' , index=False)
        runclock()

def destroyer(w):
    w.destroy()
    runclock()

def main():
    global MeetingTime , MeetingId , username , user
    my_file = Path("data.csv")
    if my_file.is_file():
        window = tk.Tk()
        window.configure(bg = "white")
        window.geometry("600x400")
        l = Label(window,text = "Time Table File Detected. Create New ?" , fg = "white" , bg = '#4285f4', font = ("Times New Roman" , 25) , width = 500 , anchor = 'w' , height = 3)
        l.pack(side = TOP)
        fs = Frame(window,bg = "white", bd = 0 , width = 600,height = 150)
        f = Frame(window,bg = "white", bd = 0 , width = 600)
        btnYes = Button(f,text="Yes",command = lambda : timetable(window), fg = "white"  , relief = "groove" , width = 10 , bg = "#4285f4" , bd = 0 , height = 1, font = ("Times New Roman" , 20))
        btnNo = Button(f,text="No",command = lambda : destroyer(window) , fg = "white"  , relief = "groove" , width = 10 , bg = "#e62017" , bd = 0 , height = 1, font = ("Times New Roman" , 20))
        btnYes.pack(side = LEFT , padx = (10,10))
        btnNo.pack(side = LEFT)
        fs.pack(side = TOP)
        f.pack(side = TOP)
        window.mainloop()
    else:
        window = tk.Tk()
        timetable(window)
            

if __name__ == '__main__':
    main()