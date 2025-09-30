import sample_methods
from sample_methods import adder as adder

def test_justone_1(): assert sample_methods.justone() == 'one'

def test_adder_2(): assert adder(0, 0) == 0
def test_adder_3(): assert adder(0, 1) == 1
def test_adder_4(): assert adder(1, 1) == 2
def test_adder_5(): assert adder(1, 2) == 3

def test_adder_6(): assert adder(2, 2) == 5

def test_adder_7():
	try:
		assert adder(2, 2) == 5
	except AssertionError as ex:
		print(f'ERROR: {ex}')

def test_adder_8(): assert adder(2, 2) == 4
