# Please create a python program that asks a bowling team captain to enter scores from their latest 
# tournament between the USA, Jordan, and South Korea (or another country of your choosing). 
# There are Four bowlers from each team, and you must provide them with names (please hard-code 
# them). The scores must be between 0 and 300 for each bowler. Each bowler must have a score for 
# each game. Each team member will bowl one game, and games two and three will be random, 
# between 190 – 300.

# a. You must print each team and all bowlers (separated by the team). 
# i. Compute the average for each bowler (including the random game)
# ii. Compute the average for each team.
# iii. Display all of this information on the screen.
# b. You will add the scores for each team and determine the winning team.
# c. You will compute the average score for each team.
# d. You will determine which team is the overall winner.
# e. You will determine the top 3 bowlers by their averages and provide them with a Gold (1st 
# place), Silver (2nd place), or Bronze (3rd place) Olympic medal.

# Printout requirements:
# You will display each of the above accomplishments. 
# Make sure that the final figures are as integers.
# I grant you full creative rights to make any printout that displays all the data collected in any 
# form or fashion of your choosing. Bonus points will be awarded for well-presented data. 
# All judging is final, and please note that Doug does take bribes. ￿ 
from time import sleep
import random
import os
import threading

TEAM_POS = (1, 40)
PLAYER_POS = (3, 10)
POINTS_POS = (5, 10)

SHIFT_METER = (1, 14 + 1)
SPEED_METER = (2, 14 + 1)
SPIN_METER = (3, 14 + 1)

lane = []
for x in range(15):
  row = []
  for y in range(9):
    row.append(' ')
  lane.append(row)
pins = []

stop = False

shift = 0
speed = 0
spin = 0

playerBall = None

print('\x1b[?25l', end = '')

os.system("cls")

class Team:
  def __init__(self, name, players = []) -> None:
    self.name = name
    self.points = 0
    self.players = players

class Player:
  def __init__(self, name) -> None:
    self.name = name
    self.points = []
    self.average = 0
  
  def getavg(self):
    total = 0 
    for score in self.points:
      total += score
    self.average = total // len(self.points)

class Pin:
  def __init__(self, r, c, left = None, right = None, behind = None) -> None:
    self.row = r
    self.column = c
    self.left = left
    self.right = right
    self.behind = behind
    self.symbol = "l"

  def __repr__(self) -> str:
    return self.symbol

  def fall(self):
    print(f'\x1b[{self.row + 1};{self.column + 1 + 2}H', end = "")
    print('#', end = "", flush = True)
    sleep(0.1)
    print(f'\x1b[{self.row + 1};{self.column + 1 + 2}H', end = "")
    print('*', end = "", flush = True)
    sleep(0.1)
    print(f'\x1b[{self.row + 1};{self.column + 1 + 2}H', end = "")
    print(' ', end = "", flush = True)
  
  def knock(self, speed, spin):
    lane[self.row][self.column] = ' '
    self.fall()

    if speed >= 1:
      if spin > 0:
        if self.right != None:
          self.right.knock(speed/2, spin)
      elif spin < 0:
        if self.left != None:
          self.left.knock(speed/2, spin)
      else:
        if self.behind != None:
          self.behind.knock(speed/2, spin)

class Ball:
  def __init__(self, r, c, s, spin) -> None:
    self.row = r
    self.column = c
    self.speed = s
    self.spin = spin
    self.collided = False
    self.symbol = "o"
    self.draw()

  def reset(self, r, c, s, spin):
    self.row = r
    self.column = c
    self.speed = s
    self.spin = spin
    self.collided = False
    #
    self.draw()

  def draw(self):
    print(f'\x1b[{self.row + 1};{self.column + 1 + 2}H', end = "")
    print(self.symbol, end = "", flush = True)

  def undraw(self):
    print(f'\x1b[{self.row + 1};{self.column + 1 + 2}H', end = "")
    print(' ', end = "", flush = True)

  def move(self):
    # friction reduce speed
    self.speed /= 1
    # move forward
    self.row -= 1
    # apply spin (move left & right)
    self.column += self.spin

    # bounce of the walls
    if self.column < 0:
      self.column = 0
      self.spin = -1 * self.spin
      self.column += self.spin
    if self.column > 8:
      self.column = 8
      self.spin = -1 * self.spin
      self.column += self.spin
    
    # hit end
    if self.row < 0:
      self.collided = True
      return

    # hit pin
    if type(lane[self.row][self.column]) == Pin:
      self.collided = True
      lane[self.row][self.column].knock(self.speed, self.spin)       
  
  def roll(self):
    while True:
      self.undraw()
      self.move()

      if self.collided:
        break
      self.draw()

      sleep(1/self.speed)

def typewrite(text, start, border = False, author = '', delay = 0.1, dramaticPause = 0.1):
  if type(text) != str:
    text = str(text)
  row = start[0]
  column = start[1]
  string = ''
  length = len(text) + 5

  if border:
    top = ''
    if author == '':
      top = '╭' + '─'*length + '─╮'
    else:
      top = '╭─' + ' ' + author + ' ' + '─' * (length - ( len(author) + 3 )) + '─╮'

    for char in text:
      string += char
      print(f'\x1b[{start[0]    };{start[1]}H' + top , flush = True)
      print(f'\x1b[{start[0] + 1};{start[1]}H│ {string:{length}}│', flush = True)
      print(f'\x1b[{start[0] + 2};{start[1]}H╰' + '─'*length + '─╯', flush = True)
      print('\x1b[3A', end = '', flush = True)
      sleep(delay)
  else:
    for char in text:
      string += char
      print(f'\x1b[{start[0]};{start[1]}H', end = "")
      print(string, end = '', flush = True)
      sleep(delay)
  sleep(dramaticPause)

