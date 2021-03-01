import pygame
import sys
import random

pygame.init()
SIZE = 20

#MOVS RIGHT UP LEFT DOWN
movx = [SIZE, 0, -SIZE, 0]
movy = [0, -SIZE, 0, SIZE]

index = {
  pygame.K_RIGHT : 0,
  pygame.K_UP : 1,
  pygame.K_LEFT : 2,
  pygame.K_DOWN : 3
}

class snake():
  def __init__(self, height, width, speed):
    self.height = height
    self.width = width
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption('Snake')
    self.speed = speed
    self.direction = movx[0], movy[0]
    self.score = 0
    self.head = [(self.height/SIZE//2)*SIZE, (self.width/SIZE//2)*SIZE]
    self.food = []
    self.clock = pygame.time.Clock()
    self.snake = [self.head,[self.head[0]-SIZE, self.head[1]], [self.head[0]-2*SIZE, self.head[1]]]
    #self.screen.fill((200,0,0))
    self.generate_food()

  def game(self):
    directionaux = [0,0]
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        raise SystemExit("Gracias por jugar!")

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          raise SystemExit("Gracias por jugar!")
        directionaux = [movx[index[event.key]], movy[index[event.key]]]

    aux = self.move(directionaux)
    if self.check_move(aux):
      self.direction = directionaux

    aux = self.move(self.direction)
    self.head = aux
    self.snake.insert(0, self.head)

    if self.end_game():
      return True, self.score

    if self.head == self.food:
      self.score += 1
      self.generate_food()
    else:
      self.snake.pop()

    self.UI()
    self.clock.tick(self.speed)

    return False, self.score

  def UI(self):
    self.screen.fill((0,0,0))
    for i in self.snake:
      pygame.draw.rect(self.screen, (90,90,90), pygame.Rect((i[0], i[1]), ([SIZE]*2)));
    pygame.draw.rect(self.screen, (200,0,0), pygame.Rect((self.food[0], self.food[1]), ([SIZE]*2)));
    pygame.display.flip()

  def end_game(self):
    if self.head in self.snake[1:]:
      return True
    return self.head[0] < 0 or self.head[1] < 0 or self.head[0] >= self.width or self.head[1] >= self.height

  def check_move(self, position):
    if position in self.snake:
      return False
    return True

  def generate_food(self):
    x = random.randint(0, (self.width/SIZE - 1))
    y = random.randint(0, (self.height/SIZE - 1))
    self.food = [x*SIZE, y*SIZE]
    if self.food in self.snake:
      self.generate_food()

  def move(self, direction):
    x = self.head[0] + direction[0]
    y = self.head[1] + direction[1]
    return [x, y]

if __name__ == "__main__":
  game = snake(460, 680, 10)
  score = 0
  final = 0
  while 1:
    final, score = game.game()
    if final == True:
      break
  print("Score: ", score);
