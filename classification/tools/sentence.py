class Sentence(object):
    """
    センテンスのリストを保存する
    """

    def __init__(self):
        self.text = str()
        self.bag = list()
        self.tokens = list()
        self.tree = None

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

