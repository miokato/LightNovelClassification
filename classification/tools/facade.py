from classification.tools.parser import CabochaParser, JumanParser


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
    t = """
    ライトノベルとその他の小説の境界は曖昧であり、はっきりとした定義を持たないことから、「ライトノベルの定義」についてさまざまな説がある。ライトノベルを発行しているレーベルから出ている、出版社がその旨宣言した作品、マンガ・萌え絵のイラストレーション、挿絵を多用し、登場人物のキャラクターイメージや世界観設定を予め固定化している、キャラクターを中心として作られている、青少年（あるいは若年層）を読者層に想定して執筆されている、作者が自称する、など、様々な定義が作られた[2][3]が、いずれも客観的な定義にはなっていない。
    """
    manager = MessageManager(parser='cabocha')
    message = manager.extract_message(t)
    print(message.bags)
