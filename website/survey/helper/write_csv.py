import csv
import statistics


def write_csv(file_name, precisions, recalls, fmeasures):
	with open(file_name, 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['', 'Precision', 'Recall', 'F-Meausre'])
		for i in range(len(precisions)):
			writer.writerow(['User ' + str(i + 1), precisions[i], recalls[i], fmeasures[i]])


def write_all():
	ress = statistics.get_all_precision_recall_fmeasure()
	file_names = ['city', 'company', 'job_title', 'experience_from', 'experience_to', 'college', 'major', 'degree',
	              'education_from', 'education_to']
	postfix = '.csv'

	for i in range(0, len(ress), 3):
		write_csv(file_names[i/3]+postfix, ress[i], ress[i+1], ress[i+2])