from msilib.schema import tables
from re import T
import sqlite3
from tkinter import *
from tkinter import ttk
import sqlite3
# 4/11/2022
# FireSquad database manager
# Alpha 0.1.0
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
        )
        """
        # exicutes SQL commands
        # self.c.execute()

        # actually gets the data
        # self.c.fetchone()
        # self.c.fetchmany(3)
        # self.c.fetchall()

    def command_prompt(self):
        first_time = True
        running = True
        while running:
            if first_time:
                action = input("Welcome to the FireSquad database manager.\nfor help inter help.: ")
                first_time = False
                print(" ")
            else:
                action = input("For help enter help.: ")

            ########################################## actions ##########################################

            ###################################### basic commands ######################################
            # help action
            if action == "help":
                print("""This is alpha 0.0.2 of the database manager.

                database commands:
                all scores - returns ecery record in the scores table
                
                Commands:
                admin - test if your admin
                data connected - test if there is data connected
                exit - exit program""")

            elif action == "thanks":
                print("Your welcome")

            elif action == "Pineapple":
                print("Okay... ._.")

            # exit action
            elif action == "exit":
                print("bye")
                running = False

            # data connection test
            elif action == "data connected":
                if self.data:
                    print("data is connected.")
                else:
                    print("data is not connected.")

            # admin check test
            elif action == "admin":
                if self.data:
                    print("you are admin.")
                else:
                    print("you are not admin.")

            ##################################### database commands #####################################

            # select all from score table
            elif action == "all scores":
                self.c.execute('select * from scores')

                text = (self.c.fetchall())
                print(f"Here is everything in the scores table\n{text}")

                self.commit_close()


            ######################################## debug error ########################################

            # error thing
            else:
                print("This is not a command.\nThe command might not be implemented or exists.")
            print(" ")

    def select_all(self, table):
        self.c.execute(f'select * from {table}')
        data = self.c.fetchall()
        self.commit_close()
        return data

    def record_data(self, table, table_contents, recorded_data):
        self.c.execute(f'insert into {table} ({table_contents}) values ({recorded_data});')

        self.commit_close()

    def commit_close(self):
        self.conn.commit()
        self.conn.close()

################################## manger GUI ##################################
class Welcome_screen:
    # code based on B1
    def __init__(self, root):
        super().__init__()
        # window things
        self.root = root
        self.root.title("Fire Squad Manager")

        # frames
        self.frame = Frame(self.root)
        self.frame.grid(column=0, row=0)

        # Labels
        Label(self.frame, anchor=CENTER, text="Welcome to the FS data manager" ).grid(column=0, row=1)
        Label(self.frame, anchor=CENTER, text="Ver: 1.0").grid(column=0, row=2)
        Label(self.frame, justify=CENTER,
        text="In this manager you can manage the data collected from playing.").grid(column=0, row=3)

        # Buttons
        self.cont_btn = Button(self.frame, text="continue", command=self.manage_mode)
        self.cont_btn.grid(column=0, row=4)

    def manage_mode(self):
        new_window = Tk()
        win2 = Manager(new_window)
        self.root.destroy()
        
        

class Manager:
    def __init__(self, root):
        super().__init__()
        # window things
        
        self.root = root
        self.root.title("Manager")

        # database connector
        self.data_manager = Database_manager(None)

        # frame
        self.frame = Frame(self.root)
        self.frame.grid(column=0, row=0)

        # tabs
        self.tabCont = ttk.Notebook(self.frame)

        self.score_board = ttk.Frame(self.tabCont)
        self.score_board.grid(row=0, column=0)

        # add to tab controller
        self.tabCont.add(self.score_board, text="Scores")
        self.tabCont.pack(expand=1, fill="both")

        ##################### score board #####################

        # frames
        self.cont_panel = Frame(self.score_board, padx=10, pady=10, border=5, relief="groove", bg="grey")
        self.cont_panel.grid(column=0, row=2, padx=10)

        self.data_disp = Frame(self.score_board, padx=10, pady=10, border=5, relief="raised", bg="cyan")
        self.data_disp.grid(column=1, row=2, padx=10)

        # labels
        Label(self.score_board, text="Score Board", anchor=CENTER).grid(column=0, columnspan=2, row=0)
        Label(self.cont_panel, text="Control Panel").grid(column=0,row=0)
        Label(self.data_disp, text="Score Data").grid(column=0,row=0)

        # buttons // control panal only

        # data // data display only
        scores = self.data_manager.select_all("scores")
        if len(scores) <= 0:
            Label(self.data_disp, text="There is no data in the table").grid(column=0, row=1)
        else:
            Label(self.data_disp, text="Data Found").grid(column=0, row=1)


        
    
b = Database_manager(None)
# b.command_prompt()

"""if __name__ == "__main__":
    root = Tk()
    app = Welcome_screen(root)
    root.mainloop()"""
