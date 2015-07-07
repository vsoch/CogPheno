from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied, ValidationError
from cogpheno.apps.assessments.forms import AssessmentForm, QuestionForm
from cogpheno.apps.assessments.models import Assessment, Question
from django.http import HttpResponse
from django.shortcuts import render
import json

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

    # Editing an existing assessment
    if aid:
        assessment = get_assessment(aid,request)
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

    context = {"form": form, "active":"assessments"}
    return render(request, "edit_assessment.html", context)


# Edit a single question
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
                'question': question,
                "active":"questions"
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
            'aid':aid,
            'active':'assessments'}

    return render_to_response('assessment_details.html', context)

# View a single question
def view_question(request, qid):
    question = get_question(qid,request)
    context = {'question': question,
               'qid':qid,
               'active':'questions'}

    return render_to_response('question_details.html', context)


# All assessments
def assessments_view(request):
    assessments = Assessment.objects.all()
    counts = [ assessment.question_set.count() for assessment in assessments ]
    context = {'assessments': assessments,
               'active' : 'assessments' }
    return render(request, 'all_assessments.html', context)

# Delete an assessment
def delete_assessment(request, aid):
    assessment = get_assessment(aid,request)
    assessment.delete()
    return redirect('assessments')


# Delete a question
def delete_question(request, qid):
    question = get_question(qid,request)
    question.delete()
    return redirect('questions')


# All questions
def questions_view(request):
    questions = Question.objects.all()
    context = {'questions': questions,
               'active':'questions'}
    return render(request, 'all_questions.html', context)


# Edit all questions view
def edit_questions(request, assessment_aid):
    from cogpheno.apps.assessments.models import CognitiveAtlasConcept, Question
    assessment = get_assessment(assessment_aid, request)

    # Get all cognitive atlas concepts
    concepts = CognitiveAtlasConcept.objects.all()
    cognitive_atlas_concepts = [ca.name for ca in concepts]
    cognitive_atlas_concepts = '","'.join(cognitive_atlas_concepts)

    # Update questions on post
    if request.method == "POST":
        import pickle
        pickle.dump(request.POST,open("/home/vanessa/Desktop/test.pkl","wb"))
        
        data = request.POST.lists()
        content = request.POST.keys()
        # For each question
        for n in range(len(data[0][1])):
            new_question=dict()
            for i in range(len(content)):
                label = data[i][0].replace("[]","")
                value = data[i][1][n]
                new_question[label] = value
                # Look up cognitive atlas concept
                if label == "cognitive_atlas_concept":
                    try:
                       concept = CognitiveAtlasConcept.objects.all().filter(name=value)[0]
                    except:
                       concept = CognitiveAtlasConcept.objects.all().filter(cog_atlas_id=value)[0]
            Question.objects.update_or_create(assessment=assessment, 
                                          text=new_question["text"],
                                          label=new_question["label"],
                                          data_type=new_question["data_type"],
                                          required=bool(new_question["required"]),
                                          cognitive_atlas_concept=concept)

        
    else:
        message=""
 
    # Retrieve all questions
    questions = get_questions(assessment)

    return render(request, "edit_questions.html", {
        'assessment': assessment,
        'questions': questions,
        'active':'questions',
        'cognitive_atlas_concepts':cognitive_atlas_concepts,
        'mess':message})

def get_questions(assessment):
    return assessment.question_set.all()

