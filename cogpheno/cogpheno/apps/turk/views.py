from optparse import make_option
from django.core.management.base import BaseCommand
from boto.mturk.question import (AnswerSpecification, Overview, Question,
        QuestionContent, QuestionForm, FreeTextAnswer, FormattedContent)
from cogpheno.apps.turk.utils import get_connection, get_worker_url, get_worker_ids_past_tasks, get_host()


def get_questions(number=10,random_selection=False):

    

def turk_questions(request):

    host = get_host()
    #if request.GET.get("assignmentId") == "ASSIGNMENT_ID_NOT_AVAILABLE":
        # worker hasn't accepted the HIT (task) yet
    #    pass
    #else:
        # worked accepted the task
    #    pass

    worker_id = "WORKER_ID"
    #worker_id = request.GET.get("workerId", "")
    #if worker_id in get_worker_ids_past_tasks():
        # you might want to guard against this case somehow
    #    pass

    # Get a random sample of questions

    context = {
        "worker_id": worker_id,#request.GET.get("workerId", ""),
        "assignment_id": assignment_id,#request.GET.get("assignmentId", ""),
        "amazon_host": host,
        "hit_id": "hitID",#request.GET.get("hitId", ""),
    }

    response = render_to_response("mturk_question.html", context)
    # without this header, your iFrame will not render in Amazon
    response['x-frame-options'] = 'this_can_be_anything'
    return response
