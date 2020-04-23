# /urs/bin/python3
# -*-coding:utf-8-*-

# 渲染文本， HTML，加标签

class Handler:
    """处理父类"""
    def callback(self, pre, name, *args):
        method = getattr(self, pre + name, None)
        if callable(method):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def wrapper(matchobj):
            return self.callback('sub_', name, matchobj.group())
        return wrapper

class HTMLRander(Handler):
    def start_html(self):
        print('<html><head><title>SYL</title></head><body>')

    def end_html(self):
        print('</body></html>')

    def start_h1(self):
        print('<h1 style="color: #1ABC9C;">')

    def end_h1(self):
        print('</h1>')

    def start_h2(self):
        print('<h2 style="color: #68BE5D;">')

    def end_h2(self):
        print('</h2>')

    def start_p(self):
        print('<p style="color: #444;">')

    def end_p(self):
        print('</p>')

    def start_ul(self):
        print('<ul style="color: #363736;">')

    def end_ul(self):
        print('</ul>')

    def start_li(self):
        print('<li>')

    def end_li(self):
        print('</li>')

    def feed(self, data):
        print(data)

    def sub_em(self, match):
        return '<em>{}</em>'.format(match)

    def sub_url(self, match):
        return '<a style="color: #BC1A4B;" href="{}">{}</a>'.format(match, match)

    def sub_mail(self, match):
        return '<a style="color: #BC1A4B;" href="mailto:{}">{}</a>'.format(match, match)


if __name__ == '__main__':
    rander = HTMLRander()
    with open('test.txt', 'r') as f:
        data = f.read()

    # 采用正则(regular experssion)来替换(substitute)
    import re
    data = re.sub(r'([\.a-zA-Z0-9]+@[\.a-zA-Z]+[a-zA-Z]+)', rander.sub('mail'), data)
    print(data)

    # 渲染开头
    rander.start('html')
    rander.feed(data)
    rander.end('html')