def setupPins():
  pin1 = Pin(0, 1)
  pin2 = Pin(0, 3)
  pin3 = Pin(0, 5)
  pin4 = Pin(0, 7)
  lane[0][1] = pin1
  lane[0][3] = pin2
  lane[0][5] = pin3
  lane[0][7] = pin4

  pin5 = Pin(1, 2, pin1, pin2)
  pin6 = Pin(1, 4, pin2, pin3)
  pin7 = Pin(1, 6, pin3, pin4)
  lane[1][2] = pin5
  lane[1][4] = pin6
  lane[1][6] = pin7

  pin8 = Pin(2, 3, pin5, pin6, pin2)
  pin9 = Pin(2, 5, pin6, pin7, pin3)
  lane[2][3] = pin8
  lane[2][5] = pin9

  pin10 = Pin(3, 4, pin8, pin9, pin6)
  lane[3][4] = pin10

  pins = [pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9, pin10]

def printLane():
  for row in range(15):
    if row == 0:
      print('╮', end = '')
    elif row == 14:
      print('╯', end = '')
    else:
      print('│', end = '')
    print('║', end = '')

    for item in lane[row]:
      print(item, end = '')
    
    print('║', end = '')
    if row == 0:
      print('╭')
    elif row == 14:
      print('╰')
    else:
      print('│')

def getInput():
  global stop
  junk = input()
  stop = True

def useMeter(meter_pos):
  global stop
  stop = False

  name = ''
  if meter_pos == SHIFT_METER:
    name = 'SHIFT'
  elif meter_pos == SPEED_METER:
    name = 'SPEED'
  elif meter_pos == SPIN_METER:
    name = 'SPIN'
  
  var = 3
  x = threading.Thread(target = getInput)
  x.start()

  while stop == False:
    if var < 8:
      var += 1
    else:
      var = 0

    print(f'\x1b[{meter_pos[0]};{meter_pos[1]}H', end = "")
    print(name + ':', var, end = '', flush = True)

    # jump to bar
    print(f'\x1b[{meter_pos[0]};{meter_pos[1] + 9}H', end = "")

    # clear bar
    print('\x1b[0K', end = '', flush = True)

    # draw bar
    for i in range(var):
      print('>', end = '', flush = True)
    
    sleep(1)
  return var

def resetPins():
  for pin in pins:
    lane[pin.row][pin.col] = pin

def resetMeters():
  print(f'\x1b[{SHIFT_METER[0]};{SHIFT_METER[1]}H', end = "")
  print('\x1b[0K', end = '', flush = True)
  print(f'\x1b[{SPEED_METER[0]};{SPEED_METER[1]}H', end = "")
  print('\x1b[0K', end = '', flush = True)
  print(f'\x1b[{SPIN_METER[0]};{SPIN_METER[1]}H', end = "")
  print('\x1b[0K', end = '', flush = True)

def shoot():
  resetMeters()
  global shift, speed, spin, playerBall
  shift = useMeter(SHIFT_METER)
  speed = useMeter(SPEED_METER)
  spin = useMeter(SPIN_METER)

  if playerBall == None:
    playerBall = Ball(14, shift, speed, spin)
  else:
    playerBall.reset(14, shift, speed, spin)
  playerBall.roll()

# canada players
brody = Player('Brody Eaton')
ryder = Player('Ryder Miller')
maximus = Player('Maximus Morrison')
griffin = Player('Griffin Scott')
# japan players
mihara = Player('Mihara Kado')
yamane = Player('Yamane Yasotaro')
eguchi = Player('Eguchi Norishige')
yukimura = Player('Yukimura Yoshiyuki')
# wsu players
isaac = Player('Isaac Bennett')
harley = Player('Harley Brooks')
max = Player('Max Nicholson')
colt = Player('Colt Daniels')

# teams
teamCAN = Team('CANADA', [brody, ryder, maximus, griffin])
teamJAP = Team('JAPAN', [mihara, yamane, eguchi, yukimura])
teamWSU = Team('WAYNE STATE', [isaac, harley, max, colt])

# random points for players
for player in teamCAN.players:
  for i in range(3):
    player.points.append(random.randint(190, 300))
  player.getavg()
for player in teamJAP.players:
  for i in range(3):
    player.points.append(random.randint(190, 300))
  player.getavg()

# display CAN and JAP
typewrite('TEAM:' + teamCAN.name, TEAM_POS)

for i in range(len(teamCAN.players)):
  typewrite(teamCAN.players[i].name, (PLAYER_POS[0], PLAYER_POS[1] + i * 20))

for game in range(len(teamCAN.players[0].points) + 1):
  for player in range(len(teamCAN.players)):
    # print scores and averages
    if game == 3:
      typewrite(teamCAN.players[player].average, (POINTS_POS[0] + game, POINTS_POS[1] + player * 20))
    else:
      typewrite(teamCAN.players[player].points[game], (POINTS_POS[0] + game, POINTS_POS[1] + player * 20))






# enter team WSU scores

# play

# display WSU scores

# podium


# setupPins()
# printLane()

# for i in range(3):
#   shoot()

