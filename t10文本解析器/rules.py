# /urs/bin/python3
# -*-coding:utf-8-*-

# 制定规则
class Rule(object):
    """docstring for Rule"""
    def __init__(self):
        self.lable = None

    def condition(self, *args):
        pass 
    
    def action(self, block, handler):
        handler.start(self.lable)
        handler.feed(block)
        handler.end(self.lable)
        return True

class H2Rule(Rule):
    """docstring for H1Rule"""
    def __init__(self):
        self.lable = 'h2'
    
    def condition(self, block):
        return '\n' not in block and block[-1] != ':' and len(block)<=50


class H1Rule(H2Rule):
    """docstring for H1Rule"""
    def __init__(self):
        self.lable = 'h1'
        self.first = True

    def condition(self, block):
        if self.first:
            self.first = False
            return super().condition(block)
        return False


class LiRule(object):
    """docstring for LiRule"""
    def __init__(self):
        self.lable = 'li'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.lable)
        handler.feed(block[1:].strip())
        handler.end(self.lable)
        return True


class UlRule(LiRule):
    """docstring for UlRule"""
    def __init__(self):
        self.lable = 'ul'
        self.inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and super().condition(block):
            handler.start(self.lable)
            self.inside = True
        if self.inside and not super().condition(block):
            handler.end(self.lable)
            self.inside = False
        return False


class PRule(Rule):
    """docstring for PRule"""
    def __init__(self):
        self.lable = 'p'

    def condition(self, block):
        return True


RuleList = [UlRule(), LiRule(), H1Rule(), H2Rule(), PRule()]

import re

class Filters:
    """docstring for Filter"""
    re_em = r'\*(.+?)\*'
    re_url = r'(http://[\.a-zA-Z/]+)'
    re_mail = r'([\.a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z]+)'

    def get(self, name):
        def filter(handler, block):
            pattern = getattr(self, 're_' + name, None)
            return re.sub(pattern, handler.sub(name), block)
        return filter

FilterList = [Filters().get(name) for name in ('em', 'url', 'mail')]