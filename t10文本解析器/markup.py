# /urs/bin/python3
# -*-coding:utf-8-*-

import sys
from handlers import HTMLRander
from rules import RuleList, FilterList
from util import blocks


class TextParse:
    """docstring for TextParse"""
    def __init__(self, handler):
        self.handler = handler
        self.rules = []     # 判断文本块规则的实例列表
        self.filters = []   # 过滤方法列表
        for rule in RuleList:
            self.rules.append(rule)
        for filter in FilterList:
            self.filters.append(filter)

    def parse(self, file):
        self.handler.start('html')
        for block in blocks(file):
            # 调用过滤器，对每个文本块进行处理
            for filter in self.filters:
                block = filter(self.handler, block)
            # 循环规则类的实例
            for rule in self.rules:
                # 如果符合规则，调用实例的 action 方法打印标签
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    # 如果 action 方法的返回值为 True 
                    # 表示该文本块处理完毕，结束循环
                    if last: 
                        break
        self.handler.end('html')
        

def main():
    '''
    主函数，控制整个程序的运行
    '''
    handler = HTMLRander()
    parser = TextParse(handler)
    # 将文件内容作为标准输入，sys.stdin 获取标准输入的内容，生成 IOWrapper 迭代器对象
    parser.parse(sys.stdin)


if __name__ == '__main__':
    main()
    # 终端执行
    # python3 markup.py <test.txt>test.html