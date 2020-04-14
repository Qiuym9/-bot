import os
import re
import sys

from gensim.models import word2vec
import numpy as np
import tensorflow as tf
import pandas as pd

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import RepeatVector, Dense, TimeDistributed

import pre_train


def XY_vector(X,Y):
    model = word2vec.Word2Vec.load('D:/Python/PycharmProject/-bot-master/word_vector/Word60.model')
    
    X_v=[]
    
    for x_sentence in X:
        x_word = x_sentence.split(' ')
        x_sen2vec = [model[w] for w in x_word if w in model.wv.vocab]
        X_v.append(x_sen2vec)
        
    Y_v=[]
    
    for y_sentence in Y:
        y_word = y_sentence.split(' ')
        y_sen2vec = [model[w] for w in y_word if w in model.wv.vocab]
        Y_v.append(y_sen2vec)
        
    word_dim = len(X_v[1][0])
    sentend = np.ones((word_dim,),dtype=np.float32)
    for stv in X_v:
        if len(stv)>15:
            stv[15:]=[]
            stv.append(sentend)
        else:
            for i in range(15-len(stv)):
                stv.append(sentend)
                
    for stv in Y_v:
        if len(stv)>15:
            stv[15:]=[]
            stv.append(sentend)
        else:
            for i in range(15-len(stv)):
                stv.append(sentend)
    return X_v,Y_v


def seq2seq(X_vector, Y_vector):
    # print(len(X_vector[0][0]))
    # 将 X_vector、Y_vector 转化为数组形式
    X_vector = np.array(X_vector, dtype=np.float32)
    Y_vector = np.array(Y_vector, dtype=np.float32)

    # 手动切分数据为：训练集、测试集
    pos = 80
    X_train, X_test = X_vector[:pos], X_vector[pos:]
    Y_train, Y_test = Y_vector[:pos], Y_vector[pos:]

    timesteps = X_train.shape[1]
    word_dim = X_train.shape[2]
    print(X_train.shape)
    print(timesteps)
    print(word_dim)
    print(X_train.shape[1:])

    # 构建一个空容器
    model = Sequential()

    # 编码
    model.add(LSTM(word_dim, input_shape=X_train.shape[1:], return_sequences=False))

    # 将问句含义进行复制
    model.add(RepeatVector(timesteps))

    # 解码
    model.add(LSTM(word_dim, return_sequences=True))

    # 添加全连接层
    model.add(TimeDistributed(Dense(word_dim, activation="linear")))

    # 编译模型
    model.compile(loss='mse', optimizer='Adam', metrics=['accuracy'])

    # 训练、保存模型
    model.fit(X_train, Y_train, nb_epoch=500, validation_data=(X_test, Y_test))
    model.save('model/model5000.h5')

    return model


if __name__ == '__main__':
    X, Y = pre_train.XY()
    # X_list, Y_list=pre_train.word_segment(X,Y)
    X_list, Y_list=pre_train.word_segment2(X,Y)
    X_vector, Y_vector = XY_vector(X_list, Y_list)
    model = seq2seq(X_vector, Y_vector)
