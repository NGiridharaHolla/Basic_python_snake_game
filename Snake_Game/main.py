import pygame
from time import sleep
from pygame.locals import *
import random
SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3  #Multiple of 40 because picture is 40*40 in dimension
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0,24)*SIZE #screen size is 1000*800 so 1000/40=25 and 800/40=20
        self.y = random.randint(0,19)*SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpg').convert()  # Loading the Image\
        self.x = [SIZE] * length  #To create a snake of specified length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(SIZE)
        self.y.append(SIZE)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # Draw the image at given position i.e. (x,y)
        pygame.display.update()

    def move_left(self):
        if self.direction!='right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0]-= SIZE
        if self.direction == 'right':
            self.x[0]+= SIZE
        if self.direction == 'up':
            self.y[0]-= SIZE
        if self.direction == 'down':
            self.y[0]+= SIZE

        self.draw()

class Game :
    def __init__(self):
        pygame.init()  # Initialising the whole module
        pygame.display.set_caption('Basics Snake and apple game')
        pygame.mixer.init()  #To set background music
        self.background_music()
        self.surface = pygame.display.set_mode((1000, 800))  # Initialising window size
        self.surface.fill((110, 110, 5))  # setting background color
        self.snake = Snake(self.surface,1)  #Snake is inside game so create snake object inside game class
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 +SIZE:
            if y1 >= y2 and y1 < y2 +SIZE:
                return True

        return False

    def border_collision(self,x1,y1):
        if x1<=-1 or x1>=1001 or y1<=-1 or y1>=801:
            return True
        return False

    def increase_speed(self):
        sleep(0.2)

    def background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play_sound(self,snd):
        sound = pygame.mixer.Sound(f'resources/{snd}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load('resources/background.jpg')
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        """
          In snake we have walk function which will call draw() which in turn clear the screen so we have to draw the apple every time
        """
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # snake eating apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound('crash')
                raise Exception('Game over')

        # Snake colliding with the border
        if self.border_collision(self.snake.x[0],self.snake.y[0]):
            self.play_sound('crash')
            raise Exception('Game over')

        if ((self.snake.length-1)*10)>100:
            sleep(0.25)
        elif ((self.snake.length-1)*10)>180:
            sleep(0.18)
        else:
            sleep(0.3)

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        # font.render(self,text:str, antialias:bool,color,background
        score = font.render(f'Score : {(self.snake.length-1)*10}',True,(255,255,255))
        self.surface.blit(score,(800,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'Game is over!! Your score is {(self.snake.length-1)*10}',True,(255,255,255))
        self.surface.blit(line1,(200,300))

        line2 = font.render('To play again press Enter, To exit press Escape',True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.update()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)  # Snake is inside game so create snake object inside game class
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():  # Provides all the events like keystroke etc...
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()



if __name__ == "__main__":
    game = Game()
    game.run()

