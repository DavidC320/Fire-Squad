from msilib.schema import tables
import sqlite3
from sre_compile import isstring
from tkinter import *
from tkinter import ttk, font, messagebox
# 4/11/2022
# FireSquad database manager
# 0.2.2
# db_credits
# based off of A1

class Database_manager:
    def __init__(self):

        self.conn = sqlite3.connect('database_stuff//score_board.db')

        # create cursor
        self.c = self.conn.cursor()

        # score table
        """CREATE TABLE scores(
        id INTEGER PRIMARY KEY,
        name TEXT,
        score INTEGER,
        difficulty INTEGER
        fake Integer 0 false 1 true
        hidden Integer 0 false 1 true
        )
        """
        # exicutes SQL commands
        # self.c.execute("""Alter Table scores add fake Integer bit default 0""")
        #self.c.execute("""update scores set fake = 1 where fake = 0""")

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

    def select_num_order(self, table, order_by, number, has_args, arguments):
        com = f'select * from {table} order by {order_by} desc limit {number}'
        if has_args:
            com = f'select * from {table} where {arguments} order by {order_by} desc limit {number}'
        self.c.execute(com)
        data = self.c.fetchall()
        self.commit_close()
        return data

    def record_data(self, table, table_contents, recorded_data):
        # (score, difficulty)
        self.c.execute(f'insert into {table} ({table_contents}) values ({recorded_data});')
        self.commit_close()

    def update_record(self, table, content, new_data, item_id):
        if isstring(new_data):
            self.c.execute(f'update {table} set {content} = "{new_data}" where id = {item_id}')
        else:
            self.c.execute(f'update {table} set {content} = {new_data} where id = {item_id}')
        self.commit_close()

    def commit_close(self):
        self.conn.commit()
        #self.conn.close()


################################## manger GUI ##################################
class Welcome_screen(Tk):
    # code based on B1
    def __init__(self):
        super().__init__()
        # window things
        self.title("Fire Squad Manager")
        self.Title = font.Font(size=20, weight= "bold")
        self.big_text = font.Font(size=12)

        # frames
        self.master_frame = Frame(self, padx=10, pady=10).grid(column=0, row=0)

        self.frame_title = Frame(self.master_frame, relief=RAISED, border=10)
        self.frame_title.grid(column=0, row=0, pady=6)

        self.frame = Frame(self.master_frame)
        self.frame.grid(column=0, row=1)

        # Labels
        Label(self.frame_title, anchor=CENTER, text="Welcome to the FS data manager", font=self.Title ).grid(column=0, row=1)
        Label(self.frame_title, text="Nail Box").grid(column=0, row=2)
        Label(self.frame_title, anchor=CENTER, text="Ver: 2.0").grid(column=0, row=3)
        Label(self.frame, justify=CENTER,
        text="In this manager you can manage the data\ncollected from the game Fire Squad.", font=self.big_text).grid(column=0, row=3)

        # Entry
        self.text_var = StringVar(self, "user")
        self.name = Entry(self.frame, textvariable=self.text_var).grid(column=0, row=5)

        # radio buttons
        # help from D2
        themes = {
            "Light theme" : "1",
            "Dark theme" : "2",
        }

        self.v = StringVar(self, "1")

        self.radio_frame = Frame(self.frame)
        self.radio_frame.grid(column=0, row=4)

        row_num = 0
        for (text, value) in themes.items():
            Radiobutton(self.radio_frame, text=text, variable=self.v, value = value).grid(column=0, row=row_num)
            row_num += 1

        # Buttons
        self.cont_btn = Button(self.frame, text="continue", command=self.manage_mode)
        self.cont_btn.grid(column=0, row=6)

    def manage_mode(self):
        num = self.v.get()
        name = self.text_var.get()
        new_window = Manager(int(num), self, name)
        new_window.resizable(False, False)
        self.withdraw()
        

