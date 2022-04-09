def read_input(input_file):
	"""
	reads input from the given file
	format is as follows-
	first line: string
	second line: k
	next k lines: i, j, l
	"""
	test_cases = []
	with open(input_file) as f:
		lines = [line.rstrip() for line in f]
		input_string = lines[0]
		k = int(lines[1])
		for i in range(k):
			test_cases.append([int(x) for x in lines[i + 2].split(' ')])
	return input_string, test_cases


def read_and_compare_output(generated_output, output_file):
	"""
	verify the generated output against correct output
	:return: count of failing testcases
	"""
	count_failed = 0
	with open(output_file) as f:
		correct_output = [int(line.rstrip()) for line in f]
		n = len(generated_output)
		for i in range(n):
			if generated_output[i] != correct_output[i]:
				count_failed += 1
	return count_failed


def edit_distance(X, Y):
	"""
	Compute the edit distance between X and Y in O(mn) time and using exactly n + O(1) extra space

	:param X: string 1
	:param Y: string 2
	:return: edit distance
	"""
	m = len(X)
	n = len(Y)
	A = [j for j in range(0, n + 1)]
	print("m:", m)
	print("n:", n)
	print(A)
	for i in range(1, m + 1):
		init = i
		prev = init
		for j in range(1, n + 1):
			if X[i - 1] == Y[j - 1]:
				delta = 0
			else:
				delta = 1
			A[j - 1] = min(A[j - 1] + delta, A[j] + 1, prev + 1)
			prev = A[j - 1]
		for j in range(n, 0, -1):
			A[j] = A[j - 1]
		A[0] = init
		print(A)
	return A[n]


def edit_distance_on_substrings(input_str, i, j, l):
	"""
	Compute the edit distance between X[i..i+l) and Y[j..j+l),
	using exactly n + O(1) extra space

	:param input_str: the input string from which we take substrings
	:param i: the starting index of X (1 indexed)
	:param j: the starting index of Y (1 indexed)
	:param l: the length of substrings
	:return: the edit distance between X and Y
	"""
	m = l
	n = l
	A = [c for c in range(0, n + 1)]  # DP array which stores results for previous row (n extra space)

	for p in range(1, m + 1):  # iterate over X
		init = p  # base case
		prev = init  # stores the result of the prev index for this row
		for q in range(1, n + 1):  # iterate over X
			if input_str[p + i - 2] == input_str[q + j - 2]:  # check if the characters match
				delta = 0  # no change needed
			else:
				delta = 1  # substitution
			# ED(X[1..p],Y[1..q]) is the minimum of the 3 values below:
			# 1. ED(X[1..p-1],Y[1..q-1]) + delta, corresponds to A[q - 1] + delta
			# 2. ED(X[1..p-1],Y[1..q]) + 1, corresponds to A[q] + 1
			# 3. ED(X[1..p],Y[1..q-1]) + 1, corresponds to prev + 1

			# Note:  ED(X[1..p],Y[1..q]) is stored at position q-1
			# this works because that value is not needed (for this p value) going further
			A[q - 1] = min(A[q - 1] + delta, A[q] + 1, prev + 1)
			prev = A[q - 1]  # update this q index's result for next iteration

		for q in range(n, 0, -1):  # shift the values in A by 1 position
			A[q] = A[q - 1]
		A[0] = init  # the first value equals init
	return A[n]


if __name__ == "__main__":
	# print(edit_distance("abaefkaheflkaca", "acdhshahfalkfba"))
	# print(edit_distance_on_substrings("abaefkaheflkaca", 1, 6, 2))
	input_str, tests = read_input("./data/in.txt")
	results = []
	for test in tests:
		results.append(edit_distance_on_substrings(input_str, test[0], test[1], test[2]))
	failed_tests = read_and_compare_output(results, "./data/out.txt")
	print("Failed tests:", failed_tests)
