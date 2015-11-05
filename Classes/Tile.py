import pygame.mixer
from Classes.Game.GameClass import Game
from Classes.Game.Board import EMPTY_BOARD
pygame.mixer.init()
game = Game()

board = EMPTY_BOARD


# Class for apples
def play_sound(name):
    sound = pygame.mixer.Sound(name)
    sound.play()


class Tile:
    image = None
    counter = 0

    def __init__(self, counter):
        self.counter = counter

    def update(self):
        self.counter -= 1
        if self.counter <= 0:
            return False
        return True

    def effect(self, s):
        pass


class EmptyTile(Tile):
    def __init__(self):
        super().__init__(0)

    def update(self):
        return True


class PoisonTile(Tile):
    image = "Skull.png"

    def __init__(self):
        super().__init__(100)

    def effect(self, snake):
        x, y = snake.tail[0]
        if snake.size > 5:
            snake.size -= 5
            board[y][x] = EmptyTile()
            game.poison_count -= 1
            play_sound("Toxic.wav")
        else:
            snake.dead = True
            board[y][x] = EmptyTile()
            game.poison_count -= 1
            # Play a sound
            play_sound("Trombone.wav")


class MiracleTile(Tile):
    image = "green.png"

    def __init__(self):
        super().__init__(100)

    def effect(self, snake):
        x, y = snake.tail[0]
        game.special_counter -= 1
        board[y][x] = EmptyTile()
        snake.size += 5
        play_sound("ComputerError.wav")


class SpeedTile(Tile):
    image = "orange.png"

    def __init__(self):
        super().__init__(100)

    def effect(self, snake):
        x, y = snake.tail[0]
        game.special_counter -= 1
        board[y][x] = EmptyTile()
        play_sound("Blip.wav")
        snake.speed /= 1.5


class SlowTile(Tile):
    image = "blue2.png"

    def __init__(self):
        super().__init__(100)

    def effect(self, snake):
        x, y = snake.tail[0]
        game.special_counter -= 1
        board[y][x] = EmptyTile()
        play_sound("Slowdown.wav")
        snake.speed *= 1.5


class BorderTile(EmptyTile):
    image = "brick.png"

    def effect(self, snake):
        d = snake.direction.lower()
        head = snake.tail
        if d == "left":
            head[0] = (head[0][0] + len(board[0])-2, head[0][1])
        elif d == "right":
            head[0] = (head[0][0] - len(board[0])+2, head[0][1])
        elif d == "down":
            head[0] = (head[0][0], head[0][1]-len(board)+2)
        elif d == "up":
            head[0] = (head[0][0], head[0][1]+len(board)-2)


class Apple(Tile):
    image = "apple.png"

    def __init__(self):
        super().__init__(0)

    def effect(self, s):
        x, y = s.tail[0]
        board[y][x] = EmptyTile()
        # Play a sound
        play_sound("Badip.wav")
        s.eat()

    def update(self):
        return True
