from copy import deepcopy
import json
import os
from random import randint

import pygame

import pygame.font
import pygame.event
import pygame.draw
import pygame.mixer
import pygame.image
from Classes.Game.GameClass import Game
from Classes.Game.Board import EMPTY_BOARD
from Classes.Snake import Snake
from Classes.Tile import EmptyTile, PoisonTile, MiracleTile, SpeedTile, SlowTile, Apple, BorderTile

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)


TILE_WIDTH = 24
TILE_HEIGHT = 24


stuff = {
    0: EmptyTile,
    1: BorderTile,
}

for i in range(len(EMPTY_BOARD)):
    EMPTY_BOARD[i] = [stuff[c]() for c in EMPTY_BOARD[i]]

# create objects of the classes
snake = Snake(65, 5, "Left", (0, 255, 0, 255))
snake_2 = Snake(1, 7, "Right", (0, 0, 255, 255))
robot = Snake(32, 30, "Up", (255, 0, 0, 255))
SNAKES = [snake, snake_2, robot]

game = Game()

# copy of the empty board
board = deepcopy(EMPTY_BOARD)


'''Robot functions'''


# front check
# list of positions in front of the robot
def list_front():
    head = robot.tail
    if not isinstance(board[head[0][1]][head[0][0]], BorderTile):
        if robot.direction.lower() == "up" or robot.direction.lower() == "down":
            b = head[0][1]
            if robot.direction.lower() == "down":
                front_list = [b+1]
                return front_list
            elif robot.direction.lower() == "up":
                front_list = [b-1]
                return front_list
        elif robot.direction.lower() == "right" or robot.direction.lower() == "left":
            b = head[0][0]
            if robot.direction.lower() == "right":
                front_list = [b+1]
                return front_list
            elif robot.direction.lower() == "left":
                front_list = [b-1]
                return front_list

        # return front_list
    else:
        front_list = [0]
        return front_list


# to change the direction if you run into a problem like skulls
def change_direction():
    # I wanted to make room for error on the part o the robot.
    # How boring would it be to compete against a perfect competitor
    # the integer 0 is a built in imperfection for the robot.
    # if it picks this number it will die
    if game.left_relative >= 2:
        f = 2
    #     If you've gone left twice relative to the snakes direction you want to go right

    elif game.right_relative >= 2:
        f = 1
    #    If you've gone right twice relative to the snakes direction you want to go lef relative to the snakes direction

    else:
        f = randint(1, 2)

    if robot.direction.lower() == "up":
        if f == 0:
            return
        elif f == 1:
            # we returned a 1 so we want the snake to go to the relative left
            # if your going up then relative left is to the left side of the board
            robot.direction = "Left"
            game.left_relative += 1
            game.right_relative = 0
        elif f == 2:
            # we returned a 2 so we want the snake to go to the relative right
            # if you are going up, relative right is to the right side of the board
            robot.direction = "Right"
            game.right_relative += 1
            game.left_relative = 0

    elif robot.direction.lower() == "down":
        if f == 0:
            return
        elif f == 2:
            # we returned a 2 so we want the snake to go to the relative right
            # If you are going down, the relative right is to the left side of the board
            robot.direction = "Left"
            game.left_relative = 0
            game.right_relative += 1

        elif f == 1:
            # we returned a 1 so we want the snake to go to the relative left
            #  When you are going down the relative left is to the right side of the board
            robot.direction = "Right"
            game.right_relative = 0
            game.left_relative += 1

    elif robot.direction.lower() == "right":
        if f == 0:
            return
        elif f == 1:
            # we returned a 1 so we want the snake to go to the relative left
            #  When you are going to the right (east), the relative left is up
            robot.direction = "Up"
            game.left_relative += 1
            game.right_relative = 0
        elif f == 2:
            # we returned a 2 so we want to go to the relative right
            #  when you are going right, the relative right is down
            robot.direction = "Down"
            game.right_relative += 1
            game.left_relative = 0

    elif robot.direction.lower() == "left":
        if f == 0:
            return
        elif f == 2:
            #  We returned a 2 so we want to go to the relative right
            #  When you are going left the relative right is up
            robot.direction = "Up"
            game.left_relative = 0
            game.right_relative += 1
        elif f == 1:
            #  We returned a 1, so we want to go to the relative left
            #  when you are going left the relative left is down
            robot.direction = "Down"
            game.right_relative = 0
            game.left_relative += 1


