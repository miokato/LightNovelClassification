from classification.tools.parser import CabochaParser, JumanParser
from classification.tools.loader import BookManager


class MessageManager:
    def __init__(self, parser=None):
        if parser == 'cabocha':
            self.parser = CabochaParser()
        elif parser == 'juman':
            self.parser = JumanParser()

    def extract_message(self, text):
        message = self.parser.parse_message(text)
        message = self.parser.parse(message)
        return message


if __name__ == '__main__':
    file_manager = BookManager()
    files = file_manager.load('305')
    for file in files:
        with open(file, 'rt') as f:
            data = f.read()
        parse_manager = MessageManager(parser='cabocha')
        message = parse_manager.extract_message(data)
        print(message.bags)
