from django.db import models


# Create your models here.
class User(models.Model):
	name = models.CharField(null=True, max_length=50, blank=True)
	group = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return 'user: ' + str(self.id) + ', username: ' + self.name + ', group: ' + str(self.group)


class Answer(models.Model):
	user = models.ForeignKey(User)
	file = models.FilePathField()
	overall_score = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return 'user: ' + str(self.user.id) + ', answer: ' + str(self.id) + ', file: ' + self.file


class Triple(models.Model):
	subject = models.CharField(max_length=100, null=True, blank=True)
	predicate = models.CharField(max_length=30, null=True, blank=True)
	object = models.CharField(max_length=100, null=True, blank=True)

	parse_subject = models.CharField(max_length=100, null=True, blank=True)
	parse_predicate = models.CharField(max_length=30, null=True, blank=True)
	parse_object = models.CharField(max_length=100, null=True, blank=True)

	score = models.IntegerField(null=True, blank=True)

	answer = models.ForeignKey(Answer)

	def __unicode__(self):
		return 'answer: ' + str(self.answer.id) + ', triple: ' + str(self.id)


class Data(models.Model):
	file_name = models.CharField(max_length=100, unique=True)
	user_group = models.IntegerField(null=True, blank=True)
	file_exists = models.BooleanField(default=False)
	file_url = models.CharField(max_length=150)
	rdf = models.BooleanField(default=0)
	type = models.CharField(default='PERSON', max_length=10)

	def __unicode__(self):
		return "data: " + self.file_name