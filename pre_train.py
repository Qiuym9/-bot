import os
import re
import sys

import jieba
import numpy as np
import tensorflow as tf
import pandas as pd
import csv

def XY():
    X,Y=[],[]
    with open('data/financezhidao_filter2.csv',encoding='gbk',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            X.append(row[0])
            Y.append(row[1])
#    print(X[:10])
    return X,Y

def word_segment(X,Y):
    output_x = open('data/X.txt','w',encoding='utf-8')
    output_y = open('data/Y.txt','w',encoding='utf-8')
    X_list,Y_list=[],[]
    for i in range(len(X)):        
        seg_list=''
        seg_list = jieba.cut(X[i])
        segments=''
        for word in seg_list:
            segments = segments+' '+word
        segments += '\n'
        segments = segments.lstrip()
        
        output_x.write(segments)        
        X_list.append(' '.join(segments))
        
    for i in range(len(Y)):
        seg_list=''
        seg_list = jieba.cut(Y[i])
        segments=''
        for word in seg_list:
            segments = segments+' '+word
        segments += '\n'
        segments = segments.lstrip()
        
        output_y.write(segments)        
        Y_list.append(' '.join(segments))

                      
    output_x.close()
    output_y.close()
 #   print(X_list[:10])
                      
    return X_list,Y_list

#X Y生成后
def word_segment2(X,Y):
    output_x = open('test/data/X.txt','r',encoding='utf-8')
    output_y = open('test/data/Y.txt','r',encoding='utf-8')
    
    X_list,Y_list=[],[]
    lines_x = output_x.readlines()
    lines_y = output_y.readlines()
    
    for i in range(len(lines_x)):
        X_list.append(lines_x[i])
    for i in range(len(lines_y)):
        Y_list.append(lines_y[i])
                      
    output_x.close()
    output_y.close()
  #  print(len(X_list),X_list[1],len(Y_list),Y_list[1])
                      
    return X_list,Y_list

