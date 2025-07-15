import time
from turtle import Screen
from paddle import Paddle
from ball import Ball
from brick import Brick
from scoreboard import ScoreBoard

bricks = []

colors = ["red", "orange", "yellow", "green", "blue"]
x_start = -350
y_start = 250

screen = Screen()
paddle_game = Paddle((0, -180))
ball_game = Ball()
scoreboard = ScoreBoard()

screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Breakout Game")

screen.listen()
screen.onkey(fun=paddle_game.go_left, key="a")
screen.onkey(fun=paddle_game.go_right, key="d")

for row in range(5):
    for col in range(10):
        x = x_start + (col * 80)
        y = y_start - (row * 30)
        print("Color for row", row, "is", colors[row])
        brick = Brick((x, y), colors[row])
        bricks.append(brick)
game_is_on = True
while game_is_on:
    time.sleep(ball_game.move_speed)
    screen.update()
    ball_game.move()

    for brick in bricks[:]:
        if ball_game.distance(brick) < 50:
            brick.hideturtle()
            bricks.remove(brick)
            ball_game.bounce_y()
            scoreboard.increase_score()
            break
        if len(bricks) == 0:
            scoreboard.game_won()
            game_is_on = False
    if ball_game.xcor() > 380 or ball_game.xcor() < -380:
        ball_game.bounce_x()
    if ball_game.ycor() > 280:
        ball_game.bounce_y()
    if ball_game.distance(paddle_game) < 60 and ball_game.ycor() < -160:
        ball_game.bounce_y()

    if ball_game.ycor() < -280:
        time.sleep(2)
        ball_game.reset_position()