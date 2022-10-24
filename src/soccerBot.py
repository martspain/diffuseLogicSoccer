import pygame
import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint
from skfuzzy import control as ctrl

class SoccerBotGame():
  def __init__(self):
    pygame.init()

    self.win_width = 900 # DO NOT CHANGE
    self.win_height = 900 # DO NOT CHANGE

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
    self.playerCurrentDirection = (0, 0)

    # Ball starting coordinates
    self.ballStartX = 100
    self.ballStartY = randint(100, 800)

    # Ball coords
    self.ballCoordX = 100
    self.ballCoordY = 100

    # Ball stats
    self.ballWidth = 10
    self.ballHeight = 10
    self.ballVelocity = 20

    # Direction to the goal from the player
    self.goalDirection = (0, 0)

    # Counter to keep goal count
    self.score = 0

    # ---------------- CRISP VARIABLES ----------------

    # Fuzzy logic antecednets (inputs)
    self.location = ctrl.Antecedent(np.arange(0, 70, 1), 'location')  
   
    self.distance = ctrl.Antecedent(np.arange(0, 70, 1), 'distance')  
    self.speed = ctrl.Antecedent(np.arange(0, 250, 5), 'speed')
    
    # Fuzzy logic consequents (outputs) 
    self.coordenates = ctrl.Consequent(np.arange(-20, 5, 1), 'coordenates')
    self.force = ctrl.Consequent(np.arange(-20, 5, 1), 'force')

    #  ---------------- LINGUISTIC VARIABLES ----------------
    # find the ball
    self.location['left'] = fuzz.trimf(self.location.universe, [0, 0, 70])
    self.location['right'] = fuzz.trimf(self.location.universe, [0, 0, 70])
    self.location['up'] = fuzz.trimf(self.location.universe, [0, 70, 70]) 
    self.location['down'] = fuzz.trimf(self.location.universe, [0, 70, 70]) 

    self.coordenates['x'] = fuzz.trimf(self.coordenates.universe, [-20, -20, -10])
    self.coordenates['y'] = fuzz.trimf(self.coordenates.universe, [-15, -10, -5])
    
    # force to kick ball
    self.speed['slow'] = fuzz.trimf(self.speed.universe, [0, 10, 20])
    self.speed['medium'] = fuzz.trimf(self.speed.universe, [15, 25, 40])
    self.speed['fast'] = fuzz.trimf(self.speed.universe, [35, 50, 60])

    self.distance['close'] = fuzz.trimf(self.distance.universe, [0, 0, 20])
    self.distance['middle'] = fuzz.trimf(self.distance.universe, [10, 40, 80])
    self.distance['far'] = fuzz.trimf(self.distance.universe, [150, 250, 250])

    self.force['low'] = fuzz.trimf(self.force.universe, [0, 0, 5])
    self.force['mid'] = fuzz.trimf(self.force.universe, [0, 5, 10])
    self.force['high'] = fuzz.trimf(self.force.universe, [5, 10, 10])

    self.forceRules = [
      ctrl.Rule(self.speed['slow'] & self.distance['close'] | self.distance['middle'] | self.distance['far'], self.force['high']),
      ctrl.Rule(self.speed['medium'] & self.distance['close'] | self.distance['middle'] | self.distance['far'], self.force['mid']),
      ctrl.Rule(self.speed['fast'] & self.distance['close'] | self.distance['middle'] | self.distance['far'], self.force['low']),
    ]

    self.coordRules = [
      ctrl.Rule(self.location['left'], self.coordenates['x']),
      ctrl.Rule(self.location['right'], self.coordenates['x']),

      ctrl.Rule(self.location['down'], self.coordenates['y']),
      ctrl.Rule(self.location['up'], self.coordenates['y']),
    ]

    self.coordSystem = ctrl.ControlSystem(self.coordRules)
    self.coordSim = ctrl.ControlSystemSimulation(self.coordSystem)

    self.forceSystem = ctrl.ControlSystem(self.forceRules)
    self.forceSim = ctrl.ControlSystemSimulation(self.forceSystem)

    # self.speed.view()
    # self.location.view()
    # self.coordenates.view()
    # self.distance.view()
    # self.force.view()
  
    # Graphic -> find the ball
    self.location.view()
    plt.title('Function to find the ball')

    # Grapic -> force to kick ball 
    self.force.view()
    plt.title('Force to kick the ball')
    plt.show()

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

    # Score label
    white = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', 32)
    font2 = pygame.font.Font('freesansbold.ttf', 20)

    textScore = font.render(f'Score: {self.score}', True, white)
    self.gameWindow.blit(textScore, (1,110))
    
    # player coordinates
    playerLabel = font2.render(f'Player coordinates : {self.player.x}, {self.player.y}', True, white)
    self.gameWindow.blit(playerLabel, (1,20))

    # ball coordinates
    ballLabel = font2.render(f'Ball coordinates: {self.ball.x}, {self.ball.y}', True, white)
    self.gameWindow.blit(ballLabel, (1,50))

    # goal coordinates
    goalLabel = font2.render(f'Goal coordinates: {self.goalArea}', True, white)
    self.gameWindow.blit(goalLabel, (1,80))

    # Refresh window
    pygame.display.update()

  def updateKeys(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
      self.run = False

    # # For controlling the player
    # if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
    #   self.playerCoordX += self.playerVelocity
    #   self.playerCoordY += self.playerVelocity
    #   self.playerCurrentDirection = (1,1)
    # elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
    #   self.playerCoordX += self.playerVelocity
    #   self.playerCoordY -= self.playerVelocity
    #   self.playerCurrentDirection = (1,-1)
    # elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
    #   self.playerCoordX -= self.playerVelocity
    #   self.playerCoordY += self.playerVelocity
    #   self.playerCurrentDirection = (-1,1)
    # elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
    #   self.playerCoordX -= self.playerVelocity
    #   self.playerCoordY -= self.playerVelocity
    #   self.playerCurrentDirection = (-1,-1)
    # elif keys[pygame.K_RIGHT]:
    #   self.playerCoordX += self.playerVelocity
    #   self.playerCurrentDirection = (1,0)
    # elif keys[pygame.K_LEFT]:
    #   self.playerCoordX -= self.playerVelocity
    #   self.playerCurrentDirection = (-1,0)
    # elif keys[pygame.K_UP]:
    #   self.playerCoordY -= self.playerVelocity
    #   self.playerCurrentDirection = (0,-1)
    # elif keys[pygame.K_DOWN]:
    #   self.playerCoordY += self.playerVelocity
    #   self.playerCurrentDirection = (0,1)
    # elif keys[pygame.K_ESCAPE]:
    #   self.run = False

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

  # FUZZY SIMULATIONS

  def calculateCoordenates(self, location):
    self.coordSim.input['location'] = location
    self.coordSim.compute()
    return self.coordSim.output['coordenates']

  def calculateForce(self, distance, speed):
    self.forceSim.input['distance'] = distance
    self.forceSim.input['speed'] = speed
    self.forceSim.compute()
    return self.forceSim.output['force']

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
    self.ballCoordY = randint(100, 800)

  def detectCollisions(self):
    # Collision between player and ball
    if self.ball.colliderect(self.player):
      self.playerInteraction()
    
    # Collision between ball and goal area
    if self.ball.colliderect(self.goalArea):
      self.score += 1
      self.resetBall()

  # Function to call when player collides with ball
  def playerInteraction(self):
    # Calc force to hit the ball
    playerCoords = (self.player.x, self.player.y)
    ballCoords = (self.ball.x, self.ball.y)
    dist = self.getDistanceToBall(playerCoords, ballCoords)
    forceToHit = abs(self.calculateForce(dist, self.playerVelocity))

    # Update goal direction
    self.getGoalDirection()

    # Kick ball
    self.kickBall(self.goalDirection, self.ballVelocity * forceToHit) # Testing

  def getDistanceToBall(self, a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

  def getGoalDirection(self):
    ballX = self.ball.x
    ballY = self.ball.y
    goalX = [850, 900]
    goalY = [350, 550]

    # Ball is on the left
    if ballX < goalX[0]:
      self.goalDirection = (1, self.goalDirection[1])
    
    # Ball is up
    if ballY < goalY[0]:
      self.goalDirection = (self.goalDirection[0], 1)

    # Ball is down
    elif ballY > goalY[1]:
      self.goalDirection = (self.goalDirection[0], -1)

  def lookForBall(self):
    # Calc distance from player to ball
    playerCoords = (self.player.x, self.player.y)
    ballCoords = (self.ball.x, self.ball.y)
    
    deltaX = playerCoords[0] - ballCoords[0]
    deltaY = playerCoords[1] - ballCoords[1]
    
    ### X Coords ###
    # Player is on the right
    if deltaX > 0:
      self.playerCurrentDirection = (-1, self.playerCurrentDirection[1])
    # Player is on the left
    elif deltaX < 0:
      self.playerCurrentDirection = (1, self.playerCurrentDirection[1])
    
    ### Y Coords ###
    # Player is down
    if deltaY > 0:
      self.playerCurrentDirection = (self.playerCurrentDirection[0], -1)
    # Player is up
    elif deltaY < 0:
      self.playerCurrentDirection = (self.playerCurrentDirection[0], 1)
    
    self.movePlayer()
      
  def movePlayer(self):
    self.playerCoordX += self.playerCurrentDirection[0] * self.playerVelocity
    self.playerCoordY += self.playerCurrentDirection[1] * self.playerVelocity

  def runGame(self):
    while self.run:
      pygame.time.delay(100)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.run = False

      self.updateKeys()

      self.lookForBall()

      self.detectCollisions()

      self.updateFrame()
