from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from questionnaire.models import *
import re

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
			#TODO: Send email
			return render_to_response('questionnaire/thanks.html', {
				'email' : email
			},context_instance=RequestContext(request))

	return render_to_response('questionnaire/questionnaire.html', {
		'questionnaire' : questionnaire
	},context_instance=RequestContext(request))
