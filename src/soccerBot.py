import pygame

class SoccerBotGame():
  def __init__(self):
    pygame.init()

    self.win_width = 900
    self.win_height = 900

    self.win_background = (76, 133, 39) # Green
    self.player_color = (0,0,0) # Black
    self.ball_color = (0, 0, 0) # Black
    self.stripes_color = (255, 255, 255)

    self.gameWindow = pygame.display.set_mode((self.win_width, self.win_height))

    pygame.display.set_caption('Soccer Bot')

    # Player starting coordinates
    self.playerStartX = 30
    self.playerStartY = 30

    # Player coords
    self.playerCoordX = 30
    self.playerCoordY = 30

    # Player stats
    self.playerWidth = 20
    self.playerHeight = 30
    self.playerVelocity = 20
    self.playerCurrentDirection = (0,0)

    # Ball starting coordinates
    self.ballStartX = 100
    self.ballStartY = 100

    # Ball coords
    self.ballCoordX = 100
    self.ballCoordY = 100

    # Ball stats
    self.ballWidth = 10
    self.ballHeight = 10
    self.ballVelocity = 20

    # Counter to keep goal count
    self.score = 0

    # Init objects in scene
    self.updateFrame()

    # Program status flag
    self.run = True

  def updateFrame(self):
    self.gameWindow.fill(self.win_background)
    pygame.draw.rect(self.gameWindow, self.stripes_color, (500, 200, 400, 500), 10)
    self.goalArea = pygame.draw.rect(self.gameWindow, self.stripes_color, (850, 350, 50, 200))  # Goal area
    pygame.draw.circle(self.gameWindow, self.stripes_color, (500, 440), 40)

    # Update objects in the scene
    self.ball = pygame.draw.circle(self.gameWindow, self.ball_color, (self.ballCoordX, self.ballCoordY), self.ballWidth)
    self.player = pygame.draw.rect(self.gameWindow, self.player_color, (self.playerCoordX, self.playerCoordY, self.playerWidth, self.playerHeight))

    # Refresh window
    pygame.display.update()

  def updateKeys(self):
    keys = pygame.key.get_pressed()

    # For controlling the player
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
      self.playerCoordX += self.playerVelocity
      self.playerCoordY += self.playerVelocity
      self.playerCurrentDirection = (1,1)
    elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
      self.playerCoordX += self.playerVelocity
      self.playerCoordY -= self.playerVelocity
      self.playerCurrentDirection = (1,-1)
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
      self.playerCoordX -= self.playerVelocity
      self.playerCoordY += self.playerVelocity
      self.playerCurrentDirection = (-1,1)
    elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
      self.playerCoordX -= self.playerVelocity
      self.playerCoordY -= self.playerVelocity
      self.playerCurrentDirection = (-1,-1)
    elif keys[pygame.K_RIGHT]:
      self.playerCoordX += self.playerVelocity
      self.playerCurrentDirection = (1,0)
    elif keys[pygame.K_LEFT]:
      self.playerCoordX -= self.playerVelocity
      self.playerCurrentDirection = (-1,0)
    elif keys[pygame.K_UP]:
      self.playerCoordY -= self.playerVelocity
      self.playerCurrentDirection = (0,-1)
    elif keys[pygame.K_DOWN]:
      self.playerCoordY += self.playerVelocity
      self.playerCurrentDirection = (0,1)
    elif keys[pygame.K_ESCAPE]:
      self.run = False

    # For controlling the ball
    # if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
    #   self.kickBall((1,1), self.ballVelocity)
    # elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
    #   self.kickBall((1,-1), self.ballVelocity)
    # elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
    #   self.kickBall((-1,1), self.ballVelocity)
    # elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
    #   self.kickBall((-1,-1), self.ballVelocity)
    # elif keys[pygame.K_RIGHT]:
    #   self.kickBall((1,0), self.ballVelocity)
    # elif keys[pygame.K_LEFT]:
    #   self.kickBall((-1,0), self.ballVelocity)
    # elif keys[pygame.K_UP]:
    #   self.kickBall((0,-1), self.ballVelocity)
    # elif keys[pygame.K_DOWN]:
    #   self.kickBall((0,1), self.ballVelocity)
    # elif keys[pygame.K_ESCAPE]:
    #   self.run = False

  '''
  @param direction: Direction to kick the ball to
    (1,0) Right
    (0,1) Down
    (-1,0) Left
    (0,-1) Up
    (1, 1) Right-Down
    (1, -1) Right-Up
    (-1, 1) Left-Down
    (-1, -1) Left-Up
  @param strength: Velocity (Number of pixels to move)
  '''
  def kickBall(self, direction, strength): # Direction has to come as a vector (x, y)
    dirX = direction[0]
    dirY = direction[1]

    if dirX == 1: # Right
      if self.ballCoordX + strength > self.win_width:
        self.kickBall((-dirX, 0), strength) # Bounce
      else:
        self.ballCoordX += strength
    if dirX == -1:  # Left
      if self.ballCoordX - strength < 0:
        self.kickBall((-dirX, 0), strength) # If on bounds bounce
      else:
        self.ballCoordX -= strength
    
    if dirY == 1: # Down
      if self.ballCoordY + strength > self.win_height:
        self.kickBall((0, -dirY), strength) # Bounce
      else:
        self.ballCoordY += strength
    if dirY == -1:  # Up
      if self.ballCoordY - strength < 0:
        self.kickBall((0, -dirY), strength) # Bounce
      else:
        self.ballCoordY -= strength

  def resetBall(self):
    self.ballCoordX = self.ballStartX
    self.ballCoordY = self.ballStartY

  def detectCollisions(self):
    # Collision between player and ball
    if self.ball.colliderect(self.player):
      self.playerInteraction()
      print(f'Colission at Ball({self.ball.x}, {self.ball.y}) - Player({self.player.x}, {self.player.y})')
    
    # Collision between ball and goal area
    if self.ball.colliderect(self.goalArea):
      self.score += 1
      self.resetBall()
      print(f'Score: {self.score}')

  # Function to call when player collides with ball
  def playerInteraction(self):
    self.kickBall(self.playerCurrentDirection, self.ballVelocity * 2) # Testing

  def runGame(self):
    while self.run:
      pygame.time.delay(100)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.run = False

      self.updateKeys() # TODO when simulation is done, this should be commented

      self.detectCollisions()

      self.updateFrame()