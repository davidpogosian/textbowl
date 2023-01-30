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
import concurrent.futures

screen = \
'''
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ╭───────────────────────────────────────────────────────────────────────────────────────────╮ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ |                                                                                           │ ┃
┃ ╰───────────────────────────────────────────────────────────────────────────────────────────╯ ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                        ╱╱		╲╲
'''

TEAM_POS = (1 + 4, 45)
PLAYER_POS = (3 + 4, 15)
POINTS_POS = (5 + 6, 15)
LABEL_POS = (5 + 6, 0 + 5)

# enter position adjustment here
LANE_REF = (3, 10)

# top left corner of the lane
LANE_REF = (LANE_REF[0] + 1, LANE_REF[1] + 3) # adjust for 1 based index and decor

SHIFT_METER = (LANE_REF[0]    , 12 + LANE_REF[1])
SPEED_METER = (1 + LANE_REF[0], 12 + LANE_REF[1])
SPIN_METER =  (2 + LANE_REF[0], 12 + LANE_REF[1])

MESSAGE_POS = (20, 30)

PLAYER_PODIUM = (5, 50)
TEAM_PODIUM = (9, 50)


lane = {}
for x in range(LANE_REF[0], 15 + LANE_REF[0]):
  for y in range(LANE_REF[1], 9 + LANE_REF[1]):
    lane[(x,y)] = ' '

stop = False

shift = 0
speed = 0
spin = 0

playerBall = None

os.system('cls')

print('\x1b[?25l', end = '')

class Team:
  def __init__(self, name, players = []) -> None:
    self.name = name
    self.points = 0
    self.players = players
    self.avg = 0
  def getavg(self):
    sum = 0
    for player in self.players:
      for score in player.points:
        sum += score
    self.avg = sum // 12
  def gettotal(self):
    total = 0
    for player in self.players:
      for score in player.points:
        total += score
    self.points = total

class Player:
  def __init__(self, name, pos = (20, 1)) -> None:
    self.name = name
    self.points = []
    self.avg = 0

    self.position = pos
    self.hair = random.choice([',,,', '...', '>>>', '///'])
    self.eye = random.choice(['^', '*', '.'])
    self.mouth = random.choice(['-', 'w', 'o', 'O'])
    self.body = random.choice(['() )', '[] ]'])
    self.leg = random.choice(['┋', '║', '┃'])
    self.rest = None
    self.walk1 = None
    self.walk2 = None
    self.generateframes()

  def generateframes(self):
    self.rest = \
    f''' {self.hair}
({self.eye}{self.mouth}{self.eye})
{self.body}
 {self.leg}{self.leg}
 ┗┗
'''
    self.walk1 = \
    f''' {self.hair}
({self.eye}{self.mouth}{self.eye})
{self.body}
//\\\\
┗   ┗
'''
    self.walk2 = \
    f''' {self.hair}
({self.eye}{self.mouth})
{self.body}
 {self.leg}
 ┗
'''
    self.dance1 = \
    f'''  {self.hair}
 ({self.eye}{self.mouth}{self.eye})
.() )-.
  {self.leg}{self.leg}
  ┗┗
    '''
    self.dance3 = \
    f'''  {self.hair}
 ({self.eye}{self.mouth}{self.eye})
v() )^
  {self.leg}{self.leg}
  ┗┗
    '''
    self.dance4 = \
    f'''  {self.hair}
 ({self.eye}{self.mouth}{self.eye})
^() )v
  {self.leg}{self.leg}
  ┗┗
    '''
    self.dance2 = \
    f'''  {self.hair}
 ({self.eye}{self.mouth}{self.eye})
.-() ).
  {self.leg}{self.leg}
  ┗┗
    '''
  
  def draw(self, pose, onlyhead = False):
    parts = pose.split('\n')
    for i in range(len(parts) if not onlyhead else 2):
      print(f'\x1b[{self.position[0] + i};{self.position[1]}H' + parts[i], end = "", flush = True)
  
  def erase(self):
    for i in range(6):
      print(f'\x1b[{self.position[0] + i};{self.position[1]}H' + '     ', end = "", flush = True)

  def spawn(self):
    self.draw(self.rest)
      
  def walk(self, distance):
    steps = 0
    self.erase()
    while distance > 0:   
      self.draw(self.walk1 if steps % 2 == 0 else self.walk2)
      sleep(0.3)
      self.erase()
      self.position = (self.position[0], self.position[1] + 1)
      steps += 1
      distance -= 1
    self.draw(self.rest)

  def dance(self):
    x = 100
    while x > 0:
      self.erase()
      self.draw(self.dance1)
      sleep(0.3)
      self.erase()
      self.draw(self.dance2)
      sleep(0.3)
      self.erase()
      self.draw(self.dance3)
      sleep(0.3)
      self.erase()
      self.draw(self.dance4)
      sleep(0.3)
      x -= 1
  
  def getavg(self):
    sum = 0 
    for score in self.points:
      sum += score
    self.avg = sum // 3

