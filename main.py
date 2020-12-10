#standard GUI library
import numpy as np
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tmsg

#To access the database file
from collections import OrderedDict
import sqlite3 as sq
import json, sys
import matplotlib.pyplot as plt

#Machine Learning Library
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score

from PIL import ImageTk,Image

class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x500')
        self.root.title("CRAIGSLIST")
        self.conStart()
        self.username = StringVar()
        self.password = StringVar()

        #Login Frame
        login_frame = Frame(self.root, bg="Silver")
        login_frame.place(x=0, y=0, width=800, height=50)
        title_login = Label(login_frame, text="LOGIN PAGE", font=("palatino", 25, "bold"),bg="Silver",fg="Blue")
        title_login.pack()

        #Main Frame
        main_frame = Frame(self.root, bd=7, relief=RIDGE)
        main_frame.place(x=5, y=55, width=785, height=450)

        # Username and Password input field
        username_label = Label(main_frame, text="USERNAME", font=("palatino", 15, 'bold'), fg="Blue")
        username_label.grid(row=1, column=1, padx=40, pady=40)
        username_field = Entry(main_frame, textvariable=self.username)
        username_field.grid(row=1, column=2, ipady=7, ipadx=20, padx=40)
        password_label = Label(main_frame, text="PASSWORD", font=("palatino", 15, "bold"), fg="Blue")
        password_label.grid(row=2, column=1, pady=40)
        password_field = Entry(main_frame, textvariable=self.password)
        password_field.grid(row=2, column=2, ipady=7, ipadx=20, padx=40)

        #Login and Registration
        login_button = Button(main_frame, text="LOGIN", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                           relief=SUNKEN, command=self.get)
        login_button.grid(row=3, column=1, ipady=4, ipadx=13, pady=40, padx=40)
        register_button = Button(main_frame, text="REGISTER", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                         relief=SUNKEN, command=self.post)
        register_button.grid(row=3, column=2, ipady=4, ipadx=13, pady=40)
        load = Image.open("ww.png")
        render = ImageTk.PhotoImage(load)
        img = Label(main_frame, image=render)
        img.image = render
        img.grid(row=2, column=3)

    # Entering into the Login page
    def HomeScreen(self):
        root2 = Toplevel(self.root)
        enter = HomePage(root2)
        
    #Creating the Database Table
    def conStart(self):
        con = sq.connect("craig_data.db")
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login(
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )
        """)
        con.commit()
        con.close()
        
    #Putting the Data 
    def post(self):
        a = self.username.get()
        b = self.password.get()
        con = sq.connect("craig_data.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM login")
        data = cursor.fetchall()
        data_imp = OrderedDict(data)
        if (self.username.get() in data_imp.keys()) and (self.password.get() in data_imp.values()):
            self.Info_Error_2()
        elif(self.username.get() =="" or self.password.get() == ""):
            self.Info_Error_3()
        else:
            cursor.execute("INSERT INTO login VALUES(?,?)", (a, b))
            con.commit()
            con.close()
            self.Info_Success_2()
            
    #Getting the data       
    def get(self):
        con = sq.connect("craig_data.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM login")
        data = cursor.fetchall()
        data_imp = OrderedDict(data)
    #To check the condition for login
        if (self.username.get() in data_imp.keys()) and (self.password.get() in data_imp.values()):
            self.success()
        else:
            self.error()

    #Displaying the message if the login is success
    def success(self):
        a = tmsg.showinfo('Login successful', "Thanks For Coming Back")
        if a == 'ok':
            self.HomeScreen()

    #Displaying the message if the login is not successful
    def error(self):
        tmsg.showerror('Error', "Username/Password Not Found/Match")

    #Displaying the message if the Registration is not successful
    def Info_Error_2(self):
        tmsg.showerror("Error", "User Already Found")

    #Displaying the message if the login is not successful
    def Info_Error_3(self):
        tmsg.showerror("Error", "Username/Password cannot be empty")

    # Displaying the message if the Registration is successful
    def Info_Success_2(self):
        tmsg.showinfo("success", "Account Create successfully")

# Entering the Homepage
class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x500')
        self.root.title("HOMEPAGE")

        #Frame
        login_frame = Frame(self.root, bg="Silver")
        login_frame.place(x=0, y=0, width=800, height=50)
        title_login = Label(login_frame, text="WELCOME TO CRAIGSLIST", font=("palatino", 25, "bold"), bg="Silver",fg="Blue")
        title_login.pack()

        #Main Frame
        main_frame = Frame(self.root, bd=7, relief=RIDGE)
        main_frame.place(x=5, y=55, width=786, height=435)
        user_label_1 = Label(self.root,text = " HELLO USER!! ",font=("lucida",10,'bold'),fg = "Blue")
        user_label_1.grid(row = 3,column = 1,padx = 40,pady = 40)

        show_button = Button(self.root, text="DB POSTs", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                           relief=SUNKEN, command=self.get)
        show_button.grid(row=5, column=0, ipady=1, ipadx=8, pady=5, padx=10)
        submit_button = Button(self.root, text="FIND POST", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                         relief=SUNKEN, command=self.post)
        submit_button.grid(row=6, column=0, ipady=1, ipadx=8, pady=5)
        algo_button = Button(self.root, text="ALGO RUN", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                         relief=SUNKEN, command=self.algo)
        algo_button.grid(row=7, column=0, ipady=1, ipadx=8, pady=5)
        load_button = Button(self.root, text="LOAD FILE", font=("palatino", 10, "bold"), bg="Silver", fg="Blue", bd=7,
                         relief=SUNKEN, command=self.load)
        load_button.grid(row=4, column=0, ipady=1, ipadx=8, pady=5)
        load = Image.open("qq.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(main_frame, image=render)
        img.image = render
        img.grid(row=5, column=2)
        
    def load(self):
        loadFile(self.root)
        tmsg.showinfo("success","File Loading Successfull!!")
    def get(self):
        display = Toplevel(self.root)
        btn = showData(display)
    def post(self):
        self.secondScreen()
    def algo(self):
        algo_analysis(self.root)

    # Entering the Second Screen
    def secondScreen(self):
        root1 = Toplevel(self.root)
        enter = EnterData(root1)

class algo_analysis:
    def __init__(self,root):
        self.root = root
        self.algos()

    def algos(self):
        description=[]
        category=[]
        con = sq.connect('craig_data.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM post_data")
        results = list(cursor.fetchall())
        for result in results:
            #Combining both Section and Decription
            istr =str(result[3] + " " + result[4])
            prepos_str = self.my_preprocessor(istr)
            description.append(prepos_str)
            category.append(result[2])

        X_train=np.array(description)
        Y_train=category
        X_test = []
        Y_test = []

        with open('sample-test.in.json', 'r',encoding="utf8") as fp:
            next(fp)  #To skip the number of rows line
            for each_line in fp:
                test_data = json.loads(each_line)
                istr =test_data['section'] + " " + test_data['heading']
                X_test.append(self.my_preprocessor(istr))
        with open('sample-test.out.json', 'r',encoding="utf8") as fp:
            for each_op in fp:
                Y_test.append(each_op.rstrip('\n'))

        #Analysing which algorithm is most accurate
        Algorithm = [LinearSVC(),MultinomialNB(alpha=0.2, fit_prior=True),RandomForestClassifier()]
        accr_scr=0
        accr_alg=""
        for each_algo in Algorithm:
            model = Pipeline([('vect', CountVectorizer(stop_words='english', lowercase=True)),
                              ('tfidf', TfidfTransformer()),
                              ('clf', each_algo)])
            model.fit(X_train, Y_train)
            Y_pred = model.predict(X_test)
            print(each_algo,accuracy_score(Y_test,Y_pred))
            if accr_scr <  accuracy_score(Y_test,Y_pred):
                accr_scr = accuracy_score(Y_test,Y_pred)
                accr_alg = each_algo

        fd = str(accr_alg) + " " + "shows better accuracy: " + str(round(accr_scr*100,2))
        with open('Accu_algo.txt', 'w') as f:
            f.write(str(accr_alg))
        tmsg.showinfo("Results",fd)

        model = Pipeline([('vect', CountVectorizer(stop_words='english', lowercase=True)),
                          ('tfidf', TfidfTransformer()),
                          ('clf', accr_alg)])
        model.fit(X_train, Y_train)
        Y_pred = model.predict(X_test)
        cm = confusion_matrix(Y_test,Y_pred)
        print(cm)

        import seaborn as sn
        import pandas as pd
        labels = ['activities', 'appliances', 'artists', 'automotive', 'cell-phones', 'childcare', 'general',
                  'household-services', 'housing', 'photography', 'real-estate', 'shared', 'temporary', 'therapeutic',
                  'video-games', 'wanted-housing']
        df_cm = pd.DataFrame(cm,index=labels,columns=labels)
        plt.figure(figsize=(12, 12))
        cmap = sn.cubehelix_palette(light=1, as_cmap=True)
        sn.heatmap(df_cm, annot=True, fmt='.0f',cmap=cmap,
           vmin=0, vmax=100, cbar_kws={"shrink": .8},linecolor ='black', linewidths = 1)
        plt.show()
        print("completed!!!!")
        labels = ['activities', 'appliances', 'artists', 'automotive', 'cell-phones', 'childcare', 'general',
                  'household-services', 'housing', 'photography', 'real-estate', 'shared', 'temporary', 'therapeutic',
                  'video-games', 'wanted-housing']
        import pylab as pl
        cf_matrix = confusion_matrix(Y_test, Y_pred)
        print(cf_matrix)
        df_cm = pd.DataFrame(cf_matrix, columns=np.unique(Y_test), index=np.unique(Y_pred))
        df_cm.index.name = 'Actual'
        df_cm.columns.name = 'Predicted'
        plt.figure(figsize=(10, 7))
        sn.set(font_scale=1.4)  # for label size
        sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": 16})  # font size
        print("completed!!!!")

    def my_preprocessor(self,string):
        return re.sub('[-@~%^&*+#$/\.?!<>;:,\'\"\\(){}]', ' ', string).lower()

#Loading the json file
class loadFile:
    def __init__(self, root):
        self.root = root
        self.load()

    def load(self):
        con = sq.connect('craig_data.db')
        cursor = con.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_data(
                ID INTEGER PRIMARY KEY,
                City TEXT,
                Category TEXT NOT NULL,
                Section TEXT NOT NULL,
                description TEXT NOT NULL
                )
            """)
        all_rows=self.json_load()
        for each_row in all_rows:
            cursor.execute("INSERT INTO post_data VALUES(NULL,?,?,?,?)",
                                   (each_row[0], each_row[1], each_row[2], each_row[3]))
        con.commit()
        con.close()

    def json_load(self):
        post_list=[]
        with open('training.json', 'r') as f:
            next(f)
            for line in f:
                post = json.loads(line)
                post_list.append([post['city'],post['category'],post['section'],post['heading']])
        return post_list

