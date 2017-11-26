import tensorflow as tf
import cv2 #open cv
import pong
import numpy as np
import random
from collections import deque #datastructure

#print all the nitty gritty details (slows down performance)
VERBOSE = True

#define hyperperameters
ACTIONS = 3 #up down or stay
#learning rate
GAMMA = 0.99
#update gradient or training time
INITIAL_EPSILON = 1.0
FINAL_EPSILON = 0.05
#how many frames to anneal epsilong
EXPLORE = 500000
OBSERVE = 50000
REPLAY_MEMORY = 50000
#batch size (HOW MANY TIMES TO TRAIN)
BATCH = 100

#create TF graph
#5 layer conv network
def createGraph():
    
    #first convolutional layer, bias vector
    #tf.zeros creates an empty tensor
    w_conv1 = tf.Variable(tf.zeros([8, 8, 4, 32]))
    b_conv1 = tf.Variable(tf.zeros([32]))
    
    #second layer
    w_conv2 = tf.Variable(tf.zeros([4, 4, 32, 64]))
    b_conv2 = tf.Variable(tf.zeros([64]))
    
    #third layer
    w_conv3 = tf.Variable(tf.zeros([3, 3, 64, 64]))
    b_conv3 = tf.Variable(tf.zeros([64]))
    
    #fourth layer
    w_fc4 = tf.Variable(tf.zeros([3136, 784]))
    b_fc4 = tf.Variable(tf.zeros([784]))
    
    #last layer
    w_fc5 = tf.Variable(tf.zeros([784, ACTIONS]))
    b_fc5 = tf.Variable(tf.zeros([ACTIONS]))
    
    #input for our pixel data
    s = tf.placeholder('float', [None, 84, 84, 4])
    
    #rectified radial unit activation function
    #compute RELu on 2D convolutions given 4D input and filter tensors
    #this is taking the data and passing it to the next layer
    conv1 = tf.nn.relu(tf.nn.conv2d(s, w_conv1, strides=[1, 4, 4, 1], padding = "VALID") + b_conv1)
    
    conv2 = tf.nn.relu(tf.nn.conv2d(conv1, w_conv2, strides=[1, 2, 2, 1], padding = "VALID") + b_conv2)
    
    conv3 = tf.nn.relu(tf.nn.conv2d(conv2, w_conv3, strides=[1, 1, 1, 1], padding = "VALID") + b_conv3)
    
    conv3_flat = tf.reshape(conv3, [-1, 3136])
    
    fc4 = tf.nn.relu(tf.matmul(conv3_flat, w_fc4) + b_fc4)
    
    fc5 = tf.matmul(fc4, w_fc5) + b_fc5
    
    return s, fc5

#deep q network. feed in pixel data to graph session 
def trainGraph(inp, out, sess):

    #to calculate the argmax, we multiply the predicted output with a vector with one value 1 and rest as 0
    argmax = tf.placeholder("float", [None, ACTIONS]) 
    gt = tf.placeholder("float", [None]) #ground truth

    #action
    action = tf.reduce_sum(tf.multiply(out, argmax), reduction_indices = 1)
    #cost function we will reduce through backpropagation
    cost = tf.reduce_mean(tf.square(action - gt))
    #optimization fucntion to reduce our minimize our cost function 
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    #initialize our game
    game = pong.PongGame()
    
    #create a queue for experience replay to store policies
    D = deque()

    #intial frame
    frame = game.getPresentFrame()
    #convert rgb to gray scale for processing
    frame = cv2.cvtColor(cv2.resize(frame, (84, 84)), cv2.COLOR_BGR2GRAY)
    #binary colors, black or white
    ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
    #stack frames, that is our input tensor
    inp_t = np.stack((frame, frame, frame, frame), axis = 2)

    #saver
    saver = tf.train.Saver()

    sess.run(tf.initialize_all_variables())

    t = 0
    epsilon = INITIAL_EPSILON
    
    #training time
    while(1):
        #output tensor
        out_t = out.eval(feed_dict = {inp : [inp_t]})[0]
        #argmax function
        argmax_t = np.zeros([ACTIONS])

        #
        if(random.random() <= epsilon):
            maxIndex = random.randrange(ACTIONS)
        else:
            maxIndex = np.argmax(out_t)
        argmax_t[maxIndex] = 1
        
        if epsilon > FINAL_EPSILON:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        #reward tensor if score is positive
        reward_t, frame = game.getNextFrame(argmax_t)
        #get frame pixel data
        frame = cv2.cvtColor(cv2.resize(frame, (84, 84)), cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
        frame = np.reshape(frame, (84, 84, 1))
        #new input tensor
        inp_t1 = np.append(frame, inp_t[:, :, 0:3], axis = 2)
        
        #add our input tensor, argmax tensor, reward and updated input tensor tos tack of experiences
        D.append((inp_t, argmax_t, reward_t, inp_t1))

        #if we run out of replay memory, make room
        if len(D) > REPLAY_MEMORY:
            D.popleft()
        
        #training iteration
        if t > OBSERVE:

            #get values from our replay memory
            minibatch = random.sample(D, BATCH)
        
            inp_batch = [d[0] for d in minibatch]
            argmax_batch = [d[1] for d in minibatch]
            reward_batch = [d[2] for d in minibatch]
            inp_t1_batch = [d[3] for d in minibatch]
        
            gt_batch = []
            out_batch = out.eval(feed_dict = {inp : inp_t1_batch})
            
            #add values to our batch
            for i in range(0, len(minibatch)):
                gt_batch.append(reward_batch[i] + GAMMA * np.max(out_batch[i]))



            #train on that 
            train_step.run(feed_dict = {
                           gt : gt_batch,
                           argmax : argmax_batch,
                           inp : inp_batch
                           })
        
        #update our input tensor the the next frame
        inp_t = inp_t1
        t = t+1

        #save where we are
        if t % 10000 == 0:
            saver.save(sess, './' + 'pong' + '-dqn', global_step = t)
            
        #print our where were
        if (VERBOSE):

            print("TIMESTEP", t, "/ EPSILON", epsilon, "/ ACTION", maxIndex, "/ REWARD", reward_t, "/ Q_MAX %e" % np.max(out_t))
        
def main() :
    #create session
    sess = tf.InteractiveSession()
    #input layer and our output layer
    inp, out = createGraph()
    
    #feed into training
    trainGraph(inp, out, sess)
    
if __name__ == "__main__":
    main()
    