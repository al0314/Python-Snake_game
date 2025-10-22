import pygame, sys, random
from pygame.math import Vector2

#definations
#VERMILLION = (227,66,52)
#BURGANDY= (128, 0, 32)
BLACK = (0,0,0)
WHITE = (255,255,255)





cell_size = 30
number_of_cell = 25
width = 750
height = 750


pygame.init()
score_font = pygame.font.Font("Graphics/digital-7.ttf",40)
screen = pygame.display.set_mode((cell_size*number_of_cell,cell_size*number_of_cell))


pygame.display.set_caption("space snake")
clock = pygame.time.Clock()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT #CUSTOM EVENT
pygame.time.set_timer(SNAKE_UPDATE,200)


class Food:
    def __init__(self):
        self.position = self.generate_random_cell()
        self.sound = pygame.mixer.Sound("Sounds/eat.mp3")
        print(f"Food position initialized at: {self.position}")

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size,cell_size, cell_size)
        screen.blit(food_surface,food_rect)

    @staticmethod
    def generate_random_cell():
        x = random.randint(1, number_of_cell - 1)
        y = random.randint(1, number_of_cell - 1)
        print(f'food position at{Vector2(x,y)}')
        return Vector2(x, y)


class Snake:
    def __init__(self):
        self.body = [Vector2(6,9),Vector2(5,9),Vector2(4,9)]
        self.direction = Vector2(1,0)

    def draw(self):
        for i in self.body:
            snake_rect = pygame.Rect(i.x*cell_size,i.y*cell_size,cell_size,cell_size)
            pygame.draw.rect(screen, WHITE, snake_rect,2,7)

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
        self.wall_wrapper()

    def game_over(self):
        self.snake.reset()
        self.score.score = 0


    def generate_random_pos(self):
        pos = self.food.generate_random_cell()
        if pos in self.snake.body:

            pos = self.food.generate_random_cell()
            return pos
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
            self.food.sound.play()
            self.eating_direction()
            self.food.position = self.generate_random_pos()

            self.food.draw()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            sound2 = pygame.mixer.Sound("Sounds/Sounds_wall.mp3")
            sound2.play()

            self.game_over()
    def wall_wrapper(self):
        print(f'wall_wrapper is working')
        snake_head = self.snake.body[0]
        if snake_head.x > width // cell_size: #right_side
            snake_head.x = 0
            self.snake.body.insert(0,snake_head)
            self.snake.body.pop(1)

        if snake_head.x < 0 : #left_side
            snake_head.x = width // cell_size - 1
            self.snake.body.insert(0,snake_head)
            self.snake.body.pop(1)

        if snake_head.y > height // cell_size: #(height (pixel) // cell_size = grid conversion)
            snake_head.y = 0
            self.snake.body.insert(0,snake_head)
            self.snake.body.pop(1)

        if snake_head.y < 0 :
            snake_head.y = height // cell_size - 1
            self.snake.body.insert(0,snake_head)
            self.snake.body.pop(1)


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

