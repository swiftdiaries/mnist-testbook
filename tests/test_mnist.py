from testbook import testbook

@testbook('notebooks/mnist.ipynb', execute=True)
def test_foo(tb):

	foo = tb.ref("foo")
	assert foo(2) == 5
	assert foo(2) == 6

if __name__ == "__main__":
	test_foo()
