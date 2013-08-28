import matplotlib.pyplot as plt
import numpy as np
from survey.models import *
from django.conf import settings
from django.db.models import Q


def auto_label(rects, ax, param):
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width() / 2., param * height, '%.3f' % height,
		        ha='center', va='bottom')


def show_avg_bar_chart(field='overall_score'):
	values = []
	users = range(1, settings.NUM_GROUPS * 2 + 1)[:9]
	for user_id in users:
		answer_id_start = (user_id - 1) * settings.NUM_FILES + 1
		answer_id_end = user_id * settings.NUM_FILES
		ans = Answer.objects.filter(id__in=range(answer_id_start, answer_id_end + 1))
		objs = ans
		value = float(sum([getattr(obj, field) if getattr(obj, field) else 3 for obj in objs])) / len(objs)
		values.append(value)


def get_user_ids():
	return range(1, settings.NUM_GROUPS * 2 + 1)


def get_answer_id_start_end(user_id):
	answer_id_start = (user_id - 1) * settings.NUM_FILES + 1
	answer_id_end = user_id * settings.NUM_FILES

	return answer_id_start, answer_id_end


def get_ans_by_user(user_id):
	start, end = get_answer_id_start_end(user_id)
	return Answer.objects.filter(id__in=range(start, end))


def get_objs_by_user(class_name, user_id):
	start, end = get_answer_id_start_end(user_id)

	# get class by name
	C = globals()[class_name]
	objs = getattr(getattr(C, 'objects'), 'filter')(answer__in=range(start, end + 1))
	return objs


def get_values(objs, field, extra=False):
	if not extra:
		return float(sum([getattr(obj, field) if getattr(obj, field) else 0 for obj in objs])) / len(objs)
	else:
		return float(sum(
			[getattr(obj, field) if getattr(obj, field) else 0 if getattr(obj, extra) else 3 for obj in objs])) / len(
			objs)


def show_bar_chart(idxs, values, text, param=0.995, save_text='tmp', save=False, usr='user '):
	t = ()
	for u in idxs:
		t = t + (usr + str(u),)
	t = t + ('average', )
	fig, ax = plt.subplots()
	width = 1.0
	ind = np.arange(len(idxs)+1)
	rect = ax.bar(ind, values, color='y', width=width)

	ax.set_ylabel('Avg ratings')
	ax.set_title(text)
	ax.set_xticks(ind + width / 2)
	ax.set_xticklabels(t)
	auto_label(rect, ax, param)
	for label in ax.xaxis.get_majorticklabels():
		label.set_fontsize(13)
		label.set_rotation(30)

	if save:
		plt.savefig('/Users/jinwu/GitHub/MasterDissertation/images/' + save_text + '.png')
		plt.close()
	else:
		plt.show()


def show_all_bar_chart():
	user_ids = get_user_ids()

	overall_scores = []
	city_scores = []
	company_scores = []
	job_title_scores = []
	experience_date_from_scores = []
	experience_date_to_scores = []
	college_scores = []
	major_scores = []
	degree_scores = []
	education_date_from_scores = []
	education_date_to_scores = []

	for user_id in user_ids:
		ans = get_ans_by_user(user_id)
		overall_scores.append(get_values(ans, 'overall_score'))
		city_scores.append(get_values(ans, 'city_score', extra='city'))

		exps = get_objs_by_user('Experience', user_id)
		company_scores.append(get_values(exps, 'parse_company_score', extra='company'))
		job_title_scores.append(get_values(exps, 'parse_job_title_score', extra='job_title'))
		experience_date_from_scores.append(get_values(exps, 'parse_date_from_score', extra='date_from'))
		experience_date_to_scores.append(get_values(exps, 'parse_date_to_score', extra='date_to'))

		edus = get_objs_by_user('Education', user_id)
		college_scores.append(get_values(edus, 'parse_college_score', extra='college'))
		major_scores.append(get_values(edus, 'parse_major_score', extra='major'))
		degree_scores.append(get_values(edus, 'parse_degree_score', extra='degree'))
		education_date_from_scores.append(get_values(edus, 'parse_date_from_score', extra='date_from'))
		education_date_to_scores.append(get_values(edus, 'parse_date_to_score', extra='date_to'))

	city_scores.append(sum(city_scores)/len(city_scores))
	company_scores.append(sum(company_scores) / len(company_scores))
	job_title_scores.append(sum(job_title_scores) / len(job_title_scores))
	experience_date_from_scores.append(sum(experience_date_from_scores) / len(experience_date_from_scores))
	experience_date_to_scores.append(sum(experience_date_to_scores) / len(experience_date_to_scores))
	college_scores.append(sum(college_scores) / len(college_scores))
	major_scores.append(sum(major_scores) / len(major_scores))
	degree_scores.append(sum(degree_scores) / len(degree_scores))
	education_date_from_scores.append(sum(education_date_from_scores) / len(education_date_from_scores))
	education_date_to_scores.append(sum(education_date_to_scores) / len(education_date_to_scores))

	show_bar_chart(user_ids, city_scores, text='City ratings', save_text='average_city_score', save=True)
	show_bar_chart(user_ids, company_scores, param=0.95, text='Company ratings', save_text='average_company_score', save=True)
	show_bar_chart(user_ids, job_title_scores, param=0.95, text='Job title ratings', save_text='average_job_title_score', save=True)
	show_bar_chart(user_ids, experience_date_from_scores, text='Work start date ratings', save_text='average_experience_start_date_score', save=True)
	show_bar_chart(user_ids, experience_date_to_scores, text='Work end date ratings', save_text='average_experience_end_date_score', save=True)
	show_bar_chart(user_ids, college_scores, param=0.95, text='College ratings', save_text='average_college_score', save=True)
	show_bar_chart(user_ids, major_scores, text='Major ratings', save_text='average_major_score', save=True)
	show_bar_chart(user_ids, degree_scores, text='Degree ratings', save_text='average_degree_score', save=True)
	show_bar_chart(user_ids, education_date_from_scores, text='Education start date ratings', save_text='average_education_start_date_score', save=True)
	show_bar_chart(user_ids, education_date_to_scores, text='Education end date ratings', save_text='average_education_end_date_score', save=True)


