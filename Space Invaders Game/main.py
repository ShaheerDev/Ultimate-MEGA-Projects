import random
from turtle import Screen, Turtle
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.title("Space Invaders Game")

player = Turtle()
player.shape("triangle")
player.color("white")
player.penup()
player.goto(0, -250)
player.setheading(90)

bullet = Turtle()
bullet.shape("square")
bullet.color("white")
bullet.shapesize(stretch_wid=1, stretch_len=0.2)
bullet.penup()
bullet.speed(0)
bullet.hideturtle()
bullet.goto(0, 240)

def go_left():
    x = player.xcor()
    x -= 20
    if x > -280:
        player.setx(x)
def go_right():
    x = player.xcor()
    x += 20
    if x < 280:
        player.setx(x)

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

bullet_state = True
def fire_bullet():
    global bullet_state
    if bullet_state:
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullet.showturtle()
        bullet_state = False


enemies = []
enemy_speed = 2

for _ in range(8):
    enemy = Turtle()
    enemy.shape("circle")
    enemy.color("red")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.goto(x, y)
    enemies.append(enemy)

while True:
    screen.update()
    time.sleep(0.02)
    if not bullet_state:
        y = bullet.ycor()
        y += 20
        bullet.sety(y)
        if y > 280:
            bullet.hideturtle()
            bullet_state = True



        for enemy in enemies:
            x = enemy.xcor()
            x += enemy_speed
            enemy.setx(x)

            if x > 280 or x < -280:
                enemy_speed *= -1
                for e in enemies:
                    y = e.ycor()
                    e.sety(y-20)

        for enemy in enemies:
            if bullet.distance(enemy) < 20:
                bullet.hideturtle()
                bullet_state = True
                bullet.goto(0, -400)

                x = random.randint(-200, 200)
                y = random.randint(150, 250)
                enemy.goto(x, y)

        for enemy in enemies:
            if enemy.ycor() < player.ycor() + 20:
                print("Game Over")
                screen.bye()

    screen.onkeypress(fire_bullet, "space")
