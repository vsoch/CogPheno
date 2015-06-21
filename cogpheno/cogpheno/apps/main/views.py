from django.shortcuts import render
from django.db.models.aggregates import Count

def index_view(request):
    appname = "Cognitive Atlas Phenotype"
    context = {'appname': appname}
    return render(request, 'index.html', context)
