import math


def read_input(input_file):
	"""
	reads input from the given file
	format is as follows-
	first line: string
	second line: k
	next k lines: i, j, l
	"""
	input_string = ""
	test_cases = []
	with open(input_file) as f:
		lines = [line.rstrip() for line in f]
		input_string = lines[0]
		k = int(lines[1])
		for i in range(k):
			test_cases.append([int(x) for x in lines[i+2].split(' ')])
	return input_string, test_cases


def read_and_compare_output(generated_output, output_file):
	"""
	verify the generated output against correct output
	:return: count of failing testcases
	"""
	count_failed = 0
	false_pos = 0
	false_neg = 0
	with open(output_file) as f:
		correct_output = [line.rstrip() for line in f]
		n = len(generated_output)
		for i in range(n):
			if generated_output[i] != correct_output[i]:
				count_failed += 1
				if correct_output == "YES":
					false_neg += 1
				else:
					false_pos += 1
	return count_failed, false_neg, false_pos


def rank_strings(lst, radix=False):
	idx = 1
	sorted_char_list = radix_sort_strings(lst, radix)
	char_map = {}
	char_list = []
	for char in sorted_char_list:
		if char not in char_map:
			char_map[char] = idx
			idx += 1
	for char in lst:
		char_list.append(char_map[char])
	return char_list


def countingSort(array, place):
	size = len(array)
	output = [0] * size
	count = [0] * 10
	# Calculate count of elements
	for i in range(0, size):
		index = array[i] // place
		count[index % 10] += 1
	# Calculate cumulative count
	for i in range(1, 10):
		count[i] += count[i - 1]
	# Place the elements in sorted order
	i = size - 1
	while i >= 0:
		index = array[i] // place
		output[count[index % 10] - 1] = array[i]
		count[index % 10] -= 1
		i -= 1
	for i in range(0, size):
		array[i] = output[i]


def radix_sort_strings(array, radix=True):
	if not radix:
		return sorted(array)
	max_element = max(array)
	place = 1
	while max_element // place > 0:
		countingSort(array, place)
		place *= 10
	return array


def build_b_array(a_i, i, base):
	n = len(a_i)
	b_next = []
	for j in range(n-i):
		b_next.append(a_i[j]*base + a_i[j+i])
	return b_next


class KMR:
	def __init__(self, input_string, base):
		self.base = base
		self.pow_2 = []  # precomputed powers of r
		self.log_l = []  # precomputed log values of possible l
		self.T = input_string  # input string
		self.T_len = len(self.T)
		self.kmr_arrays = []  # KMR array list

		self.precompute_log_l()
		self.precompute_powers_2()
		self.build_kmr_arrays()

	def precompute_log_l(self):
		# compute log values from 1 to n
		# 1 indexed
		self.log_l.append(0)
		for i in range(1, self.T_len+1):
			self.log_l.append(int(math.log2(i)))

	def precompute_powers_2(self):
		# max value is 2^ceil(log(n))
		# 1 indexed
		self.pow_2.append(1)
		for i in range(1, self.log_l[self.T_len]):
			self.pow_2.append(self.pow_2[i-1] * 2)

	def build_kmr_arrays(self):
		k = self.log_l[self.T_len]  # number of kmr arrays
		a_0 = rank_strings(list(self.T), False)  # initial array
		self.kmr_arrays.append(a_0)

		for i in range(k):
			# build table for 2^i
			# build b_i using a_i-1
			b_i = build_b_array(self.kmr_arrays[-1], self.pow_2[i], self.base)
			self.kmr_arrays.append(rank_strings(b_i))

	def compute_kmr_rank(self, a, l):
		"""
		computes the representation for substring starting at a with length l
		using the precomputed KMR tables

		:param a: start point of substring
		:param l: length of substring
		:return: KMR representation value
		"""
		k = self.log_l[l]
		first_part = a
		second_part = a+l-self.pow_2[k]
		vals = self.kmr_arrays[k][first_part], self.kmr_arrays[k][second_part]
		return vals

	def query(self, i, j, l):
		"""
		:param i: start index of substring1
		:param j: start index of substring2
		:param l: length of the substrings
		:return: String that represents whether the two substrings match or not (YES/NO)
		"""
		val1 = self.compute_kmr_rank(i - 1, l)
		val2 = self.compute_kmr_rank(j - 1, l)
		if val1 == val2:
			return "YES"
		return "NO"


if __name__ == "__main__":
	input_str, tests = read_input("./testfiles/in.txt")
	kmr = KMR(input_str, 100)
	results = []
	for test in tests:
		results.append(kmr.query(test[0], test[1], test[2]))
	failed_tests, false_neg, false_pos = read_and_compare_output(results, "./testfiles/out.txt")
	print(failed_tests)
	print(false_neg)
	print(false_pos)