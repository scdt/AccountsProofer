import re
import os
import numpy as np
import catboost
import html2text as h2t
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from catboost import CatBoostClassifier

print(catboost.__file__)


def htmlToText(html):
    h = h2t.HTML2Text()
    h.ignore_links = True
    text = h.handle(html)
    # text = re.sub(r'\*\s+.*|#+\s*.*', '', text)
    # text = re.sub(r'!\S+', '', text)
    text = re.sub(r'\S.jpeg|\S.jpg|\S.svg|\S.png', '', text)
    text = text.lower()
    text = text.replace("'", ' ')
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    ps = PorterStemmer()
    text = ps.stem(text)
    stop_words = set(stopwords.words('english'))
    stop_words.difference_update({'should', 'no', 'not'})
    stop_words.update({'one', 'distribution', 'ace', 'rewards', 'cookies', 'create', 'online', 'music', 'youtube', 'english',
                       'video', 'privacy', 'terms', 'upload', 'new', 'love', 'espaol', 'portugus', 'streaming', 'log'})
    for word in text.split():
        if(word in stop_words):
            text = re.sub(rf'\b{word}\b', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text


def trainAndTest():
    train_htmls = []
    test_htmls = []
    train_classes = []
    test_classes = []
    for file in os.scandir('train_pages'):
        filename = os.fsdecode(file)
        if filename.endswith('.html'):
            with open(filename) as file1:
                train_htmls.append(file1.read())
                if(filename.find('NoReg') == -1):
                    train_classes.append(1)
                else:
                    train_classes.append(0)
    for file in os.scandir('test_pages'):
        filename = os.fsdecode(file)
        if filename.endswith('.html'):
            with open(filename) as file1:
                test_htmls.append(file1.read())
                if(filename.find('NoReg') == -1):
                    test_classes.append(1)
                else:
                    test_classes.append(0)
    print('train files:', len(train_htmls))
    print('test files:', len(test_htmls))
    train_texts = []
    test_texts = []
    for html in train_htmls:
        train_texts.append(htmlToText(html))
    for html in test_htmls:
        test_texts.append(htmlToText(html))

    vectorizer = TfidfVectorizer(max_features=200)
    train_set = vectorizer.fit_transform(train_texts)
    test_set = vectorizer.transform(test_texts)
    clfMNB = MultinomialNB()
    clfLSVC = LinearSVC()
    clfCB = CatBoostClassifier(iterations=100, learning_rate=3, depth=7)
    clfMNB.fit(X=train_set, y=train_classes)
    clfLSVC.fit(X=train_set, y=train_classes)
    clfCB.fit(X=train_set.toarray(), y=train_classes)
    predict_trainMNB = clfMNB.predict(train_set)
    predict_trainLSVC = clfLSVC.predict(train_set)
    predictMNB = clfMNB.predict(test_set)
    predictLSVC = clfLSVC.predict(test_set)
    predictCB = clfCB.predict(test_set.toarray())
    print('f1_scoreMNB:', f1_score(test_classes, predictMNB))
    print('precision_scoreMNB:', precision_score(test_classes, predictMNB))
    print('recall_scoreMNB:', recall_score(test_classes, predictMNB))
    print('f1_scoreLSVC:', f1_score(test_classes, predictLSVC))
    print('precision_scoreLSVC:', precision_score(test_classes, predictLSVC))
    print('recall_scoreLSVC:', recall_score(test_classes, predictLSVC))
    print('f1_scoreCB:', f1_score(test_classes, predictCB))
    print('precision_scoreCB:', precision_score(test_classes, predictCB))
    print('recall_scoreCB:', recall_score(test_classes, predictCB))


if __name__ == '__main__':
    trainAndTest()
