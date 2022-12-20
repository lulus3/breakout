"""
Activity 004: Breakout in Python Turtle
Collaborators: Leonardo, Lucas Trovão, Luiz Eller
Last Modified on: 19/12/2022
Last Modified by: Lucas Trovão
TODO: Add sounds, Test the game more, Resolution bug 
        Ball_Size collision, Ball_Reset stop
"""

import turtle

# Declares constants
INITIAL_DX = 1
INITIAL_DY = 1.5
SPEED_UP_COEFFICIENT = 1.5
TOTAL_LIVES = 3
SPEED_UP_NUM_HITS_1 = 4
SPEED_UP_NUM_HITS_2 = 12
PADDLE_MOVE_LENGTH = 30
BALL_SIZE = 0.5


# Represents a brick the player must hit with the ball to destroy
class Brick:
    def __init__(self, position_x, position_y, color, score_given):
        self.x = position_x
        self.y = position_y
        self.color = color
        self.score = score_given
        self.brick = turtle.Turtle()

    def hide(self):
        self.brick.hideturtle()
        self.x = None
        self.y = None

    def draw_me(self):
        self.brick.speed(0)
        self.brick.shape("square")
        self.brick.color(self.color)
        self.brick.shapesize(stretch_wid=1, stretch_len=2)
        self.brick.penup()
        self.brick.goto(self.x, self.y)


def paddle_left():
    x = paddle.xcor()
    if x > -315 + paddle_len * 10:
        x -= PADDLE_MOVE_LENGTH
    else:
        x = -315 + paddle_len * 10
    paddle.setx(x)


def paddle_right():
    x = paddle.xcor()
    if x < 315 - paddle_len * 10:
        x += PADDLE_MOVE_LENGTH
    else:
        x = 315 - paddle_len * 10
    paddle.setx(x)


# returns ball to the top center of the paddle
def reset_ball():
    # TODO: Add a pause after ball reset while playing
    ball.goto(paddle.xcor(), -330)
    if ball.dy < 0:
        ball.dy *= -1


# call this function everytime you change score or lives
def update_score():
    hud.clear()
    hud.write("{} : {}".format(score, lives), align="center",
              font=("Press Start 2P", 24, "normal"))


# linear increases the speed of the ball
def speed_up_ball():
    # for exponential scaling
    # ball.dx *= SPEED_UP_COEFFICIENT
    # ball.dy *= SPEED_UP_COEFFICIENT

    if ball.dx > 0:
        ball.dx += INITIAL_DX * SPEED_UP_COEFFICIENT
    else:
        ball.dx -= INITIAL_DX * SPEED_UP_COEFFICIENT

    if ball.dy > 0:
        ball.dy += INITIAL_DY * SPEED_UP_COEFFICIENT
    else:
        ball.dy -= INITIAL_DY * SPEED_UP_COEFFICIENT


def create_bricks():
    bricks = []
    for i_aux in range(8):
        aux_list = []
        for j_aux in range(14):
            if i_aux < 2:
                aux_list.append(Brick((j_aux * 45) - 295, 380 - 25 * i_aux, "red", 7))
            elif i_aux < 4:
                aux_list.append(Brick((j_aux * 45) - 295, 380 - 25 * i_aux, "orange", 5))
            elif i_aux < 6:
                aux_list.append(Brick((j_aux * 45) - 295, 380 - 25 * i_aux, "green", 3))
            else:
                aux_list.append(Brick((j_aux * 45) - 295, 380 - 25 * i_aux, "yellow", 1))
        bricks.append(aux_list)
    return bricks


# Initializes variables
score = 0
lives = TOTAL_LIVES
num_hits = 0
speedup_condition = [True, True, True, True]
play_again = True

# Draws the screen
# TODO: Fix the screen for different sized monitors
screen = turtle.Screen()
screen.title("My Breakout")
screen.bgcolor("black")
screen.setup(width=630, height=900)
screen.tracer(0)

# Draw Paddle
paddle_len = 6
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("cyan")
paddle.shapesize(stretch_wid=1, stretch_len=paddle_len)
paddle.penup()
paddle.goto(0, -350)

# Displays heads-up score
hud = turtle.Turtle()
hud.speed(0)
hud.shape("square")
hud.color("white")
hud.penup()
hud.hideturtle()
hud.goto(0, 410)
hud.write("000 : 3", align="center", font=("Press Start 2P", 24, "normal"))
update_score()

# Draws ball above paddle
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.shapesize(stretch_wid=BALL_SIZE, stretch_len=BALL_SIZE)
ball.penup()
ball.dx = INITIAL_DX
ball.dy = INITIAL_DY
reset_ball()

# Keyboard listener
screen.listen()
screen.onkeypress(paddle_left, "a")
screen.onkeypress(paddle_right, "d")
screen.onkeypress(paddle_left, "A")
screen.onkeypress(paddle_right, "D")
screen.onkeypress(paddle_left, "Left")
screen.onkeypress(paddle_right, "Right")

# creates and draws bricks on the screen
brick_list = create_bricks().copy()
for i in range(8):
    for j in range(14):
        brick_list[i][j].draw_me()

while True:
    screen.update()

    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # brick collision
    # TODO: Change collision to accommodate different ball sizes
    #       Add a collision sound effect
    num_hits_this_frame = 0
    if ball.ycor() > 190:
        for i in range(8):
            for j in range(14):
                if brick_list[i][j].x is not None:
                    if (brick_list[i][j].y - 10 <= ball.ycor() <= brick_list[i][j].y + 10) and (
                            brick_list[i][j].x - 25 <= ball.xcor() <= brick_list[i][j].x + 25):
                        score += brick_list[i][j].score
                        num_hits_this_frame += 1
                        update_score()
                        num_hits += 1
                        if speedup_condition[2] and i < 2:
                            speedup_condition[2] = False
                            speed_up_ball()
                        elif speedup_condition[3] and i < 4:
                            speedup_condition[3] = False
                            speed_up_ball()
                        ball.dy *= -1
                        brick_list[i][j].hide()
    if num_hits_this_frame == 2:
        ball.dy *= -1

    # collision with left wall
    if ball.xcor() < -305:
        ball.setx(-305)
        ball.dx *= -1

    # collision with right wall
    if ball.xcor() > 305:
        ball.setx(305)
        ball.dx *= -1

    # collision with the upper wall
    if ball.ycor() > 410:
        ball.sety(400)
        ball.dy *= -1
        paddle_len = 3
        paddle.shapesize(stretch_wid=1, stretch_len=paddle_len)

    # collision with the lower wall
    # TODO: Add a fail sound effect
    if ball.ycor() < -420:
        ball.sety(-420)
        lives -= 1
        if lives == 0:
            break
        reset_ball()
        update_score()

    # collision with the paddle
    if paddle.ycor() < ball.ycor() < -330 and (
            paddle.xcor() + paddle_len * 10 >= ball.xcor() >= paddle.xcor() - paddle_len * 10):
        ball.sety(-330)
        ball.dy *= -1

    # speeds up ball based on number of hits
    if speedup_condition[0] and num_hits >= SPEED_UP_NUM_HITS_1:
        speedup_condition[0] = False
        speed_up_ball()
    elif speedup_condition[1] and num_hits >= SPEED_UP_NUM_HITS_2:
        speedup_condition[1] = False
        speed_up_ball()

    if play_again and num_hits == (8 * 14):
        play_again = False
        brick_list = create_bricks().copy()
        for i in range(8):
            for j in range(14):
                brick_list[i][j].draw_me()
