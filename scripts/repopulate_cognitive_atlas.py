import os
import json
import pandas
from cogpheno.apps.assessments.models import CognitiveAtlasTask, CognitiveAtlasConcept
    
from cognitiveatlas.api import get_task, get_concept
tasks = get_task()
concepts = get_concept()

for t in range(0,len(tasks.json)):
    task = tasks.json[t]
    print "%s of %s" %(t,len(tasks.json)) 
    task, _ = CognitiveAtlasTask.objects.update_or_create(cog_atlas_id=task["id"], defaults={"name":task["name"]})
    task.save()

# Or just update those not in
#termid_present = [ct.cog_atlas_id for ct in CognitiveAtlasTask.objects.all()]
#termid = [tasks.json[x]["id"] for x in range(0,len(tasks.json))]
#termid_missing = [x for x in range(0,len(termid)) if termid[x] not in termid_present]
#for m in termid_missing:
#    task = tasks.json[m]
#    task, _ = CognitiveAtlasTask.objects.update_or_create(cog_atlas_id=task["id"], defaults={"name":task["name"]})
#    task.save()

for c in range(0,len(concepts.json)):
    concept = concepts.json[c]
    print "%s of %s" %(c,len(concepts.json))
    concept, _ = CognitiveAtlasConcept.objects.update_or_create(cog_atlas_id=concept["id"], defaults={"name":concept["name"]},definition=concept["definition_text"])
    concept.save()

