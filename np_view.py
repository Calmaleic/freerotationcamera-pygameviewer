# TODO: Next time, need to seperate vertices from models into its own matrix for the camera perspective transformation
#       Then prepare the camera as necessary in case of multiple views.
#       Model(with assembly) -> View(Projection) -> Clipping -> Rasterization

# Free Rotation Camera

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import sys
import math
import operator
import pygame
import np_extras as npex
import np_matrices as npma
import np_camera as npca

pygame.init()

# Pygame attributes
screenSize = (1000, 1000)
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
fpsLimit = 60
windowTitle = "Search Visualizer"
pygame.display.set_caption(windowTitle)

font = 'comicsansms'
fontSize = round((screenSize[0] + screenSize[1]) * 0.01)
textFont = pygame.font.SysFont(font, fontSize)

worldLimit = (100, 100, 100)

pygame.display.set_caption("3D Camera")

def truncate3(vec):
  return (vec[0], vec[1])

# Purely taking information from wikipedia
def perspective(point, fov, aspect, znear, zfar):
  # Fix the point to matrix
  p = npma.tupleToMatrix(point)
  p = npma.grow(p, (1, 4))
  p[0][3] = 1

  # Projection matrix
  m = npma.zeroes((4, 4))
  m[0][0] = aspect * (1 / math.tan(fov / 2))
  m[1][1] = 1 / math.tan(fov / 2)
  m[2][2] = zfar / (znear - zfar)
  m[2][3] = (-(zfar * znear)) / (znear - zfar)
  m[3][2] = 1
  
  p = npma.multiplication(p, m)

  if p[0][3] != 0.0:
    p[0][0] /= p[0][3]
    p[0][1] /= p[0][3]
    p[0][2] /= p[0][3]

  p = npma.shrink(p, (1, 3))
  return npma.matrixToTuple(p)

def isometric(point):
  p = npma.tupleToMatrix(point)
  c1 = [[math.sqrt(3)/math.sqrt(6), 0, -math.sqrt(3)/math.sqrt(6)],
        [1/math.sqrt(6), 2/math.sqrt(6), 1/math.sqrt(6)],
        [math.sqrt(2)/math.sqrt(6), -math.sqrt(2)/math.sqrt(6), math.sqrt(2)]]
  c = npma.multiplication(p, c1)
  op = [[1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]]
  b = npma.multiplication(c, op)
  return npma.matrixToTuple(b)

def withinBounds(vec):
  return (True if vec[0] >= 0 and vec[0] < screenSize[0] and
                  vec[1] >= 0 and vec[1] < screenSize[1] else False)

# Creating a new camera to follow
worldCamera = npca.Camera((0, 0, 0), (5, 5), (0, 0, 0), 90) # World coordinates

# Coordinate Axis Classes
class Axis:
  def __init__(self):
    self.vertices = ((-worldLimit[0], 0, 0), (worldLimit[0], 0, 0), # X Axis 
                     (0, -worldLimit[1], 0), (0, worldLimit[1], 0), # Y Axis
                     (0, 0, -worldLimit[2]), (0, 0, worldLimit[2])) # Z Axis
    self.proj = npma.zeroes((6, 3))
    
    print(npma.getDimensions(self.vertices))
    print(npma.getDimensions(self.proj))

  def perp(self):
    for i, n in enumerate(self.vertices):
      p = npma.tupleToMatrix(n)
      rotx = [[1, 0, 0],
              [0, math.cos(worldCamera.eulerAngles[0]), -math.sin(worldCamera.eulerAngles[0])],
              [0, math.sin(worldCamera.eulerAngles[0]), math.cos(worldCamera.eulerAngles[0])]]

      roty = [[math.cos(worldCamera.eulerAngles[1]), 0, math.sin(worldCamera.eulerAngles[1])],
              [0, 1, 0],
              [-math.sin(worldCamera.eulerAngles[1]), 0, math.cos(worldCamera.eulerAngles[1])]]

      rotz = [[math.cos(worldCamera.eulerAngles[2]), -math.sin(worldCamera.eulerAngles[2]), 0],
              [math.sin(worldCamera.eulerAngles[2]), math.cos(worldCamera.eulerAngles[2]), 0],
              [0, 0, 1]]

      p = npma.multiplication(p, rotx)
      p = npma.multiplication(p, roty)
      p = npma.multiplication(p, rotz)

      # Shift by the current world camera position
      p = npma.operation(p, npma.tupleToMatrix(worldCamera.pos), operator.add)
      p = npma.matrixToTuple(p)

      # Perform Perspective Projection
      p = npex.worldToUnitCoordinates(p, worldLimit)
      p = perspective(p, 90, screenSize[0]/screenSize[1], 0, 100)
      if p[2] != 0:
        p = (p[0]/p[2], p[1]/p[2], p[2])
      p = npex.unitToWorldCoordinates(p, worldLimit)
      p = npex.worldToPixelCoordinates(screenSize, p, worldLimit)
      p = npex.cartesianToCom(screenSize, p)
      self.proj[i] = p

  def display(self):
    self.perp()
    pygame.draw.line(screen, (255, 0, 0), truncate3(self.proj[0]), truncate3(self.proj[1]), 5)
    pygame.draw.line(screen, (0, 255, 0), truncate3(self.proj[2]), truncate3(self.proj[3]), 5)
    pygame.draw.line(screen, (0, 0, 255), truncate3(self.proj[4]), truncate3(self.proj[5]), 5)

