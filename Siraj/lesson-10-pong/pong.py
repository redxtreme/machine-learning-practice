#source: https://www.youtube.com/watch?v=Hqf__FlRlzg&t=479s

import pygame
import random

#define vars for game
FPS = 60

#size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

#size of ball
BALL_WIDTH = 10
BALL_HEIGHT = 10

#speed of paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

#RGB Colors paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#initialize our screen
screen = pygame.display.set_mode(WINDOW_WIDTH, WINDOW_HEIGHT)

#draw ball
def drawBall(ballXpos, ballYpos):
    ball = pygame.rect(ballXpos, ballYpos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)
    
#user
def drawPaddle1(paddle1Ypos):
    paddle1 = pygame.rect(PADDLE_BUFFER, paddle1Ypos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle1)
    
#enemy
def drawPaddle2(paddle2Ypos):
    paddle2 = pygame.rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2Ypos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle2)
    
def updateBall(paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection):
    
    #update x and y pos
    ballXpos += ballXDirection * BALL_X_SPEED
    ballYpos += ballYDirection * BALL_Y_SPEED
    
    score = 0
    
    #check for collision
    #if the ball hits the left side, then switch direction
    if (ballXpos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYpos + BALL_HEIGHT >= paddle1Ypos and ballYpos - BALL_HEIGHT <= paddle1Ypos + PADDLE_HEIGHT):
        ballXDirection = 1
    elif (ballXpos <= 0):
        ballXDirection = 1
        score = -1
        return [score, paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection]
    
    if (ballXpos >= IWNDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER adn ballYpos + BALL_HEIGHT >= paddle2Ypos and ballYpos - BALL_HEIGHT <= paddle2Ypos + PADDLE_HEIGHT):
        ballXDirection = -1
    elif (ballXpos >= WINDOW_WIDTH - BALL_WIDTH):
        ballXDirection = -1
        score = 1
        return [score, paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection]
    
    #ball hitting top
    if (ballYpos <= 0):
        ballYpos = 0
        ballYDirection = 1
    elif (ballYpos >= WINDOW_HEIGHT - BALLHEIGHT):
        ballYpos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
        return [score, paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection]

def updatePaddle1(action, paddle1Ypos):
    #if move up
    if (action[1] = 1):
        paddle1Ypos -= PADDLE_SPEED
    #if move down
    if (action[2] = 1):
        paddle1Ypos += PADDLE_SPEED
        
    #dont let it move off the screen
    if(paddle1Ypos < 0):
        paddle1Ypos = 0
    if (paddle1Ypos >= WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1Ypos = WINDOW_HEIGHT - PADDLE_HEIGHT
        
    return paddle1Ypos

def updatePaddle2(action, paddle2Ypos):
    #if move up
    if (action[1] = 1):
        paddle2Ypos -= PADDLE_SPEED
    #if move down
    if (action[2] = 1):
        paddle2Ypos += PADDLE_SPEED
        
    #dont let it move off the screen
    if(paddle2Ypos < 0):
        paddle2Ypos = 0
    if (paddle2Ypos >= WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2Ypos = WINDOW_HEIGHT - PADDLE_HEIGHT
        
    return paddle2Ypos
    
    