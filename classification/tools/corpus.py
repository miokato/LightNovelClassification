from gensim import corpora
from gensim import models

from classification.tools.parser import MessageManager, CabochaParser
from classification.tools.loader import BookManager


class CorpusManager:
    def __init__(self):
        self.file_manager = BookManager()
        self.parse_manager = MessageManager(CabochaParser())
        self.creator = CorpusCreator()
        self.labels = []

    def create_corpus(self):
        raw_data_list = ['101', '102', '104', '303', '304', '305', '306', '307', '401', '402']
        target_mapper = {'101': 1, '102': 2, '104': 3, '303': 4, '304': 5,
                         '305': 6, '306': 7, '307': 8, '401': 9, '402': 10}
        documents = []
        for raw_data in raw_data_list:
            files = self.file_manager.load(raw_data)
            for file in files:
                with open(file, 'rt') as f:
                    data = f.read()
                message = self.parse_manager.extract_message(data)
                documents.append(message.bags)
                self.labels.append(target_mapper[raw_data])

        dictionary = self.creator.create_dict(documents)
        corpus = self.creator.create_corpus(documents, dictionary)
        tfidf = self.creator.create_tfidf(corpus)
        lsi_corpus = self.creator.create_lsi(tfidf, dictionary)
        return lsi_corpus, self.labels


class CorpusCreator:
    def create_dict(self, documents):
        path = 'classification/data/corpus/novel_clf.dict'
        # 全文書に登場する単語にidをふって辞書をつくる
        dictionary = corpora.Dictionary(documents)
        dictionary.save(path)
        # dic.filter_extremes(no_below=20, no_above=0.3)
        return dictionary

    def create_corpus(self, documents, dictionary):
        # corpus 作成
        # 各文書中に辞書に登録する単語が何回登場するかを数えてbag of wordsをつくる
        path = 'classification/data/corpus/novel_clf.mm'
        bow_corpus = [dictionary.doc2bow(d) for d in documents]
        corpora.MmCorpus.serialize(path, bow_corpus)
        return bow_corpus

    def create_tfidf(self, bow_corpus):
        # tfidf
        # 各文書の単語のtf/idfを計算する
        path = 'classification/data/models/novel_clf.tfidf'
        tfidf_model = models.TfidfModel(bow_corpus)
        tfidf_model.save(path)
        tfidf_corpus = tfidf_model[bow_corpus]

        return tfidf_corpus

    def create_lsi(self, tfidf_corpus, dictionary):
        # 次元削減
        # 辞書から作成した6000次元ほどのコーパスを200次元まで圧縮する。
        path = 'classification/data/models/novel_clf.lsi'
        lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=200)
        lsi_model.save(path)
        lsi_curpus = lsi_model[tfidf_corpus]

        return lsi_curpus


