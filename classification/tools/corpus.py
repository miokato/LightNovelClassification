from gensim import corpora
from gensim import models
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import grid_search
from sklearn.externals import joblib

from classification.tools.parser import MessageManager, CabochaParser
from classification.tools.loader import BookManager


class Trainer:
    def __init__(self):
        self.corpus_manager = CorpusManager()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def create_dataset(self):
        # dataset作成
        lsi_corpus = self.corpus_manager.create_corpus()
        l_novel_dict = {}
        l_novel_dict['data'] = []
        l_novel_dict['target'] = []
        l_novel_dict['target_name'] = []

        for doc, label in zip(lsi_corpus, self.corpus_manager.labels):
            vecs = [v[1] for v in doc]
            l_novel_dict['data'].append(vecs)
            l_novel_dict['target'].append(label)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(l_novel_dict['data'],
                                                            l_novel_dict['target'],
                                                            random_state=50)

    def train(self):
        path = 'classification/data/models/novel_clf_model.pkl'
        svc = SVC()
        cs = [0.001, 0.01, 0.1, 1, 10]
        gammas = [0.001, 0.01, 0.1, 1]
        parameters = {'kernel': ['rbf'], 'C': cs, 'gamma': gammas}
        clf = grid_search.GridSearchCV(svc, parameters)
        clf.fit(self.X_train, self.y_train)
        joblib.dump(clf, path)

        return clf


class CorpusManager:
    def __init__(self):
        self.file_manager = BookManager()
        self.parse_manager = MessageManager(CabochaParser())
        self.creator = CorpusCreator()
        self.labels = []

    def create_corpus(self):
        raw_data_list = ['101', '102', '104']
        target_mapper = {'101': 1, '102': 2, '103': 3, '104': 4}
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
        lsi = self.creator.create_lsi(tfidf, dictionary)
        return lsi


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


if __name__ == '__main__':
    trainer = Trainer()
    trainer.create_dataset()
    clf = trainer.train()
    score = clf.score(trainer.X_test, trainer.y_test)
    print(score)
