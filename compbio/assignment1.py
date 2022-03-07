import math
import random

#### begin: KMP question #####
def naive_string_match(text, pattern):
	"""
	A naive algorithm to find all occurrences of the pattern in text in O(m*n)
	:param text: input text string of length n
	:param pattern: input pattern string of length m
	:return: list of indices of all occurrences of pattern in text
	"""
	m = len(pattern)
	n = len(text)
	matches = []
	for i in range(n - m + 1):
		j = 0
		while j < m:
			if text[i + j] != pattern[j]:
				break
			j += 1
		if j == m:
			matches.append(i)  # 0 indexing
	return matches


def compute_pi(pattern):
	"""
	computes the pi array for given pattern string
	:param pattern: input pattern string of length m
	:return: pi array for this pattern string (0 indexed)
	"""
	m = len(pattern)
	pi = [0] * m
	b = 0
	for i in range(1, m):
		while b > 0 and pattern[b] != pattern[i]:
			b = pi[b-1]
		if pattern[b] == pattern[i]:
			b += 1
		pi[i] = b
	return pi


def kmp_string_match(text, pattern):
	"""
	Using KMP algorithm to find all occurrences of the pattern in text
	:param text: input text string
	:param pattern: input pattern string
	:return: list of indices of all occurrences of pattern in text
	"""
	matches = []

	# compute pi array
	pi = compute_pi(pattern)

	m = len(pattern)
	n = len(text)
	j = 0
	i = 0
	while i < n - m + 1:
		while j < m and text[i + j] == pattern[j]:
			j += 1
		if j == m:
			matches.append(i)  # 0 indexing
		if j > 0:
			i += (j - pi[j - 1])
			j = pi[j - 1]
		else:
			i += 1
	return matches


def verify_matches(l1, l2):
	n = len(l1)
	m = len(l2)
	if m != n:
		return False
	for i in range(n):
		if l1[i] != l2[i]:
			return False
	return True


class KMPDriver:
	def __init__(self, total_texts_range, patterns_per_text_range, text_len_range,
				 pattern_len_range, alphabet_len_range):
		self.all_alphabets = "abcdefghijklmnopqrstuvwxyz"
		self.cases_generated = 0
		self.total_texts_range = total_texts_range
		self.patterns_per_text_range = patterns_per_text_range
		self.text_len_range = text_len_range
		self.pattern_len_range = pattern_len_range
		self.alphabet_len_range = alphabet_len_range
		self.text_lengths = {}
		self.alphabet_sizes = {}
		self.pattern_lengths = {}
		self.num_matches = {}
		self.correct_cases = 0
		self.incorrect_cases = 0

	def generate_alphabet(self):
		num_alphabets = random.randint(self.alphabet_len_range[0], self.alphabet_len_range[1])
		alphabet = ''.join(random.sample(self.all_alphabets, k=num_alphabets))
		self.alphabet_sizes[num_alphabets] = self.alphabet_sizes.get(num_alphabets, 0) + 1
		return alphabet

	def generate_text(self, alphabet):
		text_len = random.randint(self.text_len_range[0], self.text_len_range[1])
		text = ''.join(random.choices(alphabet, k=text_len))
		self.text_lengths[text_len] = self.text_lengths.get(text_len, 0) + 1
		return text

	def generate_pattern(self, alphabet):
		pattern_len = random.randint(self.pattern_len_range[0], self.pattern_len_range[1])
		pattern = ''.join(random.choices(alphabet, k=pattern_len))
		self.pattern_lengths[pattern_len] = self.pattern_lengths.get(pattern_len, 0) + 1
		return pattern

	def print_stats(self):
		print("Total cases generated: ", self.cases_generated)
		print("Correct answers: ", self.correct_cases)
		print("Incorrect answers: ", self.incorrect_cases)
		print("Number of hits frequency distribution: ", self.num_matches)
		print("Text length frequency distribution: ", self.text_lengths)
		print("Pattern length frequency distribution: ", self.pattern_lengths)
		print("Alphabet size frequency distribution: ", self.alphabet_sizes)

	def simulate(self):
		# generate texts
		failed_cases = []
		num_texts = random.randint(self.total_texts_range[0], self.total_texts_range[1])
		for i in range(num_texts):
			# generate alphabet
			alphabets = self.generate_alphabet()
			# generate text
			text = self.generate_text(alphabets)
			# generate patterns
			num_patterns = random.randint(self.patterns_per_text_range[0], self.patterns_per_text_range[1])
			for j in range(num_patterns):
				self.cases_generated += 1
				pattern = self.generate_pattern(alphabets)
				# kmp vs naive match
				# print("text, pattern: ", text, " ", pattern)
				kmp_matches = kmp_string_match(text, pattern)
				naive_matches = naive_string_match(text, pattern)
				self.num_matches[len(kmp_matches)] = self.num_matches.get(len(kmp_matches), 0) + 1
				is_match = verify_matches(kmp_matches, naive_matches)
				if is_match:
					self.correct_cases += 1
				else:
					self.incorrect_cases += 1
					failed_cases.append((text, pattern))
		return failed_cases

#### end: KMP question #####

#### begin: Karp Rabin question #####
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

#### end: Karp Rabin question #####

if __name__ == "__main__":
	#### begin: Karp Rabin question driver #####
	input_str, tests = read_input("./testfiles/in.txt")
	q = int(math.pow(10, 7) + 7)
	r = 3
	rabinKarp = KarpRabin(r, q, input_str)
	results = []
	for test in tests:
		results.append(rabinKarp.query(test[0], test[1], test[2]))
	failed_tests, false_neg, false_pos = read_and_compare_output(results, "./testfiles/out.txt")
	print(failed_tests)
	print(false_neg)
	print(false_pos)
	#### end: Karp Rabin question driver #####

	#### begin: KMP question driver #####
	kmpdriver = KMPDriver(total_texts_range=[2, 3], patterns_per_text_range=[500, 600], text_len_range=[100, 200],
						  pattern_len_range=[2, 10], alphabet_len_range=[2, 4])
	failed_cases = kmpdriver.simulate()
	print(failed_cases)
	kmpdriver.print_stats()
	#### end: KMP question driver #####