class Pin:
  def __init__(self, r, c, left = None, right = None, behind = None) -> None:
    self.row = r
    self.column = c
    self.left = left
    self.right = right
    self.behind = behind
    self.symbol = "l"
    self.knocked = False

  def __repr__(self) -> str:
    return self.symbol

  def fall(self):
    print(f'\x1b[{self.row};{self.column}H', end = "")
    print('#', end = "", flush = True)
    sleep(0.1)
    print(f'\x1b[{self.row};{self.column}H', end = "")
    print('*', end = "", flush = True)
    sleep(0.1)
    print(f'\x1b[{self.row};{self.column}H', end = "")
    print(' ', end = "", flush = True)
  
  def knock(self, ball, speed, spin):
    self.knocked = True
    ball.pins += 1
    lane[(self.row, self.column)] = ' '
    self.fall()

    if speed >= 1:
      if self.right is not None:
        if not self.right.knocked:
          self.right.knock(ball, speed/2, spin)
      if self.left is not None:
        if not self.left.knocked:
          self.left.knock(ball, speed/2, spin)
      if self.behind is not None:
        if not self.behind.knocked:
          self.behind.knock(ball, speed/2, spin)

class Ball:
  def __init__(self, r, c, s, spin) -> None:
    self.row = r
    self.column = c
    self.speed = s
    self.spin = spin
    self.collided = False
    self.symbol = "o"
    self.pins = 0
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
    print(f'\x1b[{self.row};{self.column}H', end = "")
    print(self.symbol, end = "", flush = True)

  def undraw(self):
    print(f'\x1b[{self.row};{self.column}H', end = "")
    print(' ', end = "", flush = True)

  def move(self):
    # friction reduce speed
    self.speed /= 1
    # move forward
    self.row -= 1
    # apply spin (move left & right)
    self.column += self.spin

    # bounce of the walls
    if self.column < LANE_REF[1]:
      self.column = LANE_REF[1]
      self.spin = -1 * self.spin
      self.column += self.spin
    if self.column > LANE_REF[1] + 8:
      self.column = LANE_REF[1] + 8
      self.spin = -1 * self.spin
      self.column += self.spin
    
    # hit end
    if self.row < LANE_REF[0]:
      self.collided = True
      return

    # hit pin
    if type(lane[(self.row, self.column)]) == Pin:
      self.collided = True
      lane[(self.row, self.column)].knock(self, self.speed, self.spin)       
  
  def roll(self):
    while True:
      self.undraw()
      self.move()

      if self.collided:
        break
      self.draw()

      sleep(1/self.speed)

def swap(a, b, lst):
  temp = lst[a]
  lst[a] = lst[b]
  lst[b] = temp

def bubbleSort(lst, compareFunc):
  for i in range(len(lst)):
    for item in range(len(lst) - 1):
      if compareFunc(lst[item + 1], lst[item]):
        swap(item, item + 1, lst)

def typewrite(text, start, border = False, author = '', delay = 0.03, dramaticPause = 0.1):
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

