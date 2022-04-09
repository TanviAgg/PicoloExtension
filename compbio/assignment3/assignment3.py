

def edit_distance(X, Y):
	m = len(X)
	n = len(Y)
	A = [j for j in range(0, n+1)]
	print("m:", m)
	print("n:", n)
	print(A)
	# init = None
	# prev = None
	for i in range(1, m+1):
		init = i
		prev = init
		for j in range(1, n+1):
			if X[i-1] == Y[j-1]:
				delta = 0
			else:
				delta = 1
			A[j-1] = min(A[j-1]+delta, A[j]+1, prev+1)
			prev = A[j-1]
		for j in range(n, 0, -1):
			A[j] = A[j-1]
		A[0] = init
		print(A)
	return A[n]


if __name__ == "__main__":
	print(edit_distance("abaefkaheflkaca", "acdhshahfalkfba"))