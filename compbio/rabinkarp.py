import math
import random


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


class KarpRabin:
	def __init__(self, r, q, input_string):
		self.r = r
		self.q = q
		self.pow_r = []  # precomputed powers of r
		self.T = input_string  # input string
		self.T_len = len(self.T)
		self.alphabet = {}  # mapping of characters to numbers
		self.hash_prefix = []  # prefix hash list, hash_prefix[i] = hash(T[1..i])

		self.precompute_powers_r()
		self.init_alphabet()
		self.precompute_hash_prefix_array()

	def precompute_powers_r(self):
		# max value is r^(max l)
		self.pow_r.append(1)
		for i in range(self.T_len):
			self.pow_r.append((self.pow_r[i] * self.r) % self.q)

	def precompute_hash_prefix_array(self):
		self.hash_prefix.append(0)  # indexing from 1
		for i in range(self.T_len):
			hash_val = ((self.hash_prefix[i]*self.r) + self.alphabet[self.T[i]]) % self.q
			self.hash_prefix.append(hash_val)

	# def precompute_hash_prefix_array(self):
	# 	for i in range(self.T_len):
	# 		hash_val = 0
	# 		for j in range(i):
	# 			hash_val += (self.alphabet[self.T[j]]*(self.pow_r[i+1-j])) % self.q
	# 		self.hash_prefix.append(hash_val)


	def init_alphabet(self):
		alphabet_map = {}
		alphabet_num = 1
		for char in self.T:
			if char not in alphabet_map:
				alphabet_map[char] = alphabet_num
				alphabet_num += 1
		self.alphabet = alphabet_map

	def compute_fingerprint(self, a, b):
		"""
		computes fingerprint for substring from a to b (inclusive of both)
		using the precomputed hash

		:param a: start point of substring
		:param b: end point of substring
		:return: hash value
		"""
		return (self.hash_prefix[b] - ((self.hash_prefix[a] * self.pow_r[b-a]) % self.q)) % self.q

	def query(self, i, j, l):
		"""
		:param i: start index of substring1
		:param j: start index of substring2
		:param l: length of the substrings
		:return: String that represents whether the two substrings match or not (YES/NO)
		"""
		fingerprint1 = self.compute_fingerprint(i-1, i+l-1)
		fingerprint2 = self.compute_fingerprint(j-1, j+l-1)
		if fingerprint1 == fingerprint2:
			return "YES"
		return "NO"


if __name__ == '__main__':
	input_str, tests = read_input("./testfiles/in.txt")
	q = int(math.pow(10,7) + 7)
	# r = random.randint(1, q)
	r = 10
	rabinKarp = KarpRabin(r, q, input_str)
	results = []
	for test in tests:
		results.append(rabinKarp.query(test[0], test[1], test[2]))
	failed_tests, false_neg, false_pos = read_and_compare_output(results, "./testfiles/out.txt")
	print(failed_tests)
	print(false_neg)
	print(false_pos)


