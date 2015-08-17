from cogpheno.apps.assessments.forms import AssessmentForm, QuestionForm, AddConceptForm, BehaviorForm
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from cogpheno.apps.assessments.models import Assessment, Question, BehavioralTrait
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import uuid
import json
import csv

### AUTHENTICATION ####################################################

def owner_or_contrib(request,assessment):
    if assessment.owner == request.user or request.user in collection.contributors.all() or request.user.is_superuser:
        return True
    return False


#### GETS #############################################################

# get assessment
def get_assessment(aid,request,mode=None):
    keyargs = {'pk':aid}
    try:
        assessment = Assessment.objects.get(**keyargs)
    except Assessment.DoesNotExist:
        raise Http404
    else:
        return assessment


# get behavior
def get_behavior(bid,request,mode=None):
    keyargs = {'pk':bid}
    try:
        behavior = BehavioralTrait.objects.get(**keyargs)
    except BehavioralTrait.DoesNotExist:
        raise Http404
    else:
        return behavior


# get question
def get_question(qid,request,mode=None):
    keyargs = {'pk':qid}
    try:
        question = Question.objects.get(**keyargs)
    except Question.DoesNotExist:
        raise Http404
    else:
        return question

# Get the next and previous question
def get_next_previous_question(question):
    question_ids = [x.id for x in question.assessment.question_set.all()]
    idx = question_ids.index(int(question.id))
    if idx == len(question_ids)-1:
        next_question = question_ids[0]
        previous_question = question_ids[idx-1]
    else:
        next_question = question_ids[idx+1]
        previous_question = question_ids[idx-1]
    if idx == 0:
        previous_question = question_ids[len(question_ids)-1] 
    return next_question,previous_question

#### VIEWS #############################################################

# View a single assessment
def view_assessment(request, aid):
    assessment = get_assessment(aid,request)
    questions = assessment.question_set.all()
    context = {'assessment': assessment,
               'questions': questions,
               'aid':aid,
               'active':'assessments'}

    return render_to_response('assessment_details.html', context)

# View a single behavior
def view_behavior(request, bid):
    behavior = get_behavior(bid,request)
    context = {'behavior': behavior,
               'bid':bid,
               'active':'behaviors'}

    return render_to_response('behavior_details.html', context)

# View a single question
def view_question(request, qid):
    question = get_question(qid,request)
    next_question,previous_question = get_next_previous_question(question)
    context = {'question': question,
               'qid':qid,
               'active':'questions',
               'next_question':next_question,
               'previous_question':previous_question}

    return render_to_response('question_details.html', context)


# All assessments
def assessments_view(request):
    assessments = Assessment.objects.all()
    counts = [ assessment.question_set.count() for assessment in assessments ]
    context = {'assessments': assessments,
               'active' : 'assessments' }
    return render(request, 'all_assessments.html', context)


# All questions
def questions_view(request):
    questions = Question.objects.all()
    context = {'questions': questions,
               'active':'questions'}
    return render(request, 'all_questions.html', context)


# All behavior
def behaviors_view(request):
    behaviors = BehavioralTrait.objects.all()
    context = {'behaviors': behaviors,
               'active':'behaviors'}
    return render(request, 'all_behaviors.html', context)


#### EDIT/ADD/DELETE #############################################################

# Add assessment
@login_required
def edit_assessment(request,aid=None):

    # Editing an existing assessment
    if aid:
        assessment = get_assessment(aid,request)
    else:
        assessment = Assessment()

    if not owner_or_contrib(request,assessment):
        return HttpResponseForbidden()
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


# Edit a behavior
@login_required
def edit_behavior(request, bid):
    
    behavior = get_behavior(bid,request)

    if request.method == "POST":
        from textblob import Word
        behavior.name = request.POST.get("name", "")
        behavior.wordnet_synset = request.POST.get("synset", "")
        behavior.definition = request.POST.get("definition", "")
        behavior.save()
        context = {
                'behavior': behavior,
        }
        return HttpResponseRedirect(behavior.get_absolute_url())
    else:
        form =  BehaviorForm(instance=behavior)

    context = {"form": form, 
               "active":"behaviors",
               "behavior":behavior}

    return render(request,'edit_behavior.html', context)

# Edit a single question
@login_required
def edit_question(request,qid=None):

    page_header = "Add new question"
    next_question = None
    previous_question = None

    # Check if the user owns the assessment
    #if not owner_or_contrib(request,assessment):
    #    return HttpResponseForbidden()


    # Editing an existing question
    if qid:
        question = get_question(qid,request)
        page_header = 'Edit question'
        next_question,previous_question = get_next_previous_question(question)
 
    else:
        question = Question()

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question = form.save(commit=False)
            question.save()

            context = {
                'question': question,
                "active":"questions",
                "page_header":page_header
            }
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = QuestionForm(instance=question)

    # If the user wants to add a concept
    addconceptform = AddConceptForm()

    context = {"form": form, 
               "page_header": page_header,
               "active":"questions",
               "next_question": next_question,
               "previous_question" : previous_question,
               "question": question,
               "addconceptform" : addconceptform}

    return render(request, "edit_question.html", context)

