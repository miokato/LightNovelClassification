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


class Predictor:
    def __init__(self):
        self.category_map = {1: '異世界', 2: '現実世界', 3: '純文学', 4: '歴史', 5: '推理',
                             6: 'ホラー', 7: 'アクション', 8: 'コメディー', 9: '宇宙', 10: 'ＶＲゲーム'}
        self.model_path = 'classification/data/models/novel_clf_model.pkl'
        self.dict_path = 'classification/data/corpus/novel_clf.dict'
        self.corpus_path = 'classification/data/corpus/novel_clf.mm'
        self.tfidf_path = 'classification/data/models/novel_clf.tfidf'
        self.lsi_path = 'classification/data/models/novel_clf.lsi'
        self.dictionary = None
        self.corpus = None
        self.tfidf_model = None
        self.lsi_model = None
        self.clf = None
        self._preprocess()

    def _preprocess(self):
        self.dictionary = corpora.Dictionary.load(self.dict_path)
        self.corpus = corpora.MmCorpus(self.corpus_path)
        self.tfidf_model = models.TfidfModel.load(self.tfidf_path)
        self.lsi_model = models.LsiModel.load(self.lsi_path)
        self.clf = joblib.load(self.model_path)

    def predict(self, words):
        bow_corpus = self.dictionary.doc2bow(words)
        tfidf_corpus = self.tfidf_model[bow_corpus]
        lsi_corpus = self.lsi_model[tfidf_corpus]
        vec = [vecs[1] for vecs in lsi_corpus]
        _id = self.clf.predict([vec])
        _id = _id.tolist()
        prediction = self.category_map[_id[0]]
        return prediction


if __name__ == '__main__':
    manager = MessageManager(CabochaParser())
    path = 'classification/data/104/n0102ei/chapter0.txt'
    with open(path, 'rt') as f:
        data = f.read()
    mes = manager.extract_message(data)
    words = mes.bags
    predictor = Predictor()
    prediction = predictor.predict(words)
    print(prediction)
