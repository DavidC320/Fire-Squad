# This will be used to create a centerlized spot for player information
from database_stuff import FireSquad_data_manager

class Player_info:
    def __init__(self):
        self.sql_manager = FireSquad_data_manager.Database_manager()

        self.name = None
        self.health = None
        self.damage = 1
        self.score = 0
        self.credits = 0
        self.rounds = 1
        self.boss_rounds = 0
        self.dif = None

        # upgrade levels
        self.damage_lv = 1
        self.health_lv = 1
        self.firerate_lv = 1
        
        # colleted data
        self.kills = 0
        self.shots = 0
        self.deaths = 0

    def reset_info(self):
        if self.dif != None:
            check1 = self.score > 0
            check2 = self.rounds > 1
            check3 = self.dif < 5 
            if check1 and check2 and check3:
                print("ping")
                self.sql_manager.record_data("scores",("name, score, difficulty, fake, hidden"), (f"'{self.name}', {self.score}, {self.dif}, 0, 0"))
        self.score = 0
        self.credits = 0
        self.rounds = 1
        self.boss_rounds = 0

    def total_rounds(self):
        total = self.rounds + (5 * self.boss_rounds)
        return total