from ast import Delete
from msilib.schema import tables
from re import T
import sqlite3
from tkinter import *
from tkinter import ttk, font, messagebox
import sqlite3
# 4/11/2022
# FireSquad database manager
# Alpha 0.1.1
# db_credits
# based off of A1

class Database_manager:
    def __init__(self, instance_database):
        self.data = instance_database  # this data is from the game itself since that information can not be saved.
        if self.data == None:
            modify_data = False  # this will turn off the ability to create records.
        None

        self.conn = sqlite3.connect('database stuff//score_board.db')

        # create cursor
        self.c = self.conn.cursor()

        # score table
        """CREATE TABLE scores(
        id INTEGER PRIMARY KEY,
        name TEXT,
        score INTEGER,
        difficulty INTEGER
        fake Integer
        )
        """
        # exicutes SQL commands
        #self.c.execute("""Alter Table scores add fake Integer bit default 0""")
        #self.c.execute("""Alter Table scores add hidden Integer bit default 0""")

        # actually gets the data
        # self.c.fetchone()
        # self.c.fetchmany(3)
        #self.c.fetchall()

        #self.commit_close()

    def select_all(self, table):
        self.c.execute(f'select * from {table}')
        data = self.c.fetchall()
        self.commit_close()
        return data

    def select_num_order(self, table, order_by, number):
        self.c.execute(f'select * from {table} order by {order_by} desc limit {number}')
        data = self.c.fetchall()
        self.commit_close()
        return data

    def record_data(self, table, table_contents, recorded_data):
        # (score, difficulty)
        self.c.execute(f'insert into {table} ({table_contents}) values ({recorded_data});')
        self.commit_close()

    def commit_close(self):
        self.conn.commit()
        #self.conn.close()


################################## manger GUI ##################################
class Welcome_screen:
    # code based on B1
    def __init__(self, root):
        super().__init__()
        # window things
        self.root = root
        self.root.title("Fire Squad Manager")
        self.Title = font.Font(size=20, weight= "bold")
        self.big_text = font.Font(size=12)

        # frames
        self.master_frame = Frame(self.root, padx=10, pady=10).grid(column=0, row=0)

        self.frame_title = Frame(self.master_frame, relief=RAISED, border=10)
        self.frame_title.grid(column=0, row=0, pady=6)

        self.frame = Frame(self.master_frame)
        self.frame.grid(column=0, row=1)

        # Labels
        Label(self.frame_title, anchor=CENTER, text="Welcome to the FS data manager", font=self.Title ).grid(column=0, row=1)
        Label(self.frame_title, text="Nail Box").grid(column=0, row=2)
        Label(self.frame_title, anchor=CENTER, text="Ver: 1.0").grid(column=0, row=3)
        Label(self.frame, justify=CENTER,
        text="In this manager you can manage the data\ncollected from the game Fire Squad.", font=self.big_text).grid(column=0, row=3)
        self.name = Entry(self.frame)

        # radio buttons
        # help from D2
        themes = {
            "Light theme" : "1",
            "Dark theme" : "2",
        }

        self.v = StringVar(self.root, "1")

        self.radio_frame = Frame(self.frame)
        self.radio_frame.grid(column=0, row=4)

        row_num = 0
        for (text, value) in themes.items():
            Radiobutton(self.radio_frame, text=text, variable=self.v, value = value).grid(column=0, row=row_num)
            row_num += 1

        # Buttons
        self.cont_btn = Button(self.frame, text="continue", command=self.manage_mode)
        self.cont_btn.grid(column=0, row=5)

    def manage_mode(self):
        new_window = Tk()
        num = self.v.get()
        new_window.resizable(False, False)
        win2 = Manager(new_window, int(num))
        self.root.destroy()
        

