# Calculator tool

class CalculatorTool:
	def __init__(self):
		pass

	def add(self, *args, **kwargs):
		total = 0
		for i in args:
			total += i

		for i, j in kwargs.items():
			total += j

		return total

	def multiply(self, *args, **kwargs):
		total = 1
		for i in args:
			total *= i

		for i, j in kwargs.items():
			total *= j

		return total

if __name__ == "__main__":
	tool = CalculatorTool()

	solution = tool.add(1, 2, c=3, d=4, e=10)
	solution2 = tool.multiply(1, 2, c=3, d=4, e=10)

	print(f"Sum solution: {solution}")
	print(f"Product solution: {solution2}")