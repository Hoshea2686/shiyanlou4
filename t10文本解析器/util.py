# /urs/bin/python3
# -*-coding:utf-8-*-

# 工具包：产生block块（文本中以空行开始和空行结束为标志）

# 给文本末尾加上空行，避免最后一个块结尾没有空行
def lines(file):
	for line in file:
		yield line
	yield '\n'

# 产生块
def blocks(file):
	block = []	# 用于存放block所需要的行
	for line in lines(file): # 循环遍历文本中的行
		if line.strip(): # 如果不为空行
			block.append(line)	# 加入到block中，即将每一行的文本加入列表中
		else:	# 如果为空行，标志着块结束
			# 返回block中文本，还需要将列表变成文本
			yield ''.join(block).strip()
			block = [] # 将block重置

if __name__ == '__main__':
    with open("test.txt", 'r') as f:
        for block in blocks(f):
            print(block)