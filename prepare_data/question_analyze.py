class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):  # res_classify是问题分类对问句分析的数据
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        # print(entity_dict)
        # print(question_types)
        # {'name': ['腊雪']}
        # ['name_part']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'name_part':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))
            elif question_type == 'name_alias':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))
            elif question_type == 'name_smell':
                sql = self.sql_transfer(question_type,entity_dict.get('name'))
            elif question_type == 'name_cure':
                sql = self.sql_transfer(question_type,entity_dict.get('name'))
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        return sqls
        # # print(sqls)

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询疾病的原因
        if question_type == 'name_part':
            sql = ["MATCH (n)-[r:属于]-(b) where n:中药 and n.name='{0}' return b.name".format(i) for i in entities]
        elif question_type == 'name_alias':
            sql = ["MATCH (n)-[r:别名是]-(b) where n:中药 and n.name='{0}' return b.name".format(i) for i in entities]
        elif question_type == 'name_smell':
            sql = ["MATCH (n)-[r:气味品质是]-(b) where n:中药 and n.name='{0}' return b.name".format(i) for i in entities]
        elif question_type == 'name_cure':
            sql = ["MATCH (n)-[r:使用方法是]-(b) where n:中药 and n.name='{0}' return b.name".format(i) for i in entities]
        return sql

    #["MATCH (n)-[r:属于]-(b) where n:中药 and n.name='name' return b.name"]
if __name__ == '__main__':
    handler = QuestionPaser()
    #res_classify={'args': {'腊雪': ['name']}, 'question_types': ['name_part']}
    # {'args': {'腊雪': ['name']}, 'question_types': ['name_part']}
    #print(handler.parser_main(res_classify))
    # print(handler.sql_transfer('name_part',{'name': ['腊雪']}))
    #[{'question_type': 'name_part', 'sql': ["MATCH (n)-[r:属于]-(b) where n:中药 and n.name='腊雪' return b.name"]}]


