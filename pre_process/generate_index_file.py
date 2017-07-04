import logging
import jieba
from gensim import corpora, models, similarities
from pre_process.generate_index_file_defs import get_stop_words
import os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  # logging events

origin_file = 'comments.txt'
dictionary_file = 'comment_dictionary.dict'
corpus_file = 'comment_corpus.mm'
topics_num = 10
lsi_file = 'comment_lsi.lsi'
index_file = 'comment_index.index'
stop_words_file = 'stop_words.txt'


stop_words = get_stop_words(stop_words_file)
comments = []
with open(origin_file) as f:
    lines = f.readlines()
    for document in lines:
        # for each comment(holds one line)
        # cut words
        words = jieba.cut(document)
        # remove stop words
        comment_tokenized = [word for word in words if not word in stop_words]
        if len(comment_tokenized) > 0:
            comments.append(comment_tokenized)

dictionary = corpora.Dictionary(comments)
dictionary.save(dictionary_file)

class MyCorpus(object):
    def __iter__(self):
        for line in open(origin_file):
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
