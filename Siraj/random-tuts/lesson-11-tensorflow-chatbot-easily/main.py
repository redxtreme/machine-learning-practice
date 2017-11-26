#data is Cornell movie quote corpus from http://www.cs.cornell.edu/~cristian/memorability.html
#source video is https://www.youtube.com/watch?v=SJDEOWLHYVo

import tensorflow as tf
import data_utils
import seq2seq_model

def train():
    #prepare dataset
    #encoder data and decoder data
    enc_train, dec_train = data_utils.prepare_custom_data(gConfig['working_directory'])
    
    #tokenize it
    train_set = read_data(enc_train, dec_train)
    
    #training
    with tf.Session(config=config) as sess:
        #Create model
        model = create_model(sess, False)
    
    #training loop
    while True:
        sess.run(model)
        
        #save checkpoint at zero timer and loss
        checkpoint_path = os.path.join(gConfig['working_directory'], "seq2seq.chkpt")
        model.saver.save(sess, checkpoint_path, global_step=model.global_step)
        
        
train()