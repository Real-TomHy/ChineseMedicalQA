import os
import ahocorasick   #是一种多匹配的模块，在这里用于匹配问句里面的特征词
class QuestionClassifier:
    def __init__(self):
        #加载特征词路径
        self.part_path=r'F:\知识图谱资料\中医药知识图谱\data\part.txt'
        self.name_path=r'F:\知识图谱资料\中医药知识图谱\data\name.txt'
        self.alias_path=r'F:\知识图谱资料\中医药知识图谱\data\alias.txt'
        self.smell_path=r'F:\知识图谱资料\中医药知识图谱\data\smell.txt'
        self.cure_path=r'F:\知识图谱资料\中医药知识图谱\data\cure.txt'
        #加载特征词
        self.part_wds=[i.strip() for i in open(self.part_path,encoding="utf-8") if i.strip()]
        self.name_wds = [i.strip() for i in open(self.name_path, encoding="utf-8") if i.strip()]
        self.alias_wds = [i.strip() for i in open(self.alias_path, encoding="utf-8") if i.strip()]
        self.smell_wds = [i.strip() for i in open(self.smell_path, encoding="utf-8") if i.strip()]
        self.cure_wds = [i.strip() for i in open(self.cure_path, encoding="utf-8") if i.strip()]
        # 创建了包含5类实体特征词的元素集
        self.region_words = set(self.part_wds + self.name_wds + self.alias_wds+ self.smell_wds+ self.cure_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词，对于不同的问题，赋予特征词
        self.belong_qwds = ['属于什么部类', '什么部', '部类', '哪个部']  # 询问部类
        self.smell_qwds = ['什么气味','什么味道','闻起来怎么样','什么味的','吃起来苦嘛','吃了是什么味','什么品质','有毒嘛','有毒性嘛']
        self.alias_qwds = ['有其他别名嘛','别名是什么','还有其他称呼','别称','别名','还可以怎么叫','其他名字','那些别称']
        self.cure_qwds = ['医治方式', '疗法', '咋治', '咋吃', '咋治', '如何食用','食疗方法','可以治什么','治那些病','可以治什么症状','有那些食用方法','如何食用','最佳食用方法','有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要','治愈啥', '主治啥', '主治什么', '有什么用', '有何用']
        print('问答系统启动中......')
        #print(self.wdtype_dict)
        return
    def build_wdtype_dict(self):
        # 该函数是检查问句中涉及的5类实体，并返回一个列表
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.part_wds:
                wd_dict[wd].append('part')
            if wd in self.name_wds:
                wd_dict[wd].append('name')
            if wd in self.alias_wds:
                wd_dict[wd].append('alias')
            if wd in self.smell_wds:
                wd_dict[wd].append('smell')
            if wd in self.cure_wds:
                wd_dict[wd].append('cure')
        return wd_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False
#检查是否有实体类型的特征词
    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        # 往actree中添加数据，这是已经封装好的模块
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''构造词对应的类型'''
    def check_medical(self, question):
        #该模块是通过匹配找到问句中存在的5类实体
        region_wds = []
        #iter()是迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退
        for i in self.region_tree.iter(question):#对问句进行多匹配模式的迭代
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i : self.wdtype_dict.get(i) for i in final_wds}

        return final_dict
    '''分类主函数'''

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)  # 问句过滤
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []
        #  这是对遍历选择的方式，依次判断问句中是否存在实体，以及问句中实体类型是否在types中
        #  属于什么部类
        if self.check_words(self.belong_qwds, question) :
            question_type = 'name_part'
            question_types.append(question_type)
        #print(question_types)
        # #别名
        if self.check_words(self.alias_qwds,question) :
            question_type = 'name_alias'
            question_types.append(question_type)
        #气味品质
        if self.check_words(self.smell_qwds,question) :
            question_type = 'name_smell'
            question_types.append(question_type)
        #主治方法
        if self.check_words(self.cure_qwds,question) :
            question_type = 'name_cure'
            question_types.append(question_type)
        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] :
            question_types = ['找不到']
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data





if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('输入您的问题:')
        data = handler.classify(question)
        print(data)
        #{'args': {'腊雪': ['name']}, 'question_types': ['name_part']}