# Check in front of the snake for bad apples
def check_front_y():
    head = robot.tail[0]
    # Go through the x list until you find an apple
    for point in list_front():
        # If an apple is found:
        # if isinstance(board[list_front()[y]][head[0][0]], MiracleTile):
        #     return
        # elif isinstance(board[list_front()[y]][head[0][0]], SpeedTile):
        #     return
        # elif isinstance(board[list_front()[y]][head[0][0]], Apple):
        #     return
        x, y = head[0], point
        for s in SNAKES:
            if (x, y) in s.tail[1:]:
                change_direction()
                return
        if isinstance(board[y][x], PoisonTile):
            change_direction()
            return
        elif isinstance(board[y][x], SlowTile):
            change_direction()
            return


def check_front_x():
    # Go through the x list until you find an apple
    head = robot.tail[0]
    # Go through the x list until you find an apple
    for point in list_front():
        y, x = head[1], point
        for s in SNAKES:
            if (x, y) in s.tail[1:]:
                change_direction()
                return
        if isinstance(board[y][x], PoisonTile):
            change_direction()
            return
        elif isinstance(board[y][x], SlowTile):
            change_direction()
            return


    # for x in range(0, len(list_front())):
    #     # If an apple is found:
    #     # if isinstance(board[head[0][1]][list_front()[x]], MiracleTile):
    #     #     return
    #     # elif isinstance(board[head[0][1]][list_front()[x]], SpeedTile):
    #     #     return
    #     # elif isinstance(board[head[0][1]][list_front()[x]], Apple):
    #     #     return
    #     y, x = head[1], point
    #     if board[head[0][1]][x] in robot.tail[1:]:
    #         change_direction()
    #         return
    #     elif board[head[0][1]][list_front()[x]] in snake.tail[1:]:
    #         change_direction()
    #         return
    #     elif isinstance(board[head[0][1]][list_front()[x]], PoisonTile):
    #         change_direction()
    #         return
    #     elif isinstance(board[head[0][1]][list_front()[x]], SlowTile):
    #         change_direction()
    #         return


# Function to guide robot
# A function to get the direction neccesary to go in order to get the apples
def get_direction_x(x, head_position):
    if x < head_position:
        if robot.direction.lower() == "up" and game.left_relative < 2:
            robot.direction = "Left"
            game.left_relative += 1
            game.right_relative = 0
        elif robot.direction.lower() == "down" and game.right_relative < 2:
            robot.direction = "Left"
            game.right_relative += 1
            game.left_relative = 0

        else:
            return
    elif x > head_position:
        if robot.direction.lower() == "down" and game.left_relative < 2:
            robot.direction = "Right"
            game.left_relative += 1
            game.right_relative = 0
        elif robot.direction.lower() == "up" and game.right_relative < 2:
            robot.direction = "Right"
            game.right_relative += 1
            game.left_relative = 0
        else:
            return


# Get the direction that the snake needs to go in order to get an apple
def get_direction_y(y, head_position):
    if y > head_position:
        if robot.direction.lower() == "right" and game.right_relative < 2:
            # since when your going right, down is right relatively we only want to go down if right_relative is less
            # than 3. We also want to increment the right relative because we just went right relatively
            robot.direction = "Down"
            game.left_relative = 0
            game.right_relative += 1
            print("ltiouteoiyw")
        elif robot.direction.lower() == "left" and game.left_relative < 2:
            robot.direction = "Down"
            game.left_relative += 1
            game.right_relative = 0
            print("lkkjkjlkj")
        else:
            return
        print("jimmminy crikey")
    elif y < head_position:
        if robot.direction.lower() == "right" and game.right_relative < 2:
            robot.direction = "Up"
            game.left_relative += 1
            game.right_relative = 0
            print("going up!")
        if robot.direction.lower() == "left" and game.left_relative < 2:
            robot.direction = "Up"
            game.right_relative += 1
            game.left_relative = 0
            print("up we go")

        else:
            return
            print("blahblahblah")