def erase(lines):
  for line in lines:
      print(f'\x1b[{line};{0}H;', end = '')
      print('\x1b[2K', end = '')

def setupPins():
  pin1 = Pin(LANE_REF[0], LANE_REF[1] + 1)
  pin2 = Pin(LANE_REF[0], LANE_REF[1] + 3)
  pin3 = Pin(LANE_REF[0], LANE_REF[1] + 5)
  pin4 = Pin(LANE_REF[0], LANE_REF[1] + 7)
  lane[(pin1.row, pin1.column)] = pin1
  lane[(pin2.row, pin2.column)] = pin2
  lane[(pin3.row, pin3.column)] = pin3
  lane[(pin4.row, pin4.column)] = pin4

  pin5 = Pin(LANE_REF[0] + 1, LANE_REF[1] + 2, pin1, pin2)
  pin6 = Pin(LANE_REF[0] + 1, LANE_REF[1] + 4, pin2, pin3)
  pin7 = Pin(LANE_REF[0] + 1, LANE_REF[1] + 6, pin3, pin4)
  lane[(pin5.row, pin5.column)] = pin5
  lane[(pin6.row, pin6.column)] = pin6
  lane[(pin7.row, pin7.column)] = pin7

  pin8 = Pin(LANE_REF[0] + 2, LANE_REF[1] + 3, pin5, pin6, pin2)
  pin9 = Pin(LANE_REF[0] + 2, LANE_REF[1] + 5, pin6, pin7, pin3)
  lane[(pin8.row, pin8.column)] = pin8
  lane[(pin9.row, pin9.column)] = pin9

  pin10 = Pin( LANE_REF[0] + 3, LANE_REF[1] + 4, pin8, pin9, pin6)
  lane[(pin10.row, pin10.column)] = pin10

def printLane():
  for i in range(LANE_REF[0] - 1):
    print() # push down 1 row
  
  for row in range(LANE_REF[0], LANE_REF[0] + 15):
    print(' ' * (LANE_REF[1] - 3), end = '') # push 1 column right
    if row == LANE_REF[0]:
      print('╮', end = '')
    elif row == LANE_REF[0] + 14:
      print('╯', end = '')
    else:
      print('│', end = '')
    print('║', end = '')

    for item in range(LANE_REF[1], LANE_REF[1] + 9):
      print(lane[(row, item)], end = '')
    
    print('║', end = '')
    if row == LANE_REF[0]:
      print('╭')
    elif row == LANE_REF[0] + 14:
      print('╰')
    else:
      print('│')

def getInput():
  global stop
  junk = input()
  stop = True

def generateRandomPts():
  for player in teamCAN.players:
    for i in range(3):
      player.points.append(random.randint(190, 300))
    player.getavg()
  for player in teamJAP.players:
    for i in range(3):
      player.points.append(random.randint(190, 300))
    player.getavg()

  teamCAN.getavg()
  teamJAP.getavg()