class Manager(Toplevel):
    def __init__(self, theme, root, name):
        super().__init__()
        # window things
        self.title(f" welcome to the Manager, {name}")
        self.root = root
        # taken from E1
        self.protocol("WM_DELETE_WINDOW", self.close_aplication)

        # code form D4
        if theme == 1:
            self.configure(bg="white")
            frame_color = "white"
            self.data_frame_color = "cyan"
            title_text_color = "black"
            self.default_color = "light grey"
            """style = ttk.Style()
            style.theme_create("Light mode")
            style.theme_settings("Light mode",{})"""
        else:
            self.configure(bg="black")
            frame_color = "black"
            self.data_frame_color = "#3f66a6"
            title_text_color = "white"
            self.default_color = "#c9c9b7"


        # database connector
        self.data_manager = Database_manager()

        # frame
        self.frame = Frame(self)
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

        # filter
        self.filter_frame = Frame(self.cont_panel, bg = self.default_color, padx=5)
        self.filter_frame.grid(column=0, row=2, pady=5)

        Label(self.filter_frame, text= "Filters", bg=self.default_color, font=self.title, border=4, relief=RAISED).grid(column=0, columnspan=3, row=0)
        Label(self.filter_frame, text="Show deleted", bg=self.default_color, border=4, relief=RIDGE, width=10).grid(column=0, row=1, padx=5)
        Label(self.filter_frame, text="Show fake", bg=self.default_color, border=4, relief=RIDGE, width=10).grid(column=1, row=1, padx=5)
        Label(self.filter_frame, text="difficulty", bg=self.default_color, border=4, relief=RIDGE, width=10).grid(column=2, row=1, padx=5)
        show_dlt = {
            "show deleted" : "0",
            "hide deleted" : "1"
        }
        self.dlt_opt = StringVar(self, "1")

        show_fak = {
            "show fake" : "0",
            "hide fake" : "1"
        }
        self.fak_opt = StringVar(self, "0")

        diff_list ={
            "0" : "0",
            "1" : "1",
            "2" : "2",
            "3" : "3",
            "4" : "4",
            "all" : "5",
        }
        self.dif_opt = StringVar(self, "5")

        dlt = Frame(self.filter_frame, bg = self.default_color)
        dlt.grid(column=0, row=2)

        row_num = 0
        for (name, value) in show_dlt.items():
            Radiobutton(dlt, text=name, variable=self.dlt_opt, value=value).grid(column=0, row=row_num)
            row_num += 1

        fke = Frame(self.filter_frame, bg = self.default_color)
        fke.grid(column=1, row=2)

        row_num = 0
        for (name, value) in show_fak.items():
            Radiobutton(fke, text=name, variable=self.fak_opt, value=value).grid(column=0, row=row_num)
            row_num += 1

        dif = Frame(self.filter_frame, bg = self.default_color)
        dif.grid(column=2, row=2)

        row_num = 0
        for (name, value) in diff_list.items():
            Radiobutton(dif, text=name, variable=self.dif_opt, value=value).grid(column=0, row=row_num)
            row_num += 1

        Button(self.filter_frame, text="refresh", command= lambda: self.refresh_data_capsul(), bg=self.default_color). grid(column=0, columnspan=3, row=3)

        ############################################################################## data displayer ##############################################################################
        # data // data display only
        self.data_lab = Label(self.data_disp, border=6, relief=RIDGE)
        self.data_lab.grid(column=0, row=1, pady=5)
        
        # info for the data columns
        self.data_info = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
        self.data_info.grid(column=0, row=2)
        # dataf from data base
        self.data_capsul = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
        self.data_capsul.grid(column=0, row=3)
        # data deleter
        self.data_dltr = Frame(self.data_disp, bg=self.data_frame_color, relief="groove", border=5, padx=5, pady=3)
        self.data_dltr.grid(column=1, row=3)

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
            self.data_manager.record_data("scores",("name, score, difficulty, fake, hidden"), (f"'{name}', {score}, {difficulty}, 0, 0"))
            self.refresh_data_capsul()

    def refresh_data_capsul(self):
        if self.has_data:
            # frame clearer from D1
            for item in self.data_capsul.winfo_children():
                item.destroy()

            for item in self.data_dltr.winfo_children():
                item.destroy()

        self.build_data_table()
    
    def build_data_table(self):
        scores = self.filter_data()
        if len(scores) <= 0:
            self.data_lab.config(text="There is no data in the table", bg="Red")
            self.has_data = False
        else:
            self.data_lab.config(text="Data Found", bg="green")
            self.has_data = True
            Label(self.data_info, text="id", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=0, row=0, padx=2)
            Label(self.data_info, text="name", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=1, row=0, padx=2)
            Label(self.data_info, text="score", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=2, row=0, padx=2)
            Label(self.data_info, text="difficulty", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=3, row=0, padx=2)
            Label(self.data_info, text="is fake", anchor=CENTER, width=8, height=2, border=4, relief=RAISED, bg=self.default_color).grid(column=4, row=0, padx=2)
            row_num = 1

            for records in scores:
                # record items
                id = records[0]
                name = records[1]
                score = records[2]
                difficulty = records[3]
                fake = records[4]
                hidden = records[5]
                if fake == 1:
                    fake = "Yes"
                else:
                    fake = "No"
                Label(self.data_capsul, text=id, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=0, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=name, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=1, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=score, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=2, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=difficulty, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=3, row=row_num, padx=2, pady=1)
                Label(self.data_capsul, text=fake, anchor=CENTER, width=8, height=2, border=4, relief=GROOVE, bg=self.default_color).grid(column=4, row=row_num, padx=2, pady=1)
                # fix for button value resinment from D5
                if hidden == 0:
                    Button(self.data_dltr, text="DELETE", bg="Red", command= lambda id=id: self.delete_hide_record(id)).grid(column=0, row=row_num-1, pady=8)
                elif hidden == 1:
                    Button(self.data_dltr, text="RETURN", bg="Green", command= lambda id=id: self.bring_unhide_record(id)).grid(column=0, row=row_num-1, pady=8)
                row_num += 1

    def delete_hide_record(self, id):
        id = int(id)
        response = messagebox.askquestion("Warning", f"you will be hiding the {id} record. Do you want to continue?")
        if response == "yes":
            self.data_manager.update_record("scores", "hidden", "1", id)
            self.refresh_data_capsul()

    def bring_unhide_record(self, id):
        id = int(id)
        response = messagebox.askquestion("Warning", f"you will be unhiding the {id} record. Do you want to continue?")
        if response == "yes":
            self.data_manager.update_record("scores", "hidden", "0", id)
            self.refresh_data_capsul()

    def close_aplication(self):
        # taken from E1
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
      
    def filter_data(self):
        show_deleted = self.dlt_opt.get()
        show_fake = self.fak_opt.get()
        show_difficulty = self.dif_opt.get()
        argument1 = ""
        argument2 = ""
        argument3 = ""
        args = 0
        has_args = False

        if show_deleted == "1":  # if deleted should be hidden
            argument1 = "hidden = 0"
            args += 1


        if show_fake == "1": # if fake should be hidden
            argument2 = "fake = 0"
            if args > 0:
                argument2 = "and fake = 0"
            args += 1

        if int(show_difficulty) < 5:
            argument3 = f"difficulty = {show_difficulty}"
            if args > 0:
                argument3 = f"and difficulty = {show_difficulty}"
            args += 1

        argument = f"{argument1} {argument2} {argument3}"
        if args > 0:
            has_args = True
        scores = self.data_manager.select_num_order("scores", "score", 10, has_args, argument)
        return scores

    
#b = Database_manager(None)

if __name__ == "__main__":
    app = Welcome_screen()
    # resize disabler from D3
    app.resizable(False, False)
    app.mainloop()
