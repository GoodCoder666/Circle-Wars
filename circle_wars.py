import pgzrun
from math import hypot, pi, cos, sin
from random import randint

class Circle:
    def __init__(self, pos, radius, color, angle=0):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.angle = angle
    
    def draw(self):
        screen.draw.filled_circle(self.pos, self.radius, self.color)
    
    def dist(self, c2):
        return hypot(self.pos[0] - c2.pos[0], self.pos[1] - c2.pos[1])
    
    def touch(self, c2):
        return (self.dist(c2) <= self.radius + c2.radius)
    
    def touch_edge(self, width, height):
        left = self.pos[0] - self.radius
        right = self.pos[0] + self.radius
        top = self.pos[1] - self.radius
        bottom = self.pos[1] + self.radius
        return (left <= 0 or right >= width or top <= 0 or bottom >= height)
    
    def move(self, steps):
        theta = self.angle / 180 * pi
        self.pos[0] += steps * cos(theta)
        self.pos[1] += steps * sin(theta)

WIDTH = 800
HEIGHT = 600
TITLE = 'Circle wars'

enemies = []
friends = []
player = Circle([0, 0], 50, (50, 130, 200))

score = 0
center_x = WIDTH / 2
center_y = HEIGHT / 2
game_over = False
won = False

def draw():
    global enemies, friends, score, game_over, won
    screen.clear()
    screen.fill('white')
    if game_over:
        screen.draw.text('GAME OVER!', center=(center_x, center_y), fontsize=90, color='red')
    elif won:
        screen.draw.text('YOU WON!', center=(center_x, center_y), fontsize=100, color='green')
    else:
        for friend in friends:
            friend.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        screen.draw.text('Score: ' + str(score), topleft=(20, 20), fontsize=75, color='orange', shadow=(1, 1))

def create_circles():
    radius = randint(20, 100)
    pos = [randint(radius, WIDTH), randint(radius, HEIGHT)]
    color = 'red'
    enemy = Circle(pos, radius, color, randint(0, 359))
    enemies.append(enemy)
    
    radius = randint(20, 100)
    pos = [randint(radius, WIDTH), randint(radius, HEIGHT)]
    color = 'green'
    friend = Circle(pos, radius, color, randint(0, 359))
    friends.append(friend)

def delete_enemies():
    for enemy in enemies:
        if randint(0, 1) == 0:
            enemies.remove(enemy)

def on_mouse_move(pos):
    player.pos = pos
    
def update():
    global friends, enemies, score, game_over, won
    if score <= -1500:
        clock.unschedule(create_circles)
        clock.unschedule(delete_enemies)
        game_over = True
        return
    elif score >= 1500:
        clock.unschedule(create_circles)
        clock.unschedule(delete_enemies)
        won = True
        return
    if not game_over and not won:
        for friend in friends:
            friend.move(1)
            if player.touch(friend):
                score += friend.radius
                friends.remove(friend)
            elif friend.touch_edge(WIDTH, HEIGHT):
                friend.angle = randint(0, 359)
        
        for enemy in enemies:
            enemy.move(1)
            if player.touch(enemy):
                score -= enemy.radius
                enemies.remove(enemy)
            elif enemy.touch_edge(WIDTH, HEIGHT):
                enemy.angle = randint(0, 359)

create_circles()
clock.schedule_interval(create_circles, 1.9)
clock.schedule_interval(delete_enemies, 9.89)
pgzrun.go()