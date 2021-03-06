import pygame
import sys
import random
import numpy as np

pygame.init()
SIZE = 20

#MOVS RIGHT UP LEFT DOWN
movx = [1, 0, -1, 0]
movy = [0, -1, 0, 1]

dx = [1, 0, 1, -1, 0, -1, 1, -1]
dy = [0, 1, 1, 0, -1, -1, -1, 1]

index = {
  pygame.K_RIGHT : 0,
  pygame.K_UP : 1,
  pygame.K_LEFT : 2,
  pygame.K_DOWN : 3
}

INF = 34

class snake():
  def __init__(self, height, width, speed):
    INF = max(width//SIZE, height//SIZE)
    self.map = [[0]*(width//SIZE) for i in range(height//SIZE)]
    self.height = height
    self.width = width
    self.speed = speed
    self.food = [0, 0]
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption('Snake')
    self.clock = pygame.time.Clock()

  def restart(self, NN):
    self.cont = 100
    self.NN = NN
    self.direction = movx[0], movy[0]
    self.score = 0

    self.head = [(self.width//SIZE)//2, (self.height//SIZE)//2]
    self.snake = [self.head,[self.head[0]-1, self.head[1]], [self.head[0]-2, self.head[1]]]

    for i in self.map:
      self.map[i[1]][i[0]] = 0
    for pos in self.snake:
      self.map[pos[1]][pos[0]] = 1
    self.generate_food()

  def game(self):
    self.cont -= 1
    directionaux = self.direction
    # for event in pygame.event.get():
    #   if event.type == pygame.QUIT:
    #     raise SystemExit("Gracias por jugar!")

    #   if event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_ESCAPE:
    #       raise SystemExit("Gracias por jugar!")
    #     directionaux = [movx[index[event.key]], movy[index[event.key]]]

    directionaux = self.get_move()
    aux = self.move(directionaux)
    if self.check_move(aux):
      self.direction = directionaux

    aux = self.move(self.direction)
    self.head = aux
    self.snake.insert(0, self.head)

    if self.head == self.food:
      self.score += 1
      self.generate_food()
      self.cont = min(self.cont+100, 500)
    else:
      pos = self.snake[-1]
      self.map[pos[1]][pos[0]] = 0
      self.snake.pop()

    if self.end_game():
      return True, self.score, self.cont
    self.map[aux[1]][aux[0]] = 1

    self.UI()
    self.clock.tick(self.speed)

    return False, self.score, self.cont

  def UI(self):
    self.screen.fill((0,0,0))
    for i in self.snake:
      pygame.draw.rect(self.screen, (90,90,90), pygame.Rect((i[0]*SIZE, i[1]*SIZE), ([SIZE]*2)))
    pygame.draw.rect(self.screen, (200,0,0), pygame.Rect((self.food[0]*SIZE, self.food[1]*SIZE), ([SIZE]*2)))
    pygame.display.flip()

  def end_game(self):
    if self.head in self.snake[1:] or self.cont == 0:
      return True
    return self.head[0] < 0 or self.head[1] < 0 or self.head[0] >= self.width//SIZE or self.head[1] >= self.height//SIZE

  def check_move(self, position):
    if position == self.snake[1]:
      return False
    return True

  def get_move(self):
    IN = self.get_input()
    pos = np.argmax(self.NN.predict(IN)[0])
    return [movx[pos], movy[pos]]
  
  def get_input(self):
    ans = [INF]*24

    for i in range(1, max(self.width//SIZE, self.height//SIZE)):
      for j in range(8):
        x = self.head[0]+dx[j]*i
        y = self.head[1]+dy[j]*i

        if(self.check_range(x, y) and self.map[y][x]):
          ans[self.map[y][x]*8 + j] = min(ans[self.map[y][x]*8 + j], i)

        if(not self.check_range(x, y)):
          ans[j] = min(ans[j], i)

    return np.array([ans])/INF

  def check_range(self, x, y):
    return 0 <= x < self.width//SIZE and 0 <= y < self.height//SIZE

  def generate_food(self):
    while True:
      x = random.randint(0, (self.width//SIZE - 1))
      y = random.randint(0, (self.height//SIZE - 1))
      self.food = [x, y]
      if not self.food in self.snake:
        self.map[y][x] = 2
        break

  def move(self, direction):
    x = self.head[0] + direction[0]
    y = self.head[1] + direction[1]
    return [x, y]

if __name__ == "__main__":
  game = snake(460, 680, 120)
  score = 0
  final = 0
  while 1:
    final, score = game.game()
    if final == True:
      break
  print("Score: ", score)
