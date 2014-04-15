from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.core.mail import send_mail
from questionnaire.models import *
import re,os

body_template = """
Thank you %s for your sumbission for the %s.

We appreciate your help in improving the OpenShift Mobile Project.

Thanks again,
The OpenShift Mobile Team
"""


def index(request):
	return render_to_response('questionnaire/questionnaire.html', {
		'questionnaire' : Questionnaire.objects.order_by('pk')[0]
	},context_instance=RequestContext(request))

def questionnaire(request,questionnaire_id):
	questionnaire = get_object_or_404(Questionnaire,pk=questionnaire_id)

	if len(request.POST):
		email = request.POST['email']
		if not re.match(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",email):
			return render_to_response('questionnaire/questionnaire.html', {
		'questionnaire' : questionnaire,
		'error' : 'Invalid Email Address'
	},context_instance=RequestContext(request))
		try:
			uq = UserQuestionnaire.objects.get(email=email,questionnaire=questionnaire)
			return render_to_response('questionnaire/questionnaire.html', {
				'questionnaire' : questionnaire,
				'error' : 'Questionnaire already submitted for this email address'
			},context_instance=RequestContext(request))
		except:
			resp = UserQuestionnaire(
				email = email,
				questionnaire = questionnaire
			)
			resp.save()

			sections = questionnaire.section_set.all()
			for section in sections:
				questions = section.questions.all()
				for question in questions:
					if question.name in request.POST:
						answer = Answer(
							answer = "true" if question.elem_type == 'checkbox' else request.POST[question.name],
							question = question,
							user_questionnaire = resp
						)
						answer.save()
					else:
						answer = Answer(
							answer = 'false',
							question = question,
							user_questionnaire = resp
						)
						answer.save()

			if 'EMAIL_HOST' in os.environ:
				subject,from_user = ('Thank You for You Submission!', os.environ['EMAIL_FROM'])
				body = body_template % (email,questionnaire.title)
				send_mail(subject,body,from_user,[email])

			return render_to_response('questionnaire/thanks.html', {
				'email' : email
			},context_instance=RequestContext(request))

	return render_to_response('questionnaire/questionnaire.html', {
		'questionnaire' : questionnaire
	},context_instance=RequestContext(request))
