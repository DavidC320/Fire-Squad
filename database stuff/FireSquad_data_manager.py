import sqlite3
from tkinter import *
from tkinter import ttk
import sqlite3
# 4/11/2022
# FireSquad database manager
# Alpha 0.0.2
# based off of M1

class Database_manager:
    def __init__(self, instance_database):
        self.data = instance_database  # this data is from the game itself since that information can not be saved.
        if self.data == None:
            modify_data = False  # this will turn off the ability to create records.
        None

        conn = sqlite3.connect('database stuff//score_board.db')

        # create cursor
        self.c = conn.cursor()

        # create a table
        """
        score_board
        id INTEGER PRIMARY KEY
        name TEXT
        difficulty INTEGER
        enemies_killed INTEGER
        total_creates INTEGER
        score INTEGER
        """

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

            if action == "help":
                print("""This is alpha 0.0.2 of the database manager.

                database commands:
                
                Commands:
                admin - test if your admin
                data connected - test if there is data connected
                exit - exit program""")

            elif action == "exit":
                print("bye")
                running = False

            elif action == "data connected":
                if self.data:
                    print("data is connected.")
                else:
                    print("data is not connected.")

            elif action == "admin":
                if self.data:
                    print("you are admin.")
                else:
                    print("you are not adim.")

            else:
                print("This is not a command.\nThe command might not be implemented or exists.")
            print(" ")


    
b = Database_manager(None)
b.command_prompt()
