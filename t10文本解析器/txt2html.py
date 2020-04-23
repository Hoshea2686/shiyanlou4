# /urs/bin/python3
# -*-coding:utf-8-*-

# 将4个文件写在一起了

import sys, re

# util.py
def lines(file):
    for line in file:
        yield line
    yield '\n'

def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        else:
            yield ''.join(block).strip()
            block = []

# handlers.py
class Handler:
    """docstring for Handler"""
    def callback(self, pre, name, *args):
        method = getattr(self, pre + name, None)
        if callable(method): return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def warpper(matchobj):
            return self.callback('sub_', name, matchobj.group(1))
        return warpper


class HTMLRander(Handler):
    def start_html(self):
        print('<html><head><title>将txt转换为html格式</title></head><body>')

    def end_html(self):
        print('</body></html>')

    def start_h1(self):
        print('<h1 style="color: green;">')

    def end_h1(self):
        print('</h1>')

    def start_h2(self):
        print('<h2>')

    def end_h2(self):
        print('</h2>')

    def start_ul(self):
        print('<ul>')

    def end_ul(self):
        print('</ul>')

    def start_li(self):
        print('<li>')

    def end_li(self):
        print('</li>')

    def start_p(self):
        print('<p>')

    def end_p(self):
        print('</p>')

    def feed(self, data):
        print(data)

    def sub_em(self, match):
        return '<em style="color: red;">{}</em>'.format(match)

    def sub_url(self, match):
        return '<a style="color: blue;" href="{}">{}</a>'.format(match, match)

    def sub_mail(self, match):
        return '<a style="color: blue;" href="mailto:{}">{}</a>'.format(match, match)


# rules.py
class Rule:
    """docstring for Rule"""
    lable = None

    def action(self, block, handler):
        handler.start(self.lable)
        handler.feed(block)
        handler.end(self.lable)
        return True

    def condition(self, *args):
        return False

class H2Rule(Rule):
    lable = 'h2'

    def condition(self, block):
        return '\n' not in block and block[-1] != ':' and len(block)<50

class H1Rule(H2Rule):
    lable = 'h1'
    first = True
    def condition(self, block):
        if self.first:
            self.first = False
            return super().condition(block)
        return False

class LiRule(Rule):
    lable = 'li'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self.lable)
        handler.feed(block[1:])
        handler.end(self.lable)
        return True

class UlRule(LiRule):
    lable = 'ul'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and super().condition(block):
            handler.start(self.lable)
            self.inside = True
        if self.inside and not super().condition(block):
            handler.end(self.lable)
            self.inside = False

class PRuel(Rule):
    lable = 'p'
    def condition(self, block):
        return True

RuleList = [UlRule(), LiRule(), H1Rule(), H2Rule(), PRuel()]

class Filter:
    re_em = r'\*(.+?)\*'
    re_url = r'(http://[\.a-zA-Z/]+)'
    re_mail = r'([\.a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z]+)'

    def get(self, name):
        def filter(block, handler):
            pattern = getattr(self, 're_' + name, None)
            return re.sub(pattern, handler.sub(name), block)
        return filter

FilterList = [Filter().get(name) for name in ['em', 'url', 'mail']]


# markup.py

class TextParse:
    def __init__(self, handler):
        self.handler = handler
        self.rules = RuleList
        self.filters = FilterList

    def parse(self, file):
        self.handler.start('html')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler):
                        break
        self.handler.end('html')

# main
def main():
    handler = HTMLRander()
    parser = TextParse(handler)
    parser.parse(sys.stdin)


if __name__ == '__main__':
    main()
