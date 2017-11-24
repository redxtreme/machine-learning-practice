#source: https://www.youtube.com/watch?v=Hqf__FlRlzg&t=479s

import pygame
import random

#DQN. CNN reads in pixel data. 
#reinforcement learning. trial and error.
#maximize action based on reward
#agent envrioment loop
#this is called Q Learning
#based on just game state. mapping of state to action is policy
#experience replay. learns from past policies

#define vars for game
FPS = 60

#size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of paddle
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
#distance from the edge of the window
PADDLE_BUFFER = 10

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
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#draw ball
def drawBall(ballXpos, ballYpos):
    ball = pygame.Rect(ballXpos, ballYpos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)
    
#user
def drawPaddle1(paddle1Ypos):
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1Ypos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle1)
    
#enemy
def drawPaddle2(paddle2Ypos):
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2Ypos, PADDLE_WIDTH, PADDLE_HEIGHT)
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
    
    if (ballXpos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYpos + BALL_HEIGHT >= paddle2Ypos and ballYpos - BALL_HEIGHT <= paddle2Ypos + PADDLE_HEIGHT):
        ballXDirection = -1
    elif (ballXpos >= WINDOW_WIDTH - BALL_WIDTH):
        ballXDirection = -1
        score = 1
        return [score, paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection]
    
    #ball hitting top
    if (ballYpos <= 0):
        ballYpos = 0
        ballYDirection = 1
    elif (ballYpos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYpos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
        return [score, paddle1Ypos, paddle2Ypos, ballXpos, ballYpos, ballXDirection, ballYDirection]

def updatePaddle1(action, paddle1Ypos):
    #if move up
    if (action[1] == 1):
        paddle1Ypos -= PADDLE_SPEED
    #if move down
    if (action[2] == 1):
        paddle1Ypos += PADDLE_SPEED
        
    #dont let it move off the screen
    if(paddle1Ypos < 0):
        paddle1Ypos = 0
    if (paddle1Ypos >= WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1Ypos = WINDOW_HEIGHT - PADDLE_HEIGHT
        
    return paddle1Ypos

def updatePaddle2(paddle2Ypos, ballYpos):
    #move down if ball is in upper half
    if (paddle2Ypos + PADDLE_HEIGHT / 2 < ballYpos + BALL_HEIGHT / 2):
        paddle2Ypos += PADDLE_SPEED
    #move up if ball is in lower half
    if (paddle2Ypos + PADDLE_HEIGHT / 2 > ballYpos + BALL_HEIGHT / 2):
        paddle2Ypos -= PADDLE_SPEED
    #dont let it hit the top
    if (paddle2Ypos < 0):
        paddle2Ypos = 0
    #dont let it hit bottom
    if (paddle2Ypos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2Ypos = WINDOW_HEIGHT - PADDLE_HEIGHT
        
    return paddle2Ypos

class PongGame:
    def __init__ (self):
        #random number for the initial direction of the ball
        num = random.randint(0, 9)
        #keep score
        self.tally = 0
        #init pos of our paddle
        self.paddle1Ypos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle2Ypos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        #ball direction definition
        self.ballXDirection = 1
        self.ballYDirection = 1
        #starting point
        self.ballXpos = WINDOW_HEIGHT / 2 - BALL_WIDTH / 2
        self.ballYpos = num * (WINDOW_HEIGHT - BALL_HEIGHT) / 9
        
    #need to feed NN pixels of the game
    def getPresentFrame(self):
        #for each frame, call the event queue
        pygame.event.pump()
        #make background black
        screen.fill(BLACK)
        #draw our paddles
        drawPaddle1(self.paddle1Ypos)
        drawPaddle2(self.paddle2Ypos)
        #draw ball
        drawBall(self.ballXpos, self.ballYpos)
        
        #return all the pixels of the game
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        #return the screen data
        return image_data
    
    def getNextFrame(self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.paddle1Ypos = updatePaddle1(action, self.paddle1Ypos)
        drawPaddle1(self.paddle1Ypos)
        #update evil AI paddle
        self.paddle2Ypos = updatePaddle2(self.paddle2Ypos, self.ballYpos)
        drawPaddle2(self.paddle2Ypos)
        #update our vars by updating ball position
        [score, self.paddle1Ypos, self.paddle2Ypos, self.ballXpos, self.ballYpos, self.ballXDirection, self.ballYDirection] = updateBall(self.paddle1Ypos, self.paddle2Ypos, self.ballXpos, self.ballYpos, self.ballXDirection, self.ballYDirection)
        #draw the ball
        drawBall(self.ballXpos, self.ballYpos)
        
        #return all the pixels of the game
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #update the window
        pygame.display.flip()
        
        self.tally += score
        
        #return the screen data
        return [score, image_data]
    
    