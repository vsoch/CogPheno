import os
import json
from cogpheno.apps.assessments.models import CognitiveAtlasTask, CognitiveAtlasConcept
    
from cognitiveatlas.api import get_task, get_concept
tasks = get_task()
concepts = get_concept()

for task in tasks.json:
    task, _ = CognitiveAtlasTask.objects.update_or_create(cog_atlas_id=task["id"], defaults={"name":task["name"]})
    task.save()

for c in range(0,len(concepts.json)):
    concept = concepts.json[c]
    print "%s of %s" %(c,len(concepts.json))
    concept, _ = CognitiveAtlasConcept.objects.update_or_create(cog_atlas_id=concept["id"], defaults={"name":concept["name"]},definition=concept["definition_text"])
    concept.save()
