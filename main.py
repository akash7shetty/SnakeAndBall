# SnakeAndBall
# Write logic for snake eating apple and display score

import pygame
from pygame.locals import *
import time
import random

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2,18)*SIZE
        self.y = random.randint(2,18)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("block.png").convert()
        self.direction = 'down'

        self.length = length
        self.x = [40]*length
        self.y = [40]*length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.sound_back()
        self.surface = pygame.display.set_mode((800, 700))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg=pygame.image.load("back.png")
        self.surface.blit(bg,(0,0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def reset(self):
        self.snake = Snake(self.surface, 1)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake_collides_with_apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.sound_play("ding")
            self.snake.increase_length()
            self.apple.move()

        #snake_colliding_with_the_boundries
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.sound_play("crash")
            raise "Hit the boundry error"
        
        #snake_collides_with_itself
        for i in range(2,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.sound_play("crash")
                raise "Game over!"   #exception
    def sound_back(self):
        bck=pygame.mixer.music.load("bg.mp3")
        pygame.mixer.music.play(-1,0)
    
    def sound_play(self,sound):
        media=pygame.mixer.Sound(f"{sound}.mp3")
        pygame.mixer.Sound.play(media)
                
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Your Score: {self.snake.length*2}",True,(255,255,255))
        self.surface.blit(score,(1000,800))
        pygame.display.flip()
    
    def show_game_over(self):
        font = pygame.font.SysFont('arial',30)
        pygame.mixer.music.pause()
        self.render_background()
        line1 = font.render(f"GAME OVER!!! Your Score was: {self.snake.length*2}",True,(255,255,255))
        self.surface.blit(line1,(300,300))
        line2 = font.render(f"To PLAY Again press Enter!! Press Escape to EXIT!!",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        
    def run(self):
        running=True
        pause=False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()
                
            time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()
