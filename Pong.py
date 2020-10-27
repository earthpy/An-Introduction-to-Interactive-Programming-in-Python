# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score_left = 0
score_right = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    r_x = random.randrange(120, 240)/60
    r_y = random.randrange(60, 180)/60
    if direction == "RIGHT":
        ball_vel = [r_x, -1*r_y]
    elif direction == "LEFT":
        ball_vel = [-1*r_x, -1*r_y]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score_left, score_right

    paddle1_pos = [HALF_PAD_WIDTH, (HEIGHT/2)+HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH-HALF_PAD_WIDTH, (HEIGHT/2)+HALF_PAD_HEIGHT]
    
    paddle1_vel = 0
    paddle2_vel = 0
    
    score_left = 0
    score_right = 0
    
    spawn_ball("LEFT")
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, score_left, score_right
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] >= (HEIGHT-BALL_RADIUS):
        ball_vel[1] *= -1
    elif ball_pos[1] <= (BALL_RADIUS):
        ball_vel[1] *= -1
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    if paddle1_pos[1] <= PAD_HEIGHT:
        paddle1_pos[1] = PAD_HEIGHT
    elif paddle1_pos[1] >= HEIGHT:
        paddle1_pos[1] = HEIGHT
    
    paddle2_pos[1] += paddle2_vel
    if paddle2_pos[1] <= PAD_HEIGHT:
        paddle2_pos[1] = PAD_HEIGHT
    elif paddle2_pos[1] >= HEIGHT:
        paddle2_pos[1] = HEIGHT
    
    # draw paddles
    canvas.draw_line(paddle1_pos, [paddle1_pos[0], (paddle1_pos[1]-(2*HALF_PAD_HEIGHT))], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos, [paddle2_pos[0], (paddle2_pos[1]-(2*HALF_PAD_HEIGHT))], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide    
    if ball_pos[0] >= (WIDTH-PAD_WIDTH-BALL_RADIUS):
        if (ball_pos[1] >= (paddle2_pos[1]-(2*HALF_PAD_HEIGHT)-BALL_RADIUS)) and (ball_pos[1] <= (paddle2_pos[1]+BALL_RADIUS)):
            ball_vel[0] *= -1.1
        else:
            spawn_ball("LEFT")
            score_left += 1
            
    if ball_pos[0] <= (PAD_WIDTH+BALL_RADIUS):
        if (ball_pos[1] >= (paddle1_pos[1]-(2*HALF_PAD_HEIGHT)-BALL_RADIUS)) and (ball_pos[1] <= (paddle1_pos[1]+BALL_RADIUS)):
            ball_vel[0] *= -1.1
        else:
            spawn_ball("RIGHT")
            score_right += 1
    
    # draw scores
    canvas.draw_text(str(score_left), [WIDTH/4, HEIGHT/5], 40, "White")
    canvas.draw_text(str(score_right), [WIDTH*3/4, HEIGHT/5], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
btn_restart = frame.add_button('Restart', new_game)

# start frame
new_game()
frame.start()