# Delete an assessment
@login_required
def delete_assessment(request, aid):
    assessment = get_assessment(aid,request)
    assessment.delete()
    return redirect('assessments')


# Delete a behavior
@login_required
def delete_behavior(request, bid):
    behavior = get_behavior(bid,request)
    behavior.delete()
    return redirect('behaviors')


# Delete a question
@login_required
def delete_question(request, qid):
    question = get_question(qid,request)
    question.delete()
    return redirect('questions')


# Delete a question, redirect to next
@login_required
def delete_question_redirect(request, qid):
    question = get_question(qid,request)
    next_question,previous_question = get_next_previous_question(question)
    question.delete()
    next_question = get_question(next_question,request)
    return HttpResponseRedirect("%sedit" %next_question.get_absolute_url())
    
# Edit all questions view
@login_required
def edit_questions(request, assessment_aid, message=1):
    from cogpheno.apps.assessments.models import BehavioralTrait, Question
    assessment = get_assessment(assessment_aid, request)

    # Get all behavioral traits
    traits = BehavioralTrait.objects.all()
    behavioral_traits = [trait.name for trait in traits]
    behavioral_traits = '","'.join(behavioral_traits)

    # Update questions on post
    if request.method == "POST":
        
        try:
            data = request.POST.lists()
            content = request.POST.keys()
            # For each question
            for n in range(len(data[0][1])):
                new_question=dict()
                for i in range(len(content)):
                    label = data[i][0].replace("[]","")
                    value = data[i][1][n].replace('"',"").replace("\n"," ").replace("\r"," ")
                    new_question[label] = value
                    # Look up behavioral trait
                    if label == "behavioral_trait":
                        try:
                            trait = BehavioralTrait.objects.all().filter(name=value)[0]
                        except:
                            trait = BehavioralTrait.objects.all().filter(unique_id=value)[0]

                ques = Question.objects.get_or_create(assessment=assessment,label=new_question["label"].replace(" ",""))
                ques[0].text=new_question["text"]                          
                ques[0].data_type=new_question["data_type"]
                ques[0].behavioral_trait=trait
                ques[0].options=new_question["options"]
                ques[0].options=new_question["direction"]
                ques[0].save()
            return JsonResponse({"result":"success"})
        except:
            return JsonResponse({"result":"error"})
           
 
    # Retrieve all questions
    questions = get_questions(assessment)

    return render(request, "edit_questions.html", {
        'assessment': assessment,
        'questions': questions,
        'active':'questions',
        'behavioral_traits':behavioral_traits})

def get_questions(assessment):
    return assessment.question_set.all()


# Add a concept
@login_required
def add_concept(request,qid):
    if request.method == "POST":
        from cogpheno.apps.assessments.models import BehavioralTrait
        # Add the new concept
        new_concept = request.POST["new_concept"]
        concept = BehavioralTrait(unique_id=str(uuid.uuid4()),name=new_concept,definition="")
        concept.save()
    question = get_question(qid,request)
    return HttpResponseRedirect("%sedit" %question.get_absolute_url())

#### EXPORT #############################################################

# Export all questions for a single assessment
def export_assessment(request,aid):
    assessment = get_assessment(aid,request)
    output_name = "%s_%s.tsv" %(assessment.name.replace(" ","_"),len(assessment.question_set.all()))
    return export_assessments([assessment],output_name)
   
# Export all assessment questions
def export_questions(request):
    assessments = Assessment.objects.all()
    count = Question.objects.count()
    output_name = "cogPheno_%s.tsv" %(count)
    return export_assessments(assessments,output_name) 

# General function to export some number of assessments
def export_assessments(assessments,output_name):

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="%s"' %(output_name)

    writer = csv.writer(response,delimiter='\t')
    # Write header 
    writer.writerow(['assessment_name',
                     'assessment_number_questions',
                     'assessment_version',
                     'question_label', 
                     'question_text',
                     'question_behavioral_trait',
                     'question_behavioral_trait_id',
                     'question_behavioral_trait_synset',
                     'question_direction',
                     'question_id',
                     'question_datatype',
                     'question_options'])

    for assessment in assessments:
        for question in assessment.question_set.all():
            if question.behavioral_trait == None:
                synset = "None"
            else:
                synset = question.behavioral_trait.wordnet_synset
            writer.writerow([assessment.name,
                         len(assessment.question_set.all()),
                         assessment.version,
                         question.label,
                         question.text,
                         question.behavioral_trait,
                         question.behavioral_trait_id,
                         synset,
                         question.direction,
                         question.id,
                         question.data_type,
                         question.options.replace("\t"," ").replace(",","|").replace(";","|")])

    return response
