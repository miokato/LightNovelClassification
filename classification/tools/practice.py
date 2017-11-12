from nlp.parser import CabochaParser, MessageManager
from gensim.models import Word2Vec
from gensim import corpora


if __name__ == '__main__':

    query = '今日は朝の早く1日です。猫は可愛いです。はじも可愛いです。'
    manager = MessageManager()
    manager.parser = CabochaParser()
    message = manager.extract_message(query)

    texts = [s.bag for s in message.sentences]
    print(texts)
    dictionary = corpora.Dictionary(texts)
    dictionary.save('nlp/data/test.dict')
    print(type(dictionary))
    print(dictionary.token2id) # tokenにidがふられる

    #model = Word2Vec()