# Create a list of position to either side of the snakes head
def list_x():
    head = robot.tail
    if not isinstance(board[head[0][1]][head[0][0]], BorderTile):
        b = head[0][0]
        x_list = [b-1, b+1]
        # [b-5, b-4, b-3, b-2, b-1, b+1, b+2, b+3, b+4, b+5]
        return x_list
    else:
        x_list = [0]
        return x_list


# Create a list of positions above and below the snakes head
def list_y():
    head = robot.tail
    if not isinstance(board[head[0][1]][head[0][0]], BorderTile):
        b = head[0][1]
        y_list = [b-1, b+1]
        return y_list
    else:
        y_list = [0]
        return y_list


# To find apples and move the robot in the x direction
def make_go_x():
    head = robot.tail
    # Go through the x list until you find an apple
    for x in range(0, len(list_x())):
        # If an apple is found:
        if isinstance(board[head[0][1]][list_x()[x]], MiracleTile):
            # Get the necessary direction to go to get the x coordinate of the apple
            get_direction_x(list_x()[x], head[0][0])
            return
        elif isinstance(board[head[0][1]][list_x()[x]], SpeedTile):
            # Get the necessary direction to go to get the x coordinate of the apple
            get_direction_x(list_x()[x], head[0][0])
            return
        elif isinstance(board[head[0][1]][list_x()[x]], Apple):
            # Get the necessary direction to go to get the x coordinate of the apple
            get_direction_x(list_x()[x], head[0][0])
            return
        elif board[head[0][1]][list_x()[x]] in robot.tail:
            return
        elif isinstance(board[head[0][1]][list_x()[x]], PoisonTile) or board[head[0][1]][list_x()[x]] in snake.tail:
            return


# To find apples and make robot move in the y direction
def make_go_y():
    head = robot.tail

    # Go through the x list until you find an apple
    for y in range(0, len(list_y())):

        # If an apple is found:
        if isinstance(board[list_y()[y]][head[0][0]], MiracleTile):
            # Get the necessary direction to go to get the x coordinate of the apple
            get_direction_y(list_y()[y], head[0][1])
            return
        elif isinstance(board[list_y()[y]][head[0][0]], SpeedTile):
            # Get the necessary direction to go to get the x coordinate of the apple
            get_direction_y(list_y()[y], head[0][1])
            return
        elif isinstance(board[list_y()[y]][head[0][0]], Apple):
            # Get the necessary direction to go to get the x coordinate of the apple
            print("jeshua")
            get_direction_y(list_y()[y], head[0][1])
            return
        elif board[list_y()[y]][head[0][0]] in robot.tail:
            return
        elif isinstance(board[list_y()[y]][head[0][0]], PoisonTile):
            return
        elif board[list_y()[y]][head[0][0]] in snake.tail:
            return


def move():
    if robot.direction.lower() == 'left' or robot.direction.lower() == 'right':
        check_front_x()
        make_go_y()

        # check_front_x()
    elif robot.direction.lower() == 'up' or robot.direction.lower() == 'down':
        check_front_y()
        make_go_x()
        # check_front_y()
    print(str(game.left_relative))
    print(str(game.right_relative))
    print('\n\n')




# Function that handles the changing of the snake head's orientation when it turns
def change_snake(player, x, y, part):
    if player.direction == "Right":
        draw_image(x, y, part + " right.png")
    elif player.direction == "Left":
        draw_image(x, y, part + " left.png")
    elif player.direction == "Up":
        draw_image(x, y, part + " up.png")
    elif player.direction == "Down":
        draw_image(x, y, part + " down.png")


