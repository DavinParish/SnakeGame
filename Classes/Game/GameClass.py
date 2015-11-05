from random import randint
__author__ = 'Davin'


class Game:
    """description of class"""
    # A counter for regular apples
    counter = 8
    found_apple = False
    # A counter for gems
    special_counter = 0
    # Variable for the purpose of getting the game to wait to continue
    wait = True

    # Variable handling whether to activate two players or one
    twoPlayer = False

    # Variable to pause the game
    paused = False

    # Variable handling whether a players score has already been reduced or not if he died first
    # In the absence of this variable, which ever player dies first
    # gets a score of 0 due to repeated reduction of points
    reduced = False

    # Counters for for the purpose of giving gems and skulls a lifespan
    count_speed = 0
    counter_poison = 0
    count_slow = 0
    count_miracle = 0

    left_relative = 0
    right_relative = 0
    # Random number for the purpose of deciding how many skulls to make
    b = randint(10, 50)

    # Variable for counting the number of poison apples
    poison_count = b
