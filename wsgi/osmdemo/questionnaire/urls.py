from django.conf.urls import url

import views

urlpatterns = [
	url(r'^questionnaire/(?P<questionnaire_id>\d+)$',views.questionnaire,name='questionnaire'),
    url(r'^$', views.index, name='index'),
]