'''Sound and Images'''
LOADED_IMAGES = {}


# Function that handles the drawing and displaying of images
def draw_image(t, r, name, ):
    if name in LOADED_IMAGES:
        layer = LOADED_IMAGES[name]
    else:
        layer = pygame.image.load(os.path.join(name)).convert_alpha()
        LOADED_IMAGES[name] = layer
    screen.blit(layer, ((t * TILE_WIDTH) + 2, r * TILE_HEIGHT))


# Function that handles the playing of sound
def play_sound(name):
    sound = pygame.mixer.Sound(name)
    sound.play()


# Function that handles the display of text on the window
def display_box(message, position):
    font_object = pygame.font.SysFont('Times New Roman', 18)
    if message:
        text = font_object.render(message, 1, (255, 0, 0, 255))

        screen.blit(text, position)


'''Apple, gem and skull creation functions'''


# Function that handles the creation/positioning of an apple
def spawn(typ, array):
    # place initially is equal to false thus activating the loop
    # it then generates a random index at which to spawn the apple
    # If the index is empty place is set equal to true and the loop is not executed again
    # otherwise the loop is re-executed

    # noinspection PyPep8Naming
    Cls = {
        "apple": Apple,
        "poison": PoisonTile,
        "miracle": MiracleTile,
        "slow": SlowTile,
        "speed": SpeedTile,
    }[typ]
    # Whether it is okay to place the apple in a position
    place = False
    while not place:
        l = randint(1, len(board) - 2)
        k = randint(1, len(board[0]) - 2)
        if isinstance(array[l][k], EmptyTile) and (k, l) not in snake.tail:  # if the index is empty
            array[l][k] = Cls()
            place = True
        else:
            place = False


# Function that handles the initial placing of all the regular apples
def spawn_all_apples():
    global board
    game.special_counter = 0
    board = deepcopy(EMPTY_BOARD)
    for _ in range(200):
        # create random number generator
        spawn("apple", board)


# Function that handles the placing of the poison apples
def place_poison():
    j = randint(0, 1)
    if j == 1:
        spawn("poison", board)
        game.poison_count += 1


'''Collision detection functions'''


# Function handling if a player hits them self
def itself(player):
    if player.tail[0] in player.tail[1:]:
        player.dead = True
        # take 10 off of the person who dies first
        if not game.reduced:
            if game.twoPlayer:
                if player.size > 10:
                    player.size -= 10
                else:
                    player.size = 1
                game.reduced = True
        if not player.played:
            # Play a sound
            play_sound("Smash.wav")
            player.played = True


# Function handling if the players hit each other
def each_other(player1, player2):
    if player1.tail[0] in player2.tail:
        player1.dead = True

        # take 10 off of the person who dies first
        if not game.reduced:
            if game.twoPlayer:
                if player1.size > 10:
                    player1.size -= 10
                else:
                    player1.size = 1
                game.reduced = True

        if not player1.played:
            # Play a sound
            play_sound("Smash.wav")
            player1.played = True


'''Reset and game over functions'''


def sudden_death(array, player):
    distance = 5
    b = randint(0, 8)
    try:
        if b == 0:
            array[player.y - distance][player.x - distance] = PoisonTile()
        elif b == 1:
            array[player.y + distance][player.x - distance] = PoisonTile()
        elif b == 2:
            array[player.y - distance][player.x + distance] = PoisonTile()
        elif b == 3:
            array[player.y + distance][player.x + distance] = PoisonTile()
        elif b == 4:
            array[player.y - distance][player.x - distance] = PoisonTile()
        elif b == 5:
            array[player.y + distance][player.x] = PoisonTile()
        elif b == 6:
            array[player.y][player.x + distance] = PoisonTile()
        elif b == 7:
            array[player.y - distance][player.x] = PoisonTile()
        elif b == 8:
            array[player.y][player.x - distance] = PoisonTile()
        else:
            pass
    except IndexError:
        pass


