# /urs/bin/python3
# -*-coding:utf-8-*-

class Inter:
	def __init__(self):
		self.stack = []
		self.env = {}
		self.run_code = None

	def load_num(self, num):
		self.stack.append(num)

	def save_var(self, name):
		self.env[name] = self.stack.pop()

	def load_var(self, name):
		self.stack.append(self.env[name])

	def add_two_num(self, *args):
		num1 = self.stack.pop()
		num2 = self.stack.pop()
		res = num1 + num2
		self.stack.append(res)

	def print_num(self, *args):
		print(self.stack.pop())

	def parse_arg(self, step, index):
		if index is None:
			return None
		if step in ['load_num']:
			return self.run_code['numbers'][index]
		if step in ['load_var', 'save_var']:
			return self.run_code['variable'][index]
		return None

	def run(self, what_to_exe):
		self.run_code = what_to_exe
		steps = self.run_code['steps']
		for step, index in steps:
			arg = self.parse_arg(step, index)
			getattr(self, step, None)(arg)

if __name__ == '__main__':
	inter = Inter()
	# 5+7
	what_to_exe = {
		'steps': [('load_num', 0),
				  ('load_num', 1),
				  ('add_two_num', None),
				  ('print_num', None)],
		'numbers': [5, 7]
	}
	inter.run(what_to_exe)

	# 5+7+8
	what_to_exe = {
		'steps': [('load_num', 0),
				  ('load_num', 1),
				  ('add_two_num', None),
				  ('load_num', 2),
				  ('add_two_num', None),
				  ('print_num', None)],
		'numbers': [5, 7, 8]
	}
	inter.run(what_to_exe)

	# def add():
	# 	a = 5
	# 	b = 8
	# 	return a + b
	what_to_exe = {
		'steps': [('load_num', 0),
				  ('save_var', 0),
				  ('load_num', 1),
				  ('save_var', 1),
				  ('load_var', 0),
				  ('load_var', 1),
				  ('add_two_num', None),
				  ('print_num', None)],
		'numbers': [5, 8],
		'variable': ['a', 'b']
	}
	inter.run(what_to_exe)