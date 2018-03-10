'''
贝叶斯算法实现文本分类

时间：2018-3-10
作者：刘宇

V:1.0
'''

# 导入os,codece,pandas,jieba相关模块，主要在BYSModel中使用
import os
import codecs
import pandas
import jieba

class BYSModel:

    '''
    贝叶斯模型
    1：需要将训练集放入Sample中
    2：需要导入停词
    '''

    def __init__(self):
        '''
        初始化字典，很重要，对应形式：
        Sample子文件夹名：分类名字
        '''
        self.classDict = {}
        with open("category.txt") as f:
            read_data = f.readlines()
        for eve in read_data:
            eve = eve.strip()
            if eve:
                temp1,temp2 = eve.split("----")
                self.classDict[temp1] = temp2

    def modelData(self):
        '''
        模型数据初始化
        :return: 返回tuple，主要是词库，向量等
        '''

        stop_word_data = [] # 停词
        class_list = []
        fenci_data = []

        # 停词
        with open("StopwordsCN.txt") as f:
            total_stop_word = f.readlines()
        for eve_stop_word in total_stop_word:
            stop_word_data.append(eve_stop_word.replace("\n", ""))

        # 遍历文件夹Sample，进行数据初始化，同时使用jieba进行分词等
        for eve_dir in os.walk("Sample"):
            eve_path_data = eve_dir[0]
            for eve_file_data in eve_dir[2]:
                new_path_data = os.path.join(eve_path_data, eve_file_data)
                if ".txt" in new_path_data:
                    with codecs.open(new_path_data, "r","utf-8") as f:
                        file_content = f.read()

                    eve_content_fenci_data = []

                    for eve_word_data in jieba.cut(file_content):
                        if eve_word_data not in stop_word_data and len(eve_word_data) > 0:
                            eve_content_fenci_data.append(eve_word_data)

                    fenci_data.append(" ".join(eve_content_fenci_data))
                    class_list.append(self.classDict[eve_path_data.split("/")[1]])


        fenciku = pandas.DataFrame({
            "class": class_list,
            "content": fenci_data
        })

        # 词向量
        from sklearn.feature_extraction.text import CountVectorizer
        countVectorizer = CountVectorizer(
            min_df=0,
            token_pattern=r"\b\w+\b"
        )

        textVector = countVectorizer.fit_transform(
            fenciku['content']
        )

        return (fenciku, countVectorizer, textVector)


    def setModel(self,textVector, fenciku):
        '''
        模型建立，主要是bys模型，多项式分布的朴素贝叶斯
        :param textVector:
        :param fenciku:
        :return:
        '''
        from sklearn.naive_bayes import MultinomialNB
        bys = MultinomialNB()
        bys.fit(textVector, fenciku["class"])
        return bys


    def predictModel(self,bys,companyInfor, countVectorizer):
        '''
        模型预测
        :param bys:
        :param companyInfor:
        :param countVectorizer:
        :return:
        '''
        newTexts = companyInfor
        for i in range(len(newTexts)):
            newTexts[i] = " ".join(jieba.cut(newTexts[i]));
        newTextVector = countVectorizer.transform(newTexts)
        return bys.predict(newTextVector)