# New Cube Class
class Cube:
  def __init__(self, x):
    self.vertices = npma.getTwoExp(x, 3) # Unit Coordinates
    self.proj = npma.getTwoExp(x, 3)
    self.pos = (0, 0, 0)
    self.angle = (0, 0, 0)

  def connectEdge(self, vec1, vec2):
    if withinBounds(vec1) and withinBounds(vec2):
      pygame.draw.line(screen, (255, 255, 255), truncate3(vec1), truncate3(vec2), 2)

  def connectEdges(self):
    # (-1,-1,-1)
    self.connectEdge(self.proj[0], self.proj[2])
    self.connectEdge(self.proj[0], self.proj[4])
    self.connectEdge(self.proj[0], self.proj[1])
    # (1, 1, 1)
    self.connectEdge(self.proj[7], self.proj[5])
    self.connectEdge(self.proj[7], self.proj[3])
    self.connectEdge(self.proj[7], self.proj[6])
    # (1, 1, -1)
    self.connectEdge(self.proj[6], self.proj[4])
    self.connectEdge(self.proj[6], self.proj[2])
    # (-1, -1, 1)
    self.connectEdge(self.proj[1], self.proj[5])
    self.connectEdge(self.proj[1], self.proj[3])
    # (1 -1 -1)
    self.connectEdge(self.proj[4], self.proj[5])
    # (-1, 1, 1)
    self.connectEdge(self.proj[3], self.proj[2])
    
  def iso(self):
    for i in range(len(self.proj)):
      p = npex.worldToUnitCoordinates(self.proj[i], worldLimit)
      p = isometric(p)
      p = npex.unitToWorldCoordinates(p, worldLimit)
      p = npex.worldToPixelCoordinates(screenSize, p, worldLimit)
      p = npex.cartesianToCom(screenSize, p)
      self.proj[i] = p

  def perp(self):
    for i, n in enumerate(self.vertices):
      # Rotate the matrix
      p = npma.tupleToMatrix(n)
      #rotx = [[1, 0, 0],
      #        [0, math.cos(self.angle[0]), -math.sin(self.angle[0])],
      #        [0, math.sin(self.angle[0]), math.cos(self.angle[0])]]
      #
      #roty = [[math.cos(self.angle[1]), 0, math.sin(self.angle[1])],
      #        [0, 1, 0],
      #        [-math.sin(self.angle[1]), 0, math.cos(self.angle[1])]]
      #   
      #rotz = [[math.cos(self.angle[2]), -math.sin(self.angle[2]), 0],
      #        [math.sin(self.angle[2]), math.cos(self.angle[2]), 0],
      #        [0, 0, 1]]
      #
      #p = npma.multiplication(p, rotx)
      #p = npma.multiplication(p, roty)
      #p = npma.multiplication(p, rotz)
      #
      #self.angle = (self.angle[0]+0.001, self.angle[1]+0.001, self.angle[2]+0.001)
      #if self.angle[0] >= 360 or self.angle[1] >= 360 or self.angle[2] >= 360:
      #  self.angle = (0, 0, 0)
      #
      # Rotate the matrix by the camera angle in world space
      #p = npma.tupleToMatrix(p)
      rotx = [[1, 0, 0],
              [0, math.cos(worldCamera.eulerAngles[0]), -math.sin(worldCamera.eulerAngles[0])],
              [0, math.sin(worldCamera.eulerAngles[0]), math.cos(worldCamera.eulerAngles[0])]]

      roty = [[math.cos(worldCamera.eulerAngles[1]), 0, math.sin(worldCamera.eulerAngles[1])],
              [0, 1, 0],
              [-math.sin(worldCamera.eulerAngles[1]), 0, math.cos(worldCamera.eulerAngles[1])]]

      rotz = [[math.cos(worldCamera.eulerAngles[2]), -math.sin(worldCamera.eulerAngles[2]), 0],
              [math.sin(worldCamera.eulerAngles[2]), math.cos(worldCamera.eulerAngles[2]), 0],
              [0, 0, 1]]

      p = npma.multiplication(p, rotx)
      p = npma.multiplication(p, roty)
      p = npma.multiplication(p, rotz)

      # Shift by the current world camera position
      p = npma.operation(p, npma.tupleToMatrix(worldCamera.pos), operator.add)
      p = npma.matrixToTuple(p)

      # Perform Perspective Projection
      p = npex.worldToUnitCoordinates(p, worldLimit)
      p = perspective(p, 90, screenSize[0]/screenSize[1], 0, 100)
      p = (p[0]/p[2], p[1]/p[2], p[2])
      p = npex.unitToWorldCoordinates(p, worldLimit)
      p = npex.worldToPixelCoordinates(screenSize, p, worldLimit)
      p = npex.cartesianToCom(screenSize, p)
      self.proj[i] = p

  def display(self):
    self.perp()
    for n in self.proj: # Currently no clipping is applied so there may be issues with the z-buffer.
      pygame.draw.circle(screen, (255,255,255), n, 5)
    self.connectEdges()

