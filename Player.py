# This will be used to create a centerlized spot for player information

class Player_info:
    def __init__(self):
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
        self.score = 0
        self.credits = 0
        self.rounds = 1
        self.boss_rounds = 0

    def total_rounds(self):
        total = self.rounds + (5 * self.boss_rounds)
        return total