from django.http import HttpResponse
from django.shortcuts import render


# All assessments
def assessments_view(request):
    appname = "Cognitive Atlas Phenotype"
    context = {'appname': appname}
    return render(request, 'all_assessments.html', context)


# All questions
def questions_view(request):
    appname = "Cognitive Atlas Phenotype"
    context = {'appname': appname}
    return render(request, 'all_questions.html', context)