def displayTeam(team):
  typewrite('TEAM : ' + team.name, TEAM_POS)

  for i in range(len(team.players)):
    typewrite(team.players[i].name, (PLAYER_POS[0], PLAYER_POS[1] + i * 20))
    team.players[i].position = (PLAYER_POS[0] + 1, 4 + PLAYER_POS[1] + i * 20)
    team.players[i].draw(team.players[i].rest, True)

  typewrite('game 1  :', (LABEL_POS[0]    , LABEL_POS[1]))
  typewrite('game 2  :', (LABEL_POS[0] + 1, LABEL_POS[1]))
  typewrite('game 3  :', (LABEL_POS[0] + 2, LABEL_POS[1]))
  typewrite('average :', (LABEL_POS[0] + 3, LABEL_POS[1]))

  for game in range(len(team.players[0].points) + 1):
    for player in range(len(team.players)):
      # print scores and averages
      if game == 3:
        typewrite(team.players[player].avg, (POINTS_POS[0] + game, (len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20))
      else:
        typewrite(team.players[player].points[game], (POINTS_POS[0] + game, (len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20))

  typewrite("team average : " + str(team.avg), (TEAM_POS[0] + 11, TEAM_POS[1] - 2))

def enterTeam(team):
  typewrite('TEAM : ' + team.name, TEAM_POS)

  for i in range(len(team.players)):
    typewrite(team.players[i].name, (PLAYER_POS[0], PLAYER_POS[1] + i * 20))
    team.players[i].position = (PLAYER_POS[0] + 1, 4 + PLAYER_POS[1] + i * 20)
    team.players[i].draw(team.players[i].rest, True)

  typewrite('game 1   :', (LABEL_POS[0]    , LABEL_POS[1]))
  typewrite('game 2   :', (LABEL_POS[0] + 1, LABEL_POS[1]))
  typewrite('game 3   :', (LABEL_POS[0] + 2, LABEL_POS[1]))
  typewrite('average  :', (LABEL_POS[0] + 3, LABEL_POS[1]))

  for game in range(4):
    for player in range(len(team.players)):
      if team.players[player].name == 'Colt Daniels':
        if game == 2 or game == 3:
          typewrite('TBD', (POINTS_POS[0] + game, len(team.players[player].name)//2 - 2 + POINTS_POS[1] + player * 20))
        else:
          print(f'\x1b[{POINTS_POS[0] + game};{(len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20}H', end = "")
          print('\x1b[?25h', end = '')
          score = int(input())
          print('\x1b[?25l', end = '')
          team.players[player].points.append(score)
          typewrite(team.players[player].points[game], (POINTS_POS[0] + game, (len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20))
        continue

      # print scores and averages
      if game == 3:
        team.players[player].getavg()
        typewrite(team.players[player].avg, (POINTS_POS[0] + game, (len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20))
      else:
        print(f'\x1b[{POINTS_POS[0] + game};{(len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20}H', end = "")
        print('\x1b[?25h', end = '')
        score = int(input())
        print('\x1b[?25l', end = '')
        team.players[player].points.append(score)
        typewrite(team.players[player].points[game], (POINTS_POS[0] + game, (len(team.players[player].name)//2) - 2 + POINTS_POS[1] + player * 20))

  team.getavg()
  typewrite("team average : TBD", (TEAM_POS[0] + 11, TEAM_POS[1] - 2))

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
      if name == 'SPEED':
        var = 1
      else:
        var = 0

    # this should move outside the loop
    print(f'\x1b[{meter_pos[0]};{meter_pos[1]}H', end = "")
    print(name + ':', var, end = '', flush = True)

    # jump to bar
    print(f'\x1b[{meter_pos[0]};{meter_pos[1] + 9}H', end = "")

    # clear bar
    print('\x1b[0K', end = '', flush = True)

    # draw bar
    for i in range(var):
      print('>', end = '', flush = True)

    # draw preview of ball JANK
    if name == 'SHIFT':      
      # clear previous ball
      if var == 0:
        print(f'\x1b[{LANE_REF[0] + 14};{LANE_REF[1] + 8}H' + ' ', end = "", flush = True)
      else:
        print(f'\x1b[{LANE_REF[0] + 14};{LANE_REF[1] + var - 1}H' + ' ', end = "", flush = True)
      print(f'\x1b[{LANE_REF[0] + 14};{LANE_REF[1] + var}H' + 'o', end = "", flush = True)
    
    sleep(0.2)
  return var

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
    playerBall = Ball(LANE_REF[0] + 14, LANE_REF[1] + shift, speed, spin)
  else:
    playerBall.reset(LANE_REF[0] + 14, LANE_REF[1] + shift, speed, spin)
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

coach = Player('Coach Leopold')
# teams
teamCAN = Team('CANADA', [brody, ryder, maximus, griffin])
teamJAP = Team('JAPAN', [mihara, yamane, eguchi, yukimura])
teamWSU = Team('WAYNE STATE', [isaac, harley, max, colt])

generateRandomPts()

print(screen)
displayTeam(teamCAN)
input()
os.system('cls')

print(screen)
displayTeam(teamJAP)
input()
os.system('cls')

print(screen)
enterTeam(teamWSU)
input()
os.system('cls')

coach.position = (15,1)
coach.spawn()
coach.walk(30)
print(f'\x1b[{1};{1}H', end = '')


setupPins()
printLane()

for i in range(3):  
  if i == 0:
    typewrite('Alright Colt, knock \'em dead', MESSAGE_POS, border = True, author = 'Coach Leopold', dramaticPause = 1)
  elif i == 1:
    typewrite('Shoot your best shot!', MESSAGE_POS, border = True, author = 'Coach Leopold', dramaticPause = 0.5)
  else:
    typewrite('Last chance Colt!', MESSAGE_POS, border = True, author = 'Coach Leopold', dramaticPause = 0.2)
  shoot()
  erase([MESSAGE_POS[0], MESSAGE_POS[0] + 1, MESSAGE_POS[0] + 2])
  if playerBall.pins == 10:
    typewrite('YES! That\'s my boy!', MESSAGE_POS, border = True, author = 'Coach Leopold', dramaticPause = 0.2)
    break

input()
os.system('cls')

colt.points.append(playerBall.pins * 30)
colt.getavg()
teamWSU.getavg()

print(screen)
displayTeam(teamWSU)
input()
os.system('cls')

teamWSU.gettotal()
teamCAN.gettotal()
teamJAP.gettotal()

teams = [teamWSU, teamCAN, teamJAP]
players = [brody, ryder, maximus, griffin, mihara, yamane, eguchi, yukimura, isaac, harley, max, colt]

for player in players:
  player.position = (20, 1)

# using sort() is for people who don't know bubblesort
bubbleSort(teams, lambda a, b : a.points < b.points)
bubbleSort(players, lambda a, b : a.avg < b.avg)

def walkitout(i):
  sleep(i*2)
  players[i].spawn()
  players[i].walk(100 - i*6 - (i//4) * 12)

with concurrent.futures.ThreadPoolExecutor(max_workers = 12) as executor:
  executor.map(walkitout, range(12))

typewrite('Ladies and Gentlement, Welcome to the award ceremony', (5, 5), True, 'Announcer', dramaticPause=2)
erase(range(5, 10))
typewrite('of the World Bowl Championship 2034.', (5, 5), True, 'Announcer', dramaticPause = 2)
erase(range(5, 10))
typewrite('Let\'s begin with the player awards:', (5, 5), True, 'Announcer', dramaticPause = 2)
erase(range(5, 10))
typewrite('The highest averageing player is... ', (5, 5), True, 'Announcer', dramaticPause = 3)
erase(range(5, 10))

typewrite('1 ' + players[11].name + ' : ' + str(players[11].avg) + ' pts', PLAYER_PODIUM, dramaticPause = 1)
x = threading.Thread(target = players[11].dance)
x.start()
typewrite('2 ' + players[10].name + ' : ' + str(players[10].avg) + ' pts', (PLAYER_PODIUM[0] + 1, PLAYER_PODIUM[1]), dramaticPause = 1)
y = threading.Thread(target = players[10].dance)
y.start()
typewrite('3 ' + players[9].name + ' : ' + str(players[9].avg) + ' pts', (PLAYER_PODIUM[0] + 2, PLAYER_PODIUM[1]), dramaticPause = 1)
z = threading.Thread(target = players[9].dance)
z.start()

typewrite('The 2034 Bowling Champions:', (5, 5), True, 'Announcer', dramaticPause = 3)

typewrite('1 ' + teams[2].name + ' : ' + str(teams[2].points) + ' pts', (TEAM_PODIUM[0], TEAM_PODIUM[1]), dramaticPause = 1)
typewrite('2 ' + teams[1].name + ' : ' + str(teams[1].points) + ' pts', (TEAM_PODIUM[0] + 1, TEAM_PODIUM[1]), dramaticPause = 1)
typewrite('3 ' + teams[0].name + ' : ' + str(teams[0].points) + ' pts', (TEAM_PODIUM[0] + 2, TEAM_PODIUM[1]), dramaticPause = 1)