#  Function that returns a value of text for the game over screen
def reset():

    p = 0
    list_scores = list()
    list_players = list()
    # create the vector

    for j in SNAKES:
        list_scores.append(j.get_score())

    list_scores.sort()
    for j in SNAKES:
        list_players.append(j)
        if list_players[p].get_score() == max(list_scores):
            winner = str(j)
            return winner + " won with a score of " + str(max(list_scores))
        p += 1
        # score = snake.score
        # score2 = snake_2.score
        # if game.twoPlayer:
        #     snake_score = "Player Green got a score of " + str(score) + " Player Blue got a score of " + str(score2)
        #
        #     return snake_score
        # else:
        #     your_score = "You got a score of " + str(score)
        #
        #     if score < 5:
        #         return str(your_score) + ". Lame dude... lame"
        #     elif 5 <= score < 10:
        #         return str(your_score) + ". Yeah well... its better than 5"
        #     elif 10 <= score < 20:
        #         return str(your_score) + ". I've seen better"
        #     elif 20 <= score < 30:
        #         return str(your_score) + ". That's pretty good!"
        #     elif 30 <= score < 40:
        #         return str(your_score) + ". Nice job!"
        #     elif 40 <= score < 50:
        #         return str(your_score) + ". Wow, so close to being awesome..."
        #     elif score >= 50:
        #         return str(your_score) + ". High score! Awesome"


# the function concerning the reset of all variables to their original values
def restart(player):
    player.score = 0
    player.size = 1
    player.dead = False
    player.tail = player.original_position
    player.direction = player.original_direction
    player.speed = player.original_speed
    player.saved = False
    spawn_all_apples()
    player.played = False
    pygame.mixer.stop()
    player.cheat = False
    pygame.draw.rect(screen, (0, 0, 0, 255), (0, 0, 4000, 1000), 0)
    game.reduced = False
    game.poison_count = 0
    game.paused = False


def home(player):
    player.score = 0
    player.size = 1
    player.dead = False
    player.tail = player.original_position
    player.direction = player.original_direction
    player.speed = player.original_speed
    player.saved = False
    spawn_all_apples()
    player.played = False
    game.twoPlayer = False
    pygame.mixer.stop()
    player.cheat = False
    pygame.draw.rect(screen, (0, 0, 0, 255), (0, 0, 4000, 1000), 0)
    game.wait = True
    game.reduced = False
    game.poison_count = 0
    game.paused = False


# Function for retrieving, sorting and displaying the highest four scores
def get_scores():
    with open('Scores.json') as data_file:
        data = json.load(data_file)

    count = 0
    # Bubble sort
    while count <= len(data['scores']):
        for x in range(0, (len(data['scores']) - 1)):
            if int(data['scores'][x]) > int(data['scores'][x + 1]):
                temp_var = data['scores'][x]
                data['scores'][x] = data['scores'][x + 1]
                data['scores'][x + 1] = temp_var
            x += 1
        count += 1

    # returns sliced data (the last four scores)
    return data['scores'][-4:]


# Function for saving the scores of the players
def save(player):
    if not player.saved:
        with open('Scores.json', 'r') as f:
            old_scores = json.load(f)

        # calculate the new score list
        new_scores = old_scores
        new_scores['scores'].append(snake.score)

        with open('Scores.json', 'w') as f:
            json.dump(new_scores, f)

        player.saved = True


# Function to update all snakes
def update_snake(ske: Snake):
    if not ske.dead:
        if ske.update_counter >= ske.speed:
            ske.move_snake()
            ske.update_counter = 0
        else:
            ske.update_counter += 1


