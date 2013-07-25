from django.db import models


# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=50)
	age = models.IntegerField()

	def __unicode__(self):
		return 'user: ' + str(self.id) + ', username: ' + self.name


class Answer(models.Model):
	user = models.ForeignKey(User)
	file = models.FilePathField()

	def __unicode__(self):
		return 'user: ' + str(self.user.id) + ', answer: ' + str(self.id) + ', file: ' + self.file


class Triple(models.Model):
	subject = models.CharField(max_length=100)
	predicate = models.CharField(max_length=30)
	object = models.CharField(max_length=100)
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