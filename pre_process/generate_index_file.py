import logging
import jieba
from gensim import corpora, models, similarities
from pre_process.generate_index_file_defs import get_stop_words
import os
from collections import defaultdict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  # logging events

origin_file = 'comments.txt'
dictionary_file = 'comment_dictionary.dict'
corpus_file = 'comment_corpus.mm'
topics_num = 30
lsi_file = 'comment_lsi.lsi'
index_file = 'comment_index.index'
stop_words_file = 'stop_words.txt'


stop_words = get_stop_words(stop_words_file)
comments = []
with open(origin_file, encoding="utf-8") as f:
    lines = f.readlines()
    for document in lines:
        # for each comment(holds one line)
        # cut words
        words = list(jieba.cut(document))
        # remove stop words
        if len(words) > 0:
            comments.append(words)

frequency = defaultdict(int)
for comment in comments:
    for token in comment:
        frequency[token] += 1

# remove stop words and words that appear only once
for words in comments:
    words = [word for word in words if word not in stop_words and frequency[word] > 1]

dictionary = corpora.Dictionary(comments)  # may perform better using better dictionaries
dictionary.save(dictionary_file)


class MyCorpus(object):
    def __iter__(self):
        for line in open(origin_file, encoding="utf-8"):
            yield dictionary.doc2bow(jieba.cut(line))

corpus = MyCorpus()
corpora.MmCorpus.serialize(corpus_file, corpus)

# transform to tfidf space
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=topics_num)
corpus_lsi = lsi[corpus_tfidf]
lsi.save(lsi_file)

index = similarities.Similarity(os.path.abspath(os.path.dirname(__file__)), lsi[corpus], num_features=topics_num)
index.save(index_file)
