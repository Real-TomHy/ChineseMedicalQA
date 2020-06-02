from question_analyze import *
from question_classifier import *
from answer_grasph import *
'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是Tom医药智能助理，希望可以帮到您。如果没答上来，可联系SF1210991856'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        #return res_sql
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

# if __name__ == '__main__':
#     handler = ChatBotGraph()

    # while 1:
    #     question = input('用户:')
    #     answer = handler.chat_main(question)
    #     print('Tom:', answer)