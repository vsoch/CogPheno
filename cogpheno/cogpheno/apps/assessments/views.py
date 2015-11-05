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
import os

### AUTHENTICATION ####################################################

def owner_or_contrib(request,assessment):
    if not request.user.is_anonymous():
        if owner_or_super(request,assessment) or request.user in assessment.contributors.all():
            return True
    return False

def owner_or_super(request,assessment):
    if not request.user.is_anonymous():
        if assessment.owner == request.user or request.user.is_superuser:
            return True
    return False

def check_question_edit_permission(request, assessment):
    if not request.user.is_anonymous():
        if owner_or_contrib(request,assessment):
            return True
    return False

def check_behavior_edit_permission(request):
    if not request.user.is_anonymous():
        if request.user.is_superuser:
            return True
    return False

def is_question_editor(request):
    if not request.user.is_anonymous():   
        if request.user.is_superuser:
            return True
    return False           

def is_behavior_editor(request):
    if request.user.is_superuser:
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

    # Determine permissions for edit and deletion
    edit_permission = True if owner_or_contrib(request,assessment) else False
    delete_permission = True if owner_or_super(request,assessment) else False
    edit_question_permission = True if check_question_edit_permission(request,assessment) else False

    context = {'assessment': assessment,
               'questions': questions,
               'edit_permission':edit_permission,
               'delete_permission':delete_permission,
               'question_permission':edit_question_permission,
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
    edit_question_permission = True if is_question_editor(request) else False
    context = {'questions': questions,
               'active':'questions',
               'edit_questions':edit_question_permission}
    return render(request, 'all_questions.html', context)


# All behavior
def behaviors_view(request):
    behaviors = BehavioralTrait.objects.all()
    edit_behavior_permission = True if is_behavior_editor(request) else False
    context = {'behaviors': behaviors,
               'active':'behaviors',
               'edit_behaviors':edit_behavior_permission}
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


# Edit a behavior from the behavior view
@login_required
def edit_behavior(request, bid):
        
    behavior = get_behavior(bid,request)
    edit_permission = check_behavior_edit_permission(request)

    if not edit_permission:
        return HttpResponseForbidden()

    if request.method == "POST":
        from textblob import Word
        behavior.name = request.POST.get("name", "")
        behavior.wordnet_synset = request.POST.get("synset", "")
        behavior.definition = request.POST.get("definition", "")
        behavior.save()
        context = {
                'behavior': behavior,
                'edit_permission': edit_permission
        }
        return HttpResponseRedirect(behavior.get_absolute_url())
    else:
        behaviorform =  BehaviorForm(instance=behavior)

    # Get questions that behavior is tagged for
    tagged_questions = Question.objects.filter(behavioral_trait=behavior)

    context = {"behaviorform": behaviorform, 
               "active":"behaviors",
               "behavior":behavior,
               "questions":tagged_questions}

    return render(request,'edit_behavior.html', context)

# Add a new behavior for a question
# Edit a single question
@login_required
def edit_question(request,qid=None):

    page_header = "Add new question"
    next_question = None
    previous_question = None

    # Editing an existing question
    if qid:
        question = get_question(qid,request)
        page_header = 'Edit question'
        next_question,previous_question = get_next_previous_question(question)
    else:
        question = Question()

    if not owner_or_contrib(request,question.assessment):
        return HttpResponseForbidden()

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


# Edit the behavior associated with a question (from question view)
@login_required
def view_behavior_question(request,qid):

    # Editing an existing question
    question = get_question(qid,request)
    behavior = question.behavioral_trait
    page_header = 'View question'
    next_question,previous_question = get_next_previous_question(question)

    context = {"page_header": page_header,
               "active":"questions",
               "next_question": next_question,
               "previous_question" : previous_question,
               "addconceptform" : AddConceptForm()}

    # Return edit question page showing edit behavior modal
    context["behaviorform"] = True 
    context["questions"] = Question.objects.filter(behavioral_trait=behavior)
    context["question"] = question
    context["form"] = QuestionForm(instance=question)
    
    return render(request, "edit_question.html", context)

# Edit a single question
@login_required
def edit_question(request,qid=None):

    page_header = "Add new question"
    next_question = None
    previous_question = None

    # Editing an existing question
    if qid:
        question = get_question(qid,request)
        page_header = 'Edit question'
        next_question,previous_question = get_next_previous_question(question)
    else:
        question = Question()

    if not owner_or_contrib(request,question.assessment):
        return HttpResponseForbidden()

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
    if request.user.owner == assessment.owner:
        assessment.delete()
        return redirect('assessments')
    return HttpResponseForbidden()

# Delete a behavior
@login_required
def delete_behavior(request, bid):
    if request.user.is_superuser:
        behavior = get_behavior(bid,request)
        behavior.delete()
        return redirect('behaviors')
    return HttpResponseForbidden()

# Delete a question
@login_required
def delete_question(request, qid):
    question = get_question(qid,request)
    if owner_or_contrib(request,question.assessment):
        question.delete()
        return redirect('questions')
    return HttpResponseForbidden()

# Delete a question, redirect to next
@login_required
def delete_question_redirect(request, qid):
    question = get_question(qid,request)
    next_question,previous_question = get_next_previous_question(question)
    if owner_or_contrib(request,question.assessment):
        question.delete()
        next_question = get_question(next_question,request)
        return HttpResponseRedirect("%sedit" %next_question.get_absolute_url())
    return HttpResponseForbidden()

# Edit all questions view
@login_required
def edit_questions(request, assessment_aid, message=1):
    from cogpheno.apps.assessments.models import BehavioralTrait, Question
    assessment = get_assessment(assessment_aid, request)

    # Determine permissions for edit and deletion
    edit_permission = True if owner_or_contrib(request,assessment) else False
    if not edit_permission:
        return HttpResponseForbidden()
  
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
    if not request.user.is_superuser:
        if not is_behavior_editor(request):
            return HttpResponseForbidden()

    if request.method == "POST":
        from cogpheno.apps.assessments.models import BehavioralTrait
        # Add the new concept
        new_concept = request.POST["new_concept"]
        make_new_concept(new_concept)
    question = get_question(qid,request)
    return HttpResponseRedirect("%sedit" %question.get_absolute_url())

def make_new_concept(name):
    from cogpheno.apps.assessments.models import BehavioralTrait
    from textblob import Word
    name = name.strip(" ")
    terms = [term.name for term in BehavioralTrait.objects.all()]
    if name not in terms:
        word = Word(name)
        syns = word.get_synsets()
        if syns:
            for syn in syns:
                concept = BehavioralTrait(unique_id=str(uuid.uuid4()),
                                          name=name,
                                          definition=syn.definition(),
                                          wordnet_synset=syn.name(),
                                          pos=syn.pos())
                concept.save()
        else:
            concept = BehavioralTrait(unique_id=str(uuid.uuid4()),name=name,definition="",pos="") 
            concept.save()

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
            # For now skip over questions with any bugs
            try:
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
            except:
                pass

    return response
