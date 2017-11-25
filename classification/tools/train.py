from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import grid_search
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler

from classification.tools.corpus import CorpusManager


class Trainer:
    def __init__(self):
        pass

    def create_dataset(self, corpus, labels):
        # dataset作成
        l_novel_dict = {}
        l_novel_dict['data'] = []
        l_novel_dict['target'] = []
        l_novel_dict['target_name'] = []

        for doc, label in zip(corpus, labels):
            vecs = [v[1] for v in doc]
            l_novel_dict['data'].append(vecs)
            l_novel_dict['target'].append(label)

        X_train, X_test, y_train, y_test = train_test_split(l_novel_dict['data'],
                                                            l_novel_dict['target'],
                                                            random_state=50)
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train, model=None):
        path = 'classification/data/models/novel_clf_model.pkl'
        model = model()
        cs = [0.001, 0.01, 0.1, 1, 10]
        gammas = [0.001, 0.01, 0.1, 1]
        parameters = {'kernel': ['rbf'], 'C': cs, 'gamma': gammas}
        clf = grid_search.GridSearchCV(model, parameters)
        clf.fit(X_train, y_train)
        joblib.dump(clf, path)

        return clf


if __name__ == '__main__':
    manager = CorpusManager()
    trainer = Trainer()
    corpus, labels = manager.create_corpus()
    X_train, X_test, y_train, y_test = trainer.create_dataset(corpus, labels)
    print('create dataset')
    model = trainer.train(X_train, y_train, model=SVC)
    score = model.score(X_test, y_test)
    print('Test accuracy is {}%'.format(score*100))
