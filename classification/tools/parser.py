import re
import os

from gensim import corpora, similarities, models

from .cabocha_analyzer import CaboChaAnalyzer
from .message import Message
from .sentence import Sentence
from pyknp import Jumanpp


class MessageManager:
    def __init__(self, parser):
        self.parser = parser

    def extract_message(self, text):
        message = self.parser.parse_message(text)
        message = self.parser.parse(message)
        return message


class Parser:
    def __init__(self):
        split_pattern = r'。|？|\?|！|\!|\n'
        self.split_compiled = re.compile(split_pattern)

    def parse_message(self, raw_text):
        message = Message()
        message.clear()
        message.text = raw_text.lower()
        try:
            raw_sents = self.split_compiled.split(message.text)
        except AttributeError:
            return None

        raw_sents = [s.strip() for s in raw_sents if s]
        raw_sents = [s for s in raw_sents if len(s) > 1]
        for raw_sent in raw_sents:
            sent = Sentence()
            sent.text = raw_sent
            message.add_sentence(sent)
        return message


class CabochaParser(Parser):
    def __init__(self):
        super().__init__()
        remove_pattern = r'・|、|\,|\.| |　'
        self.remove_compiled = re.compile(remove_pattern)
        self.analyzer = CaboChaAnalyzer('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    def parse(self, message):
        for sent in message.sentences:
            sent.text = self.remove_compiled.sub('', sent.text)
            sent.tree = self.analyzer.parse(sent.text)
            sent.bag = self.create_bags(sent)
            message.bags += sent.bag
        return message

    @staticmethod
    def create_bags(sent):
        bag = []
        for token in sent.tree.tokens:
            if token.pos == '名詞' or token.pos == '動詞':
                bag.append(token.surface)
        return bag


class JumanParser(Parser):
    def __init__(self):
        super().__init__()
        remove_pattern = r'・|、|\,|\.| |　'
        self.remove_compiled = re.compile(remove_pattern)
        self.analyzer = Jumanpp()

    def parse(self, message):
        for sent in message.sentences:
            sent.text = self.remove_compiled.sub('', sent.text)
            parsed = self.analyzer.analysis(sent.text)
            mrph_list = parsed.mrph_list()
            sent.bag = self.create_bags(mrph_list)
            message.bags += sent.bag
        return message

    @staticmethod
    def create_bags(mrph_list):
        bag = []
        for mrph in mrph_list:
            if mrph.hinsi == '名詞' or mrph.hinsi == '動詞':
                bag.append(mrph.genkei)
        return bag


class LSI:
    def __init__(self):
        self.dictionary = None
        self.corpus = None
        self.lsi = None
        self.index = None
        self.dictionary_path = 'nlp/data/script.dict'
        self.corpus_path = 'nlp/data/script.mm'
        self.index_path = 'nlp/data/script.index'
        self.lsi_path = 'nlp/data/script.lsi'

    def train(self, bows):
        self.dictionary = corpora.Dictionary(bows)
        self.corpus = [self.dictionary.doc2bow(sent) for sent in bows]
        self.lsi = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=100)
        self.index = similarities.MatrixSimilarity(self.lsi[self.corpus])

        self.dictionary.save(self.dictionary_path)
        corpora.MmCorpus.serialize(self.corpus_path, self.corpus)
        self.index.save(self.index_path)
        self.lsi.save(self.lsi_path)

    def similar_doc(self, bow):
        self.dictionary = corpora.Dictionary.load(self.dictionary_path)
        self.corpus = corpora.MmCorpus(self.corpus_path)
        self.index = similarities.MatrixSimilarity.load(self.index_path)
        self.lsi = models.LsiModel.load(self.lsi_path)

        vec_bow = self.dictionary.doc2bow(bow)
        vec_lsi = self.lsi[vec_bow]
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims


