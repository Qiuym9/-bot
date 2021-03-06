import jieba
import numpy as np
from tensorflow.keras.models import load_model
from gensim.models import word2vec
import execute


def answer(question):
    chat_model = load_model('D:/Python/PycharmProject/-bot-master/model/model5000.h5')
    wordVector_model = word2vec.Word2Vec.load('D:/Python/PycharmProject/-bot-master/word_vector/Word60.model')

    while(True):
        # question = input('输入问题：')
        question = question.strip()
        que_list = jieba.cut(question)
        que_vector = [wordVector_model[w] for w in que_list if w in wordVector_model.wv.vocab]

        # 获得单词的维度
        word_dim = len(que_vector[0])

        # 将每一句话，删减/补足 到仅有15个单词
        sentend = np.ones((word_dim,), dtype=np.float32)
        if len(que_vector) > 14:
            que_vector[14:] = []
            que_vector.append(sentend)
        else:
            for i in range(15 - len(que_vector)):
                que_vector.append(sentend)

        que_vector = np.array([que_vector])

        # 预测答句
        predictions = chat_model.predict(que_vector)
        answer_list = [wordVector_model.most_similar([predictions[0][i]])[0][0] for i in range(15)]
        result = ''.join(answer_list)
        print(result)
        return result