#   Entering the Data
class EnterData:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x500')
        self.root.title("Welcome User")
        self.dataStart()
        self.desc = StringVar()

        # Enter Data Frame
        data_frame = Frame(self.root, bg="Silver")
        data_frame.place(width=800, x=0, y=0, height=45)
        label_data = Label(data_frame, bg="Silver", fg="Blue", font=("palatino", 25, "bold"), text="FIND CATEGORY")
        label_data.pack()
        # Main Frame
        main_frame = Frame(self.root, bd=10, relief=RIDGE)
        main_frame.place(width=780, height=440, x=5, y=46)
        label_title = Label(main_frame, text="POST DETAILS", font=("palatino", 15, "bold"))
        label_title.grid(row=0, column=0, padx=30,pady=40)

        # User
        title_enter = Entry(main_frame, textvariable=self.desc,font=("palatino",15))
        title_enter.grid(row=0, column=1, ipady=7, ipadx=50,columnspan = 2)
        button_sub = Button(main_frame, text="Submit", bg="Silver", fg="Blue", bd=7, font=("palatino", 10, "bold"),
                         command=self.enterData)
        button_sub.grid(row=0, column=3, ipady=7, pady=40, ipadx=15)
        load = Image.open("fp.png")
        render = ImageTk.PhotoImage(load)
        img = Label(main_frame, image=render)
        img.image = render
        img.grid(row=2, column=1)

    def dataStart(self):
        con = sq.connect('craig_data.db')
        cursor = con.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_data(
                ID INTEGER PRIMARY KEY,
                City TEXT,
                Category TEXT NOT NULL,
                Section TEXT NOT NULL,
                description TEXT NOT NULL
                )
            """)
        con.commit()
        con.close()

    def enterData(self):
        con = sq.connect('craig_data.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM post_data")
        results = list(cursor.fetchall())
        con.commit()
        con.close()
        description=[]
        category=[]
        for result in results:
            istr = str(result[3] + " " + result[4])
            prepos_str =self.my_preprocessor(istr)
            description.append(prepos_str)
            category.append(result[2])
        X_train = np.array(description)
        Y_train = category
        estimator=""
        print(self.desc.get())
        with open('Accu_algo.txt', 'r') as f:
            f_content = f.readlines()
        if f_content[0] == "LinearSVC()":
            estimator = LinearSVC()
        elif f_content[0] == "MultinomialNB(alpha=0.2)":
            estimator = MultinomialNB(alpha=0.2)
        else:
            estimator = RandomForestClassifier()

        print(str(estimator))
        model = Pipeline([('vect', CountVectorizer(stop_words='english', lowercase=True)),
                          ('tfidf', TfidfTransformer()),
                          ('clf',estimator)])
        model.fit(X_train, Y_train)
        Y_pred = model.predict([self.desc.get()])
        print(Y_pred)
        res= "Predicted Craigslist Category : " +  str(Y_pred)
        tmsg.showinfo("Algo Result", res)

    def my_preprocessor(self,string):
        return re.sub('[-@~%^&*+#$/\.?!<>;:,\'\"\\(){}]', ' ', string).lower()

class showData:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x500')
        self.root.title("Post Details")
        show_frame = Frame(self.root, bg="Blue")
        show_frame.place(width=800, x=0, y=0, height=50)
        label_show = Label(show_frame, bg="Blue", fg="Silver", font=("palatino", 15, "bold"), text="Details of Posts")
        label_show.pack()
        main_frame = Frame(self.root, bd=10, relief=SUNKEN)
        main_frame.place(width=780, height=430, x=8, y=58)
        tree = ttk.Treeview(main_frame, height=200)
        tree['columns'] = ("City", "Category", "Section", "description")
        tree.column('#0', width=50, minwidth=25)
        tree.column('City', width=50, minwidth=25)
        tree.column('Category', width=50, minwidth=25)
        tree.column('Section', width=50, minwidth=25)
        tree.column('description', width=250, minwidth=25)
        tree.heading("#0", text="ID", anchor=W)
        tree.heading("City", text="City", anchor=W)
        tree.heading("Category", text="Category", anchor=W)
        tree.heading("Section", text="Section", anchor=W)
        tree.heading("description", text="description", anchor=W)
        con = sq.connect('craig_data.db')
        cursor = con.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_data(
                ID INTEGER PRIMARY KEY,
                City TEXT,
                Category TEXT NOT NULL,
                Section TEXT NOT NULL,
                description TEXT NOT NULL
                )
            """)
        cursor.execute("SELECT * FROM post_data")
        result = cursor.fetchall()
        for i in result:
            tree.insert("", "end", text=f"{i[0]}", values=(f'{i[1]}', f'{i[2]}', f'{i[3]}', f'{i[4]}'))
        vsb = ttk.Scrollbar(main_frame, command=tree.yview, orient="vertical")
        tree.configure(yscroll=vsb.set)
        vsb.pack(side=RIGHT, fill=Y)
        tree.pack(side=TOP, fill=X)

if __name__ == "__main__":

    root = Tk()
    l = Login(root)
    root.mainloop()
