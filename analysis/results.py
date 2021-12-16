import matplotlib.pyplot as plt
import numpy as np


def plot_bar_graph():
	labels = ['Task 1', 'Task 2', 'Task 3']
	manual_means = [10.99,11.5675,27.47]
	ext_means = [8.495,7.2375,7.53]
	desk_means = [9.5775,9.6225,12.055]

	x = np.arange(len(labels))  # the label locations
	width = 0.2  # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(x - 3*(width/2), ext_means, width, label='PicoloExtension')
	rects2 = ax.bar(x - (width/2), desk_means, width, label='PicoloDesk')
	rects3 = ax.bar(x + (width/2), manual_means, width, label='Manual')

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_ylabel('Time')
	ax.set_title('Mean completion time by Task and Interface')
	ax.set_xticks(x, labels)
	ax.legend()

	ax.bar_label(rects1)
	ax.bar_label(rects2)
	ax.bar_label(rects3)

	# fig.tight_layout()
	plt.savefig('./mean_comparison.png')


if __name__ == '__main__':
	plot_bar_graph()