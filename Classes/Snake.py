
__author__ = 'Davin'


# Class for the snake
class Snake:
    """This is the player's avatar"""
    original_speed = 6
    dead = False
    speed = original_speed
    size = 1
    score = size - 1
    cheat = False
    # Whether the score has been saved
    saved = False
    # Whether the sound has been played or not when the snake dies
    played = False
    # counter for updating snake
    update_counter = 0
    # Variable for tracking snakes x position
    x = 0
    # Variable for tracking snakes y position
    y = 0
    # handling directions and movement

    def __init__(self, x, y, d, color):
        self.original_direction = d
        self.original_position = [
            (x, y),
        ]
        self.tail = self.original_position
        self.color = color
        self.direction = d

    def move_snake(self):
        d = self.direction.lower()
        head = list(self.tail[0])
        if d == "left":
            head[0] -= 1
        elif d == "right":
            head[0] += 1
        elif d == "down":
            head[1] += 1
        elif d == "up":
            head[1] -= 1
        else:
            raise ValueError
        self.tail.insert(0, tuple(head))
        self.tail = self.tail[:self.size]

    def eat(self):
        self.score += 1
        self.size += 1
        print("eaten")

    def get_score(self):
        return self.score
