from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from cogpheno.apps.assessments.forms import AssessmentForm, QuestionForm
from cogpheno.apps.assessments.models import Assessment, Question
from django.http import HttpResponse
from django.shortcuts import render


# get assessment
def get_assessment(aid,request,mode=None):
    keyargs = {'pk':aid}
    try:
        assessment = Assessment.objects.get(**keyargs)
    except Assessment.DoesNotExist:
        raise Http404
    else:
        return assessment


# get question
def get_question(qid,request,mode=None):
    keyargs = {'pk':qid}
    try:
        question = Question.objects.get(**keyargs)
    except Question.DoesNotExist:
        raise Http404
    else:
        return question


# Add assessment
def edit_assessment(request,aid=None):

    page_header = "Add new assessment"

    # Editing an existing assessment
    if aid:
        assessment = get_assessment(aid,request)
        page_header = 'Edit assessment'
    else:
        assessment = Assessment()

    if request.method == "POST":
        form = AssessmentForm(request.POST, instance=assessment)

        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.save()

            context = {
                'assessment': assessment.name,
            }
            return HttpResponseRedirect(assessment.get_absolute_url())
    else:
        form = AssessmentForm(instance=assessment)

    context = {"form": form, "page_header": page_header}
    return render(request, "edit_assessment.html", context)


# Add question
def edit_question(request,qid=None):

    page_header = "Add new question"

    # Editing an existing assessment
    if qid:
        question = get_question(qid,request)
        page_header = 'Edit question'
    else:
        question = Question()

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question = form.save(commit=False)
            question.save()

            context = {
                'question': question.name,
            }
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = QuestionForm(instance=question)

    context = {"form": form, "page_header": page_header}
    return render(request, "edit_question.html", context)


# View a single assessment
def view_assessment(request, aid):
    assessment = get_assessment(aid,request)
    questions = assessment.question_set.all()
    context = {'assessment': assessment,
            'questions': questions,
            'aid':aid}

    return render_to_response('assessment_details.html', context)

# View a single question
def view_question(request, qid):
    question = get_question(qid,request)
    context = {'question': question,
            'qid':qid}

    return render_to_response('question_details.html', context)


# All assessments
def assessments_view(request):
    assessments = Assessment.objects.all()
    counts = [ assessment.question_set.count() for assessment in assessments ]
    context = {'assessments': assessments }
    return render(request, 'all_assessments.html', context)

# Delete an assessment
def delete_assessment(request, aid):
    assessment = get_assessment(aid,request)
    assessment.delete()
    return redirect('assessments')


# All questions
def questions_view(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'all_questions.html', context)