# Rendering Function
def draw():
    # keeps the game from starting while the welcome screen is displayed
    if game.wait:
        get_scores()
        # Welcome screen
        display_box("Do you want to play with two players?", (0, 0))  # calls the display_box function to display text
        display_box("press y for or n for no ", (0, 50))
        display_box("Rules:", (0, 200))
        display_box("Get as big as you can", (0, 230))
        display_box("Apples are worth 1 point", (0, 260))
        display_box("Green gems are worth 5 points", (0, 290))
        display_box("Yellow gems speed you up and Blue gems slow you down", (0, 310))
        display_box("The skulls are poison! You lose 5 points. If you don't have 5 points to lose you die", (0, 340))
        display_box("Don't run into the walls", (0, 370))
        display_box("Don't run into yourself", (0, 400))
        display_box("If playing the two player version:", (0, 460))
        display_box("Don't run into each other", (0, 490))
        display_box("If you die first you lose 10 points", (0, 510))
        display_box("Other than that, same rules as before!", (0, 540))
        display_box("Controls:", (0, 610))
        display_box("Arrow keys for the green snake", (0, 640))
        display_box("W, A, S, D for the blue snake", (0, 670))
        display_box("Q to quit (only if you're not playing)", (0, 700))
        display_box("High scores: " + str(get_scores()), (0, 780))

    # Show the menu if the opponent is dead
    elif any([snke.dead for snke in SNAKES]):
        # Handle events when the snake is dead
        # Game over screen box
        pygame.draw.rect(screen, (0, 0, 0, 255), (0, 0, 600, 1000), 0)

        if game.twoPlayer:
            if snake.dead:
                display_box("Player Green Died!", (0, 0))
            else:
                display_box("Player Blue Died!", (0, 0))

        # Displays the text value returned by the reset function
        display_box(reset(), (0, 50))
        display_box("Press r to try again. q to quit, h for home", (0, 150))

        distance = 200
        # decide who got a higher score and say who won. tell them if their score is saved
        if snake.score > snake_2.score:
            if game.twoPlayer:
                display_box("Player Green won!", (0, 100))
            if snake.saved:
                display_box("Score saved!", (0, distance))
            else:
                display_box("Do you want to save your score, Player Green? If so press o", (0, distance))

        if snake_2.score > snake.score:
            if game.twoPlayer:
                display_box("Player Blue won!", (0, 100))
            if snake_2.saved:
                display_box("Score saved!", (0, distance))
            else:
                display_box("Do you want to save your score, Player Blue? If so press o", (0, distance))

    # make the game board
    elif not game.paused:
        # Makes a background of black
        screen.fill((0, 0, 0, 255))

        for y, array in enumerate(board):
            for x, symbol in enumerate(array):
                # draw the red lines
                pygame.draw.rect(screen, (128, 0, 64, 28),
                                 (x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT), 1)

                # Draw the images
                if symbol.image:
                    draw_image(x, y, symbol.image)

        # draw snakes
        for snk in SNAKES:
            for r, t in enumerate(snk.tail):
                x, y = t
                if r == 0:
                    # Draw head
                    change_snake(snk, x, y, "head")
                elif r == len(snk.tail)-1:
                        change_snake(snk, x, y, "tail")
                else:
                    # change_snake(s, x, y, "body")
                        pygame.draw.rect(screen, snk.color, (x * TILE_WIDTH, y * TILE_WIDTH, TILE_WIDTH, TILE_HEIGHT))

        # Displays the updating scores at eh top of the board while the game is running
        if game.twoPlayer:
            # Displays for both snakes
            display_box("Score Player Blue: " + str(snake_2.score), (0, 0))
            display_box("Score Player Green: " + str(snake.score), (1400, 0))
        else:
            # Displays fo one snake only
            display_box("Score: " + str(snake.score), (0, 0))

    pygame.display.flip()


