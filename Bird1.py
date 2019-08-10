import pygame
import random
import os

pygame.mixer.init()
x = pygame.init()


# colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg = pygame.image.load('back_wallpaper.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
front_img = pygame.image.load('front.jpg')
front_img = pygame.transform.scale(front_img, (screen_width, screen_height)).convert_alpha()
back_img = pygame.image.load('back.jpg')
back_img = pygame.transform.scale(back_img, (screen_width, screen_height)).convert_alpha()


# Game title
pygame.display.set_caption("MY FIRST GAME : SNAKE BOARD")
pygame.display.update()


# initializations
clock = pygame.time.Clock()
font = pygame.font.SysFont('None', 55)


# function to display score on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(front_img, (0, 0))
        text_screen("WELCOME TO SNAKES", white, 250, 260)
        text_screen("PRESS SPACE BAR TO PLAY", white, 220, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back_music_naagin.mp3')
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(60)


# Creating a game loop
def game_loop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 30
    fps = 60
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if Highscore file exist
    if not os.path.exists("Highscore.txt"):
        with open("Highscore.txt", "w") as f:
            f.write(0)
    with open("Highscore.txt", "r") as f:
        Highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5

    while not exit_game:
        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(Highscore))
            gameWindow.fill(white)
            gameWindow.blit(back_img, (0, 0))
            text_screen("LOL..GAME OVER! PRESS ENTER TO CONTINUE", white, 10, 250)
            text_screen("YOUR SCORE : " + str(score), white, 50, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                if score > int(Highscore):
                    Highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("SCORE: " + str(score) + "  HIGHSCORE: " + str(Highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            # head is just to appear a block of snake head at the starting of the game as the list is empty at the very beginning
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('back_music.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('back_music.mp3')
                pygame.mixer.music.play()

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, (32, 43, 10), snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
welcome()
