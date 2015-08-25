#!/usr/bin/python
import numpy
from textblob import Word

from cogpheno.apps.assessments.models import BehavioralTrait
from cogpheno.apps.assessments.views import

for term in terms:
    make_new_concept(term)

from textblob.wordnet import Synset

# Add parts of speech
for behavior in BehavioralTrait.objects.all():
    if behavior.wordnet_synset:
        synset = Synset(behavior.wordnet_synset)
        behavior.pos = synset.pos()
        behavior.save()        

    
    
