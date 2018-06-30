from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    # The auto generated context var is question_list. To override this we provide the 
    # the context_object_name attribute, speciflly that we use last_question_list instead. 
    # As an alternative approuch, you could change your templates to match the new 
    # default context variabbles - bt its a lot easer to just tell Django to use the 
    # variable you want. 

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    # The question variable is provided automatically -- since we're using a Django model (Question), 
    # Django is able to detemine an approprate name for the context vaiable
    template_name = 'polls/detail.html'
    # By default, the DetailView generic view uses a template call <app name>/<model name>_detail.html.
    # In our case, it was use the template "polls/question_detail.html". The template_name attribute is
    # usted to tell Django to use a specific template name instead of the autogen defautl. 

class ResultsView(generic.DetailView):
    model =  Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # request.POST is a dictionary-like object that lets you access submitted date by key name. 
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string. 
        # request.POST values are always strings! 
    except (KeyError, Choice.DoesNotExist):
        # request.POST['choice'] will raise KeyError if choice wasn't provided in POST data. 
        # the code check for KeyError and redispays the question form with a erro message if choice isn't given. 
        # Redispaly the question voting form. 
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "you didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return a HttpResponseRedirect after successfully dealing
        # with POST data, This prevents date from being posted twice if a 
        # user hits the Back button. 
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # After incrementing the choice count, the code returns an HttpResponseRedirect 
    # rather than a nornam HttpResponse. HttpResponseRedirect taks a singe argument:
    # the URL to which the user will be redirected. 

    # We are using the reverse() function in the HttpResponseRedirect constructor 
    # in this example. This function helps avoid having to hardcode a URL in the 
    # view function. It is given the name of the view that we want to pass control
    # to and the variable portion of the URL pattern that points to that view. 

