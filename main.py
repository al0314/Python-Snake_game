import pygame, sys, random
from pygame.math import Vector2

#definations
#VERMILLION = (227,66,52)
#BURGANDY= (128, 0, 32)
BLACK = (0,0,0)
WHITE = (255,255,255)





cell_size = 30
number_of_cell = 25


pygame.init()
score_font = pygame.font.Font("Graphics/digital-7.ttf",32)
screen = pygame.display.set_mode((cell_size*number_of_cell,cell_size*number_of_cell))
pygame.display.set_caption("Retroid snake")
clock = pygame.time.Clock()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT #CUSTOM EVENT
pygame.time.set_timer(SNAKE_UPDATE,200)


class Food:
    def __init__(self):
        self.position = self.generate_random_cell()
    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size,self.position.y * cell_size,cell_size,cell_size)
        screen.blit(food_surface,food_rect)
    def generate_random_cell(self):
        x = random.randint(0, 24)
        y = random.randint(0, 24)
        return Vector2(x, y)


class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)
    def draw(self):
        for i in self.body:
            snake_rect = pygame.Rect(i.x*cell_size,i.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(screen, WHITE, snake_rect,4,7)

    def update(self):
        self.body = self.body[:-1]
        self.body.insert(0,self.body[0]+self.direction)


    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Score:
    def __init__(self):
        self.score = 0

    def score_up(self):
        self.score += 1

    def draw(self):
        score_surface = score_font.render(str(self.score), True, WHITE)
        screen.blit(score_surface, (10,10))


class Game:
    def __init__(self):
        self.food = Food()
        self.snake = Snake()
        self.score = Score()

    def draw(self):
        self.food.draw()
        self.snake.draw()
        self.score.draw()

    def update(self):
        self.snake.update()
        self.eat()
        self.check_collision_with_tail()

    def game_over(self):
        self.snake.reset()
        self.score.score = 0


    def generate_random_pos(self):
        pos = self.food.generate_random_cell()
        if pos in self.snake.body:
            self.food.generate_random_cell()
        else:
            return pos

    def eating_direction(self):
        if self.snake.direction == Vector2(1,0):
            self.snake.body.insert(0,self.snake.body[0]+Vector2(1,0))
        if self.snake.direction == Vector2(-1,0):
            self.snake.body.insert(0,self.snake.body[0]+Vector2(-1,0))

        if self.snake.direction == Vector2(0,-1):
            self.snake.body.insert(0, self.snake.body[0] + Vector2(0,-1))
        if self.snake.direction == Vector2(0,1):
            self.snake.body.insert(0, self.snake.body[0] + Vector2(0,1))



    def eat(self):
        if self.food.position == self.snake.body[0]:
            self.score.score_up()
            self.eating_direction()
            self.food.position = self.generate_random_pos()

            self.food.draw()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()


#Drawing
#food = Food()
#snake = Snake()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP  and game.snake.direction != Vector2(0,1) :
                game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    game.draw()
    pygame.display.update()
    clock.tick(60)