# Handle User Input
def handleInput():
  # Handle Keyboard inputs
  key_input = pygame.key.get_pressed()
  # Camera movement
  if key_input[pygame.K_a]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0]+2, worldCamera.pos[1], worldCamera.pos[2])
  if key_input[pygame.K_s]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1]+2, worldCamera.pos[2])
  if key_input[pygame.K_d]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0]-2, worldCamera.pos[1], worldCamera.pos[2])
  if key_input[pygame.K_w]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1]-2, worldCamera.pos[2])
  if key_input[pygame.K_t]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1], worldCamera.pos[2]-2)
  if key_input[pygame.K_g]:
    print(worldCamera.pos)
    worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1], worldCamera.pos[2]+2)
  # Camera direction
  if key_input[pygame.K_u]:
    print(worldCamera.eulerAngles)
    if worldCamera.eulerAngles[0] < 360 or worldCamera.eulerAngles[1] < 360 or worldCamera.eulerAngles[2] < 360:
      worldCamera.eulerAngles = (worldCamera.eulerAngles[0]+0.01, worldCamera.eulerAngles[1], worldCamera.eulerAngles[2])
    else:
      worldCamera.eulerAngles = (0, worldCamera.eulerAngles[1], worldCamera.eulerAngles[2])
  if key_input[pygame.K_i]:
    print(worldCamera.eulerAngles)
    if worldCamera.eulerAngles[0] < 360 or worldCamera.eulerAngles[1] < 360 or worldCamera.eulerAngles[2] < 360:
      worldCamera.eulerAngles = (worldCamera.eulerAngles[0], worldCamera.eulerAngles[1]+0.01, worldCamera.eulerAngles[2])
    else:
      worldCamera.eulerAngles = (worldCamera.eulerAngles[0], 0, worldCamera.eulerAngles[2])
  if key_input[pygame.K_o]:
    print(worldCamera.eulerAngles)
    if worldCamera.eulerAngles[0] < 360 or worldCamera.eulerAngles[1] < 360 or worldCamera.eulerAngles[2] < 360:
      worldCamera.eulerAngles = (worldCamera.eulerAngles[0], worldCamera.eulerAngles[1], worldCamera.eulerAngles[2]+0.01)
    else:
      worldCamera.eulerAngles = (worldCamera.eulerAngles[0], worldCamera.eulerAngles[1], 0)

  # Handle Mouse Inputs
  mouse_input = pygame.mouse.get_pressed()
  if mouse_input[0] == 1: #Left Click
    mc = pygame.mouse.get_rel()
    worldCamera.eulerAngles = (worldCamera.eulerAngles[0] + (mc[1]*0.002), worldCamera.eulerAngles[1] + (mc[0]*0.002), worldCamera.eulerAngles[2])
  

axis = Axis()

cubes = []
for i in range(1, 8):
  cubes.append(Cube((-i*10, i*10)))

#for i, n in enumerate(npma.getTwoExp((-1, 1), 3)):
#  print(f"{i}: {n}")

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1: # Mouse left-click
        pygame.mouse.set_pos(pygame.mouse.get_pos()) # This is to reset the relative position so it can track only the current one
        print(pygame.mouse.get_rel())
      elif event.button == 4: # Mouse wheel up
        worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1], worldCamera.pos[2]+6)
      elif event.button == 5: # Mouse wheel down
        worldCamera.pos = (worldCamera.pos[0], worldCamera.pos[1], worldCamera.pos[2]-6)
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        pygame.mouse.set_pos(pygame.mouse.get_pos()) # This is to reset the relative position so it can track only the current one
        print(pygame.mouse.get_rel())
  
  handleInput()
  screen.fill((0, 0, 0))
  axis.display()
  for n in cubes:
    n.display()

  pygame.display.flip()
  clock.tick(fpsLimit)
  #break