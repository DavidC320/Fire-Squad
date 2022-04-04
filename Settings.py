# Default stuff
wn_width = 800
wn_height = 600
z_max = 6

# Enemy information
enemy_name = [
    'chaser',  # Chases the player// target position is the center of the screen
    "shooter",  #  stays at half of z_max// shoots bullets at the center of the screen
    "launcher"  # stays at half of z_max// fires a missle at a random posistion on the sceen
    #"morpher",  #  goes to random points on the screen// transforms into a random ship after a few seconds
    #"holder"  #  spawns near z_max off screen// will fly away towards the center of the sceen and dissapear when z < 0
    ]

boss_enemy_names = [
    "seeker",  # acts like a chaser
    "gatulus", # acts like a shooter
    "tearer", # acts like a launcher
    "Gazar" # creates a target retical and fires at the location

]

projectiles = [
    "bullet",
    "missle",
    "laser",
    "mlaser"
]

# this will be used to check if the enemy is apart of the ranger classification // I think I need to remove this
rangers = [
    "shooter",
    "launcher",
    "gatulus",
    "tearer"
    ]
fighters = [
    "chaser",
    "seeker"
    ]

enemy_weight = [
    49,
    49,
    49
    #24, 
    #4
    ]  # for probability or chance of happening
