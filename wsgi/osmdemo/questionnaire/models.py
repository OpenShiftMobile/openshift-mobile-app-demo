from django.db import models

# Create your models here.
class Questionnaire(models.Model):
	title = models.CharField(max_length=200)

	def __unicode__(self):
		return self.title


class UserQuestionnaire(models.Model):
	email = models.EmailField()
	questionnaire = models.ForeignKey(Questionnaire)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s - %s" % (self.email,self.questionnaire)

	class Meta:
		ordering = ['email','created']


class Section(models.Model):
	name = models.CharField(max_length=60)
	questionnaire = models.ForeignKey(Questionnaire)
	order = models.IntegerField()

	def __unicode__(self):
		return "[%s] (%s) %s" % (self.questionnaire,self.order,self.name)

	class Meta:
		ordering = ['order']



class Question(models.Model):
	question = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	elem_type = models.CharField(max_length=200)
	section = models.ForeignKey(Section,related_name="questions")
	order = models.IntegerField()

	def __unicode__(self):
		return "%s: %s" % (self.section,self.question)

	class Meta:
		ordering = ['order']


class Answer(models.Model):
	answer = models.CharField(default="false",max_length=500)
	question = models.ForeignKey(Question,related_name="answers")
	user_questionnaire = models.ForeignKey(UserQuestionnaire,related_name="answers")

	def __unicode__(self):
		return "%s - %s - %s" % (self.user_questionnaire.email, self.question, self.answer)

	class Meta:
		ordering = ['question__section__order','question__order']
