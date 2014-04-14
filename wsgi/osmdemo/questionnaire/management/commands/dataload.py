from django.core.management.base import BaseCommand,CommandError
from questionnaire.models import *

def summitdemo():

	try:
		Questionnaire.objects.get(title='Red Hat Summit Questionnaire')
		return	
	except:
		pass

	qq = Questionnaire(
		title='Red Hat Summit Questionnaire'
	)
	qq.save()


	s1 = Section(
		name = 'Contact Info',
		questionnaire = qq,
		order = 1
	)
	s1.save()

	s1q1 = Question(
		question = 'Email Address',
		section = s1,
		name='email',
		elem_type = 'text',
		order = 1
	)
	s1q1.save()

	s2 = Section(
		name = 'Select Interests that Apply to You',
		questionnaire = qq,
		order = 2
	)
	s2.save()

	s2q1 = Question(
		question = 'Using Red Hat OpenShift',
		name = 'useos',
		elem_type = 'checkbox',
		section = s2,
		order = 1
	)
	s2q1.save()

	s2q2 = Question(
		question = 'Using OpenShift Mobile Personally',
		name= 'osmpersonal',
		elem_type='checkbox',
		section = s2,
		order = 2
	)
	s2q2.save()

	s2q3 = Question(
		question = 'Using OpenShift Mobile for Enterprise',
		name='osmenterprise',
		elem_type='checkbox',
		section = s2,
		order = 3
	)
	s2q3.save()

	s2q4 = Question(
		question = 'Contributing to OpenShift Mobile',
		name= 'osmcontrib',
		elem_type= 'checkbox',
		section = s2,
		order = 4
	)
	s2q4.save()

	s3 = Section(
		name = 'Feedback',
		questionnaire = qq,
		order = 3
	)
	s3.save()

	s3q1 = Question(
		question = 'Let us know what you think about the OpenShift Mobile project',
		name = 'feedback',
		elem_type = 'textarea',
		section = s3,
		order = 1
	)
	s3q1.save()



data_loads = {
	'summitdemo' : summitdemo
}



class Command(BaseCommand):

	def handle(self, *args, **options):
		for data in args:
			try:
				data_loads[data]()
				self.stdout.write('Data loaded for %s' % data)
			except:
				raise CommandError('Data failed to load for %s' % data)

