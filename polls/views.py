
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
#from django.http import Http404
#from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Choice, Question

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #template = loader.get_template('polls/index.htm')
  context = { 'latest_question_list': latest_question_list }
  #output = ','.join([q.question_text for q in latest_question_list])
  return render(request, 'polls/index.htm', context)
  #return HttpResponse(template.render(context, request))

def detail(request, question_id):
  #try:
    #question = Question.objects.get(pk=question_id)
  #except Question.DoesNotExist:
    #raise Http404("Question does not exist")
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.htm', {'question': question})
  #return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
  #response = "You're looking at the results of question %s."
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.htm', {'question': question})
  #return HttpResponse(response % question_id)

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.htm', {'question': question, 'error_message': "You didn't select a choice."})
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
  return HttpResponse("You're voting on question %s." % question_id)

class IndexView(generic.ListView):
  template_name = 'polls/index.htm'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.htm'

class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.htm'