class Manager:
    def __init__(self, root, theme):
        super().__init__()
        # window things
        self.root = root
        self.root.title("Manager")

        # code form D4
        if theme == 1:
            self.root.configure(bg="white")
            frame_color = "white"
            self.data_frame_color = "cyan"
            title_text_color = "black"
            self.default_color = "light grey"
            """style = ttk.Style()
            style.theme_create("Light mode")
            style.theme_settings("Light mode",{})"""
        else:
            self.root.configure(bg="black")
            frame_color = "black"
            self.data_frame_color = "#3f66a6"
            title_text_color = "white"
            self.default_color = "#c9c9b7"


        # database connector
        self.data_manager = Database_manager(None)

        # frame
        self.frame = Frame(self.root)
        self.frame.grid(column=0, row=0)

        # tabs
        self.tabCont = ttk.Notebook(self.frame)

        self.score_board = Frame(self.tabCont, bg=frame_color)
        self.score_board.grid(row=0, column=0)

        # add to tab controller
        self.tabCont.add(self.score_board, text="Scores")
        self.tabCont.pack(expand=1, fill="both")

        ##################### score board #####################
        
        # fonts // code from C1
        self.Title = font.Font(size=20, weight= "bold")

        # frames
        self.cont_panel = Frame(self.score_board, padx=10, pady=10, border=5, relief="groove", bg="grey")
        self.cont_panel.grid(column=0, row=2, padx=10)

        self.data_disp = Frame(self.score_board, padx=10, pady=10, border=5, relief="raised", bg=self.data_frame_color)
        self.data_disp.grid(column=1, row=2, padx=10)

        # labels
        Label(self.score_board, text="Score Board", anchor=CENTER, font=self.Title, fg=title_text_color, bg=frame_color).grid(column=0, columnspan=2, row=0)
        Label(self.cont_panel, text="Control Panel", bg="grey", font=self.Title).grid(column=0, row=0)
        Label(self.data_disp, text="Score Data", bg=self.data_frame_color, font=self.Title).grid(column=0, row=0)

        ############################################################################### data controller ###############################################################################
        # buttons // control panal only

        # fake record recorder
        # alot of help from C2
        self.crt_rec = Frame(self.cont_panel, bg=self.default_color)
        self.crt_rec.grid(column=0, row=1, pady=5)

        Label(self.crt_rec, text="Create a fake Record", font=self.Title, border=4, relief=RAISED, bg=self.default_color).grid(column=0, columnspan=3, pady=6, row=0)
        Label(self.crt_rec, text="Name", width=8, border=4, relief=RIDGE, bg=self.default_color).grid(column=0, row=1, padx=4)
        Label(self.crt_rec, text="score", width=8, border=4, relief=RIDGE, bg=self.default_color).grid(column=1, row=1, padx=4)
        Label(self.crt_rec, text="difficulty", width=8, border=4, relief=RIDGE, bg=self.default_color).grid(column=2, row=1, padx=4)

        self.name_txt = StringVar()
        self.name_txt.set("Null")
        self.score_num = IntVar()
        self.score_num.set(0)
        self.diff_num = IntVar()
        self.diff_num.set(0)

        self.fk_name = Entry(self.crt_rec, textvariable=self.name_txt)
        self.fk_score = Spinbox(self.crt_rec, textvariable=self.score_num, from_=0)
        self.fk_difficulty = Spinbox(self.crt_rec, textvariable=self.diff_num, from_=0, to=4)

        self.fk_name.grid(column=0 ,row=2)
        self.fk_score.grid(column=1 ,row=2)
        self.fk_difficulty.grid(column=2 ,row=2)

        # lambda relarned form C3
        self.insert_btn = Button(self.crt_rec, text="Insert fake record", command= lambda: self.insert_record(), bg=self.default_color)
        self.insert_btn.grid(column=0, columnspan=3, row=3)

        ############################################################################## data displayer ##############################################################################
        # data // data display only
        self.build_data_table()

    def insert_record(self):
        can_record = True
        print("ping")
        name = self.fk_name.get()
        score = self.fk_score.get()
        if not score.isdigit():
            print("score is not a integer")
            can_record = False
        else:
            score = int(score)
            if score < 0:
                score = 0
        difficulty = self.fk_difficulty.get()
        if not difficulty.isdigit():
            print("difficulty is not a integer")
        else:
            difficulty = int(difficulty)
            if difficulty > 4:
                difficulty = 4

        if can_record:
            print(f"'{name}', {score}, {difficulty}, 0")
            self.data_manager.record_data("scores",("name, score, difficulty, fake"), (f"'{name}', {score}, {difficulty}, 0"))
            self.refresh_data_capsul()

    def refresh_data_capsul(self):
        # frame clearer from D1
        for item in self.data_capsul.winfo_children():
            item.destroy()

        for item in self.data_dltr.winfo_children():
            item.destroy()

        self.build_data_table()
    
    def build_data_table(self):
        scores = self.data_manager.select_num_order("scores","score",10)
        if len(scores) <= 0:
            Label(self.data_disp, text="There is no data in the table", bg="Red", border=6, relief=RIDGE).grid(column=0, row=1, pady=5)
        else:
            Label(self.data_disp, text="Data Found", bg="green", border=6, relief=RIDGE).grid(column=0, row=1, pady=5)
            # info for the data columns
            self.data_info = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
            self.data_info.grid(column=0, row=2)
            # dataf from data base
            self.data_capsul = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
            self.data_capsul.grid(column=0, row=3)
            # data deleter
            self.data_dltr = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
            self.data_dltr.grid(column=1, row=3)
            Label(self.data_info, text="id", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=0, row=0, padx=2)
            Label(self.data_info, text="name", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=1, row=0, padx=2)
            Label(self.data_info, text="score", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=2, row=0, padx=2)
            Label(self.data_info, text="difficulty", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=3, row=0, padx=2)
            Label(self.data_info, text="is fake", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=4, row=0, padx=2)
            row_num = 1

            for records in scores:
                # record items
                id = records[0]
                print(id)
                name = records[1]
                score = records[2]
                difficulty = records[3]
                fake = records[4]
                if fake == 0:
                    fake = "Yes"
                else:
                    fake = "No"
                Label(self.data_capsul, text=id, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=0, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=name, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=1, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=score, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=2, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=difficulty, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=3, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=fake, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=4, row=row_num, padx=2, pady=1)
                # fix for button value resinment from D5
                Button(self.data_dltr, text="DELETE", bg="Red", command= lambda id=id: self.delete_hide_record(id)).grid(column=0, row=row_num-1, pady=8)
                row_num += 1

    def delete_hide_record(self, id):
        print(id)



        
    
#b = Database_manager(None)

if __name__ == "__main__":
    root = Tk()
    app = Welcome_screen(root)
    # resize disabler from D3
    root.resizable(False, False)
    root.mainloop()