def get_precision_recall_fmeasure(objs, field, parse_field):
	print 'field', field
	correct_predicted = 0.0
	predicted = 0.0
	for obj in objs:
		if getattr(obj, field):
			value = getattr(obj, field).strip().lower()
		else:
			value = ''
		if getattr(obj, parse_field):
			parse_value = getattr(obj, parse_field).strip().lower()
		else:
			parse_value = ''

		if value == parse_value:
			correct_predicted += 1.0
		else:
			if value and not parse_value:
				pass
			elif parse_value and not value:
				correct_predicted += 1.0
			else:
				if field == 'date_from' or field == 'date_to':
					correct_predicted += 1.0

		print 'value:', value, ', parse value:', parse_value
		if parse_value or not value:
			predicted += 1.0
	if predicted:
		precision = correct_predicted / predicted
	else:
		precision = 0
	recall = correct_predicted / len(objs)
	print 'precision', precision, 'recall', recall
	if not precision and not recall:
		fmeasure = 0.0
	else:
		fmeasure = 2 * precision * recall / (precision + recall)

	return precision, recall, fmeasure


def get_all_precision_recall_fmeasure():
	user_ids = get_user_ids()

	city_precisions = []
	city_recalls = []
	city_fmeasures = []

	company_precisions = []
	company_recalls = []
	company_fmeasures = []

	job_title_precisions = []
	job_title_recalls = []
	job_title_fmeasures = []

	experience_from_precisions = []
	experience_from_recalls = []
	experience_from_fmeasures = []

	experience_to_precisions = []
	experience_to_recalls = []
	experience_to_fmeasures = []

	college_precisions = []
	college_recalls = []
	college_fmeasures = []

	major_precisions = []
	major_recalls = []
	major_fmeasures = []

	degree_precisions = []
	degree_recalls = []
	degree_fmeasures = []

	education_from_precisions = []
	education_from_recalls = []
	education_from_fmeasures = []

	education_to_precisions = []
	education_to_recalls = []
	education_to_fmeasures = []

	for user_id in user_ids:
		print 'user_id: ', user_id
		ans = get_ans_by_user(user_id)
		p, r, f = get_precision_recall_fmeasure(ans, 'city', 'parse_city')
		city_precisions.append(p)
		city_recalls.append(r)
		city_fmeasures.append(f)

		exps = get_objs_by_user('Experience', user_id)
		p, r, f = get_precision_recall_fmeasure(exps, 'company', 'parse_company')
		company_precisions.append(p)
		company_recalls.append(r)
		company_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(exps, 'job_title', 'parse_job_title')
		job_title_precisions.append(p)
		job_title_recalls.append(r)
		job_title_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(exps, 'date_from', 'parse_date_from')
		experience_from_precisions.append(p)
		experience_from_recalls.append(r)
		experience_from_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(exps, 'date_to', 'parse_date_to')
		experience_to_precisions.append(p)
		experience_to_recalls.append(r)
		experience_to_fmeasures.append(f)

		edus = get_objs_by_user('Education', user_id)
		p, r, f = get_precision_recall_fmeasure(edus, 'college', 'parse_college')
		college_precisions.append(p)
		college_recalls.append(r)
		college_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(edus, 'major', 'parse_major')
		major_precisions.append(p)
		major_recalls.append(r)
		major_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(edus, 'degree', 'parse_degree')
		degree_precisions.append(p)
		degree_recalls.append(r)
		degree_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(edus, 'date_from', 'parse_date_from')
		education_from_precisions.append(p)
		education_from_recalls.append(r)
		education_from_fmeasures.append(f)
		p, r, f = get_precision_recall_fmeasure(edus, 'date_to', 'parse_date_to')
		education_to_precisions.append(p)
		education_to_recalls.append(r)
		education_to_fmeasures.append(f)

	return city_precisions, city_recalls, city_fmeasures, company_precisions, company_recalls, company_fmeasures, job_title_precisions, job_title_recalls, job_title_fmeasures, experience_from_precisions, experience_from_recalls, experience_from_fmeasures, experience_to_precisions, experience_to_recalls, experience_to_fmeasures, college_precisions, college_recalls, college_fmeasures, major_precisions, major_recalls, major_fmeasures, degree_precisions, degree_recalls, degree_fmeasures, education_from_precisions, education_from_recalls, education_from_fmeasures, education_to_precisions, education_to_recalls, education_to_fmeasures