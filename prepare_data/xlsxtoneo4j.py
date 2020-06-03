import os
import pandas
from py2neo import Graph,Node,Relationship#这是操作neo4j的库

g = Graph('http://neo4j:密码@localhost:7474/db/data/')#neo4j.bat console
    # 导入球队的数据
def importfile():
    m_part =open('part.txt','w+')
    for root, dirs, files in os.walk(r'F:\知识图谱资料\中医药知识图谱\data'):
        for file in files:
            part = file.split('.')[0]
            m_part.write(part)
        m_part.close()#导出部类数据
            # node = Node('部类', name=part)
            # g.create(node)
            # print(part)
#importfile()
def importRelation():
    count=0
    m_name=open('name.txt','w+')
    m_alias=open('alias.txt','w+')
    m_smell=open('smell.txt','w+')
    m_cure=open('cure.txt','w+')
    for root, dirs, files in os.walk(r'F:\知识图谱资料\中医药知识图谱\data'):
        for file in files:
            frame = pandas.read_excel(r"F:/知识图谱资料/中医药知识图谱/data/"+file)
            part = file.split('.')[0]
            for i in frame.index:
                name = frame.get_value(i, 'name')
                alias = frame.get_value(i,'alias')
                smell = frame.get_value(i, 'smell')
                cure = frame.get_value(i, 'cure')
                m_name.write(name)
                m_name.write('\n')
                m_alias.write(alias)
                m_alias.write('\n')
                m_smell.write(smell)
                m_smell.write('\n')
                m_cure.write(cure)
                m_cure.write('\n')
                count += 1
                print(count)
        m_name.close()
        m_alias.close()
        m_smell.close()
        m_cure.close()
                #career_dict = {'部类': part}
                # part_node = Node('部类', name=part)
                # g.merge(part_node)
                # # 最后创建关系
                # med_node = Node('中药', name=name)  # label为节点标签，name为节点名称，需要注意不要用label='label'否则label会成为节点的的属性
                # '''如果把这个作为中药的属性，而不作为节点属性，不利于后面的问答系统'''
                # alias_node=Node('别名',name=alias)
                # smell_node=Node('气味品质',name=smell)
                # cure_node=Node('主治方法',name=cure)
                # # med_node['别名'] = alias  # 向node添加属性'property'
                # # med_node['气味品质'] = smell
                # # med_node['使用方法'] = cure
                # # g.merge(med_node)  # 将节点加入图数据库与create不同之处在于若节点存在则不创
                # relat = Relationship(med_node, '属于', part_node)
                # relat_one = Relationship(med_node, '别名是', alias_node)
                # relat_two = Relationship(med_node, '气味品质是', smell_node)
                # relat_three = Relationship(med_node, '使用方法是', cure_node)
                #
                # try:
                #     g.create(relat_one)
                # except:
                #     continue
                # try:
                #     g.create(relat_two)
                # except:
                #     continue
                # try:
                #     g.create(relat_three)
                # except:
                #     continue
                # try:
                #     g.create(relat)
                # except:
                #     continue
                # count+=1
                # print(count)
importRelation()
