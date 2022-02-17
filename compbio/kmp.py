import random


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
		num_texts = random.randint(self.total_texts_range[0], self.total_texts_range[1])
		print("num texts selected randomly: ", num_texts)
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


if __name__ == "__main__":
	# pi_test = compute_pi("abcdabcdaaaaaaaabcd")
	# print(pi_test)

	text = "ahayhyhyhaahhaah"
	pattern = "aah"

	print(naive_string_match(text, pattern))
	print(kmp_string_match(text, pattern))

	kmpdriver = KMPDriver(total_texts_range=[200, 300], patterns_per_text_range=[5000, 6000], text_len_range=[100, 200],
						  pattern_len_range=[2, 10], alphabet_len_range=[2, 4])
	kmpdriver.simulate()
	kmpdriver.print_stats()
