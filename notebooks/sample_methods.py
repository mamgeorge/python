# sample_methods.py

print(f'filename: {__name__}')
print(f'__name__: {__name__}')

class History:

	pi = 3.14

	def __init__(self, dateyear, place, event):

		self.dateyear = dateyear
		self.place = place
		self.event = event

	def showme(self):
		return f'In {self.dateyear}, at {self.place}, the {self.event} took place!'

def justone():
	return 'one'


def adder(a, b):
	return a + b
