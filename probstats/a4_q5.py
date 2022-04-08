import math
import numpy as np


def read_data(f_name):
	with open(f_name, 'r', encoding='utf-8-sig') as f:
		data = np.genfromtxt(f, autostrip=True)
	return data


def compute_normal_mme(data):
	"""
	Formulae used from Q2:
	Mean MME = sum(x)/n
	Variance MME= sum(x^2)/n - (sum(x)/n)^2

	:param data: sample data
	:return: MME of mean and variance for normal distribution
	"""
	n = len(data)
	mean_mme = data.sum() / n
	variance_mme = (((data ** 2).sum() / n) - ((data.sum() / n) ** 2))
	return round(mean_mme, 3), round(variance_mme, 3)


def compute_uniform_mme(data):
	"""
	Formulae used:
	sample_mean = sum(x)/n
	sample_std_dev = sqrt(sum(x^2)/n) - (sample_mean^2)
	a MME = sample_mean - sqrt(3*(sample_std_dev^2))
	b MME = sample_mean + sqrt(3*(sample_std_dev^2))

	:param data: sample data
	:return: MME of a and b for uniform distribution
	"""
	n = len(data)
	sample_mean = data.sum() / n
	sample_std_dev = math.sqrt(((data ** 2).sum() / n) - (sample_mean ** 2))
	a_mme = sample_mean - math.sqrt(3 * (sample_std_dev ** 2))
	b_mme = sample_mean + math.sqrt(3 * (sample_std_dev ** 2))
	return round(a_mme, 3), round(b_mme, 3)


def compute_exponential_mme(data):
	"""
	Formulae used:
	lambda_mme = n/sum(x)
	:param data: sample data
	:return: MME of lambda for exponential distribution
	"""
	n = len(data)
	lambda_mme = n / data.sum()
	return round(lambda_mme, 3)


def compute_normal_mle(data):
	"""
	Formulae used from Q2:
	Mean MLE = sum(x)/n
	Variance MLE = sum((x - mean MLE)^2)/n

	:param data: sample data
	:return: MLE of mean and variance for normal distribution
	"""
	n = len(data)
	mean_mle = data.sum() / n
	variance_mle = ((data - mean_mle) ** 2).sum() / n
	return round(mean_mle, 3), round(variance_mle, 3)


def compute_uniform_mle(data):
	"""
	Formulae used:
	m = min(data)
	M = max(data)
	a MLE = m
	b MLE = M

	:param data: sample data
	:return: MLE of a and b for uniform distribution
	"""
	a_mle = data.min()
	b_mle = data.max()
	return round(a_mle, 3), round(b_mle, 3)


def compute_exponential_mle(data):
	"""
	Formulae used:
	lambda_mle = n/sum(x)
	:param data: sample data
	:return: MLE of lambda for exponential distribution
	"""
	n = len(data)
	lambda_mle = n / data.sum()
	return round(lambda_mle, 3)


if __name__ == "__main__":
	mean_mme, variance_mme = compute_normal_mme(read_data('./datasets/acceleration_normal.csv'))
	print("######## Question 5c - MME ########")
	print("Acceleration data - Normal distribution mean = ", mean_mme)
	print("Acceleration data - Normal distribution variance = ", variance_mme)

	a_mme, b_mme = compute_uniform_mme(read_data('./datasets/model_uniform.csv'))
	print("Model data - Uniform distribution a = ", a_mme)
	print("Model data - Uniform distribution b = ", b_mme)

	lambda_mme = compute_exponential_mme(read_data('./datasets/mpg_exponential.csv'))
	print("MPG data - Exponential distribution lambda = ", round(lambda_mme, 3))

	print("######## Question 5d - MLE ########")
	mean_mle, variance_mle = compute_normal_mle(read_data('./datasets/acceleration_normal.csv'))
	print("Acceleration data - Normal distribution mean = ", mean_mle)
	print("Acceleration data - Normal distribution variance = ", variance_mle)

	a_mle, b_mle = compute_uniform_mle(read_data('./datasets/model_uniform.csv'))
	print("Model data - Uniform distribution a = ", a_mle)
	print("Model data - Uniform distribution b = ", b_mle)

	lambda_mle = compute_exponential_mle(read_data('./datasets/mpg_exponential.csv'))
	print("MPG data - Exponential distribution lambda = ", round(lambda_mle, 3))