# update function
def update_board():
    if game.paused or game.wait:
        return
    if game.poison_count < game.b:
        place_poison()

    if game.special_counter < 20:
        # random number of apples to spawn
        p = randint(0, 1)
        # random number to decide whether to spawn an apple or not
        t = randint(0, 3)
        # creating the apple
        for num in range(p):
            if t == 0:
                spawn("speed", board)
                game.special_counter += 1
            elif t == 2:
                spawn("slow", board)
                game.special_counter += 1
            elif t == 3:
                spawn("miracle", board)
                game.special_counter += 1

    if game.counter < 8:
        spawn("apple", board)
        game.counter += 1

    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if not tile.update():
                if isinstance(board[y][x], PoisonTile):
                    game.poison_count -= 1
                else:
                    game.special_counter -= 1
                board[y][x] = EmptyTile()
            for sk in SNAKES:
                itself(sk)
                if sk.tail and sk.tail[0] == (x, y):

                    tile.effect(sk)
                    if isinstance(board[y][x], PoisonTile):
                        game.poison_count -= 1
                    else:
                        game.special_counter -= 1
                    if isinstance(board[y][x], Apple):
                        game.counter -= 1
                    if not isinstance(board[y][x], BorderTile):
                        board[y][x] = EmptyTile()

        each_other(robot, snake)
        each_other(snake, robot)
    if game.twoPlayer:
        each_other(snake, snake_2)
        each_other(snake_2, snake)
        each_other(snake_2, robot)
        each_other(robot, snake_2)
    # # sudden_death(board, snake)
    snake.score = snake.size - 1
    snake_2.score = snake_2.size - 1
    robot.score = robot.size - 1


# calls the function to create the initial batch of apples
spawn_all_apples()


# loop that runs the update function and makeboard function
while True:
    # Receive input
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.KEYDOWN:
            # key controls for Snake 1
            if not game.paused:
                # Handling for keypress events affecting the snakes direction
                if event.key == pygame.K_LEFT:
                    if snake.direction != "Right":
                        snake.direction = "Left"
                if event.key == pygame.K_RIGHT:
                    if snake.direction != "Left":
                        snake.direction = "Right"
                if event.key == pygame.K_DOWN:
                    if snake.direction != "Up":
                        snake.direction = "Down"
                if event.key == pygame.K_UP:
                    if snake.direction != "Down":
                        snake.direction = "Up"

                # key controls for Snake 2
                if event.key == pygame.K_a:
                    if snake_2.direction != "Right":
                        snake_2.direction = "Left"
                if event.key == pygame.K_d:
                    if snake_2.direction != "Left":
                        snake_2.direction = "Right"
                if event.key == pygame.K_s:
                    if snake_2.direction != "Up":
                        snake_2.direction = "Down"
                if event.key == pygame.K_w:
                    if snake_2.direction != "Down":
                        snake_2.direction = "Up"

            # handling for other keypress events
            # Key control to pause
            if event.key == pygame.K_p:
                if not game.paused:
                    game.paused = True
                else:
                    game.paused = False

            if event.key == pygame.K_h:
                # Key to welcome screen and reset all the variables
                home(snake)
                home(snake_2)
                home(robot)
                # Key to go diagonal
            elif snake_2.cheat:
                snake_2.direction = "up_right"

            if event.key == pygame.K_r:
                restart(snake)
                restart(snake_2)
                restart(robot)

            if event.key == pygame.K_q:
                # Key to quit
                if snake.dead or snake_2.dead or game.wait:
                    quit()

            if event.key == pygame.K_y:
                game.wait = False
                game.twoPlayer = True
                SNAKES = [snake, snake_2]

            if event.key == pygame.K_n:
                game.wait = False
                SNAKES = [snake, robot]

            if event.key == pygame.K_x:
                snake.dead = True

            if event.key == pygame.K_o:
                # save the highest score out of all the players
                if snake.score < snake_2.score:
                    save(snake_2)
                if snake.score > snake_2.score:
                    save(snake)

            if event.key == pygame.K_SPACE:
                snake.size += 20

    # Mover the snakes and the robot
    if not game.paused and not game.wait and not any([s.dead for s in SNAKES]):
        for s in SNAKES:
            update_snake(s)
    move()

    game_timer = pygame.time
    game_timer.wait(1)
    update_board()

    # Render
    draw()
