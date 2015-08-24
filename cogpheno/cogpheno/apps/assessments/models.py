from django.db.models import Q, DO_NOTHING
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models

class BehavioralTrait(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    unique_id = models.CharField(primary_key=True, max_length=200, null=False, blank=False)
    definition = models.CharField(max_length=1000, null=True, blank=True,default=None)
    wordnet_synset = models.CharField(max_length=200, null=True, blank=True,default=None)   
    pos = models.CharField(max_length=10, null=True, blank=True,default=None)   

    def __str__(self):
        return "%s: %s (%s)" %(self.name,self.definition,self.pos)
    
    def __unicode__(self):
        return "%s: %s (%s)" %(self.name,self.definition,self.pos)
    
    class Meta:
        ordering = ['name']

    # Get the url for a behavior
    def get_absolute_url(self):
        return_bid = self.pk
        return reverse('behavior_details', args=[str(return_bid)])


class CognitiveAtlasTask(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    cog_atlas_id = models.CharField(primary_key=True, max_length=200, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class CognitiveAtlasConcept(models.Model):
    name = models.CharField(max_length=1000, null=False, blank=False)
    cog_atlas_id = models.CharField(primary_key=True, max_length=200, null=False, blank=False)
    definition = models.CharField(max_length=5000, null=False, blank=False,default=None)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


# A behavioral assessment contains questions
class Assessment(models.Model):
    name = models.CharField(max_length=250)
    pub_date = models.DateTimeField('date published')
    cognitive_atlas_task = models.ForeignKey(CognitiveAtlasTask, help_text="Assessment defined in the <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a>", verbose_name="Cognitive Atlas Task", null=True, blank=False, on_delete=DO_NOTHING)
    abbreviation = models.CharField(max_length=250,help_text="Assessment abbreviation",default=None,null=True,blank=True)
    version = models.CharField(max_length=10,help_text="version",null=True,blank=True)
    owner = models.ForeignKey(User,default=None,null=True,blank=True)
    contributors = models.ManyToManyField(User,related_name="assessment_contributors",related_query_name="contributor", blank=True,help_text="Select other CogatPheno users to add as contributes to the assessment.  Contributors can add, edit and delete questions in the assessment.",verbose_name="Contributors")

    def __str__(self):
        return self.name

    # Get the url for an assessment
    def get_absolute_url(self):
        return_cid = self.id
        return reverse('assessment_details', args=[str(return_cid)])

# Questions belong to assessments
class Question(models.Model):

    DATA_TYPE_CHOICES = (
        ('LONGINT', 'Long Integer'),
        ('DATETIME', 'Date/Time'),
        ('TEXT', 'Text'),
        ('INT', 'Integer'),
        ('DOUBLE', 'Double')
    )

    assessment = models.ForeignKey(Assessment)
    behavioral_trait = models.ForeignKey(BehavioralTrait, help_text="Behavioral trait described by the question", verbose_name="Behavioral Trait", null=True, blank=False,on_delete=DO_NOTHING)
    text = models.CharField(max_length=500)
    label = models.CharField(max_length=250,help_text="question unique label",unique=True)
    required = models.BooleanField(choices=((False, 'Not required'),
                                            (True, 'Required')),
                                            default=True,verbose_name="Required") 
    direction = models.CharField(choices=(("positive", 'Positive (same direction)'),
                                          ("negative", 'Negative (inverse relationship)')),
                                          default="positive",verbose_name="Directionality",
                                          max_length=10)
 
    data_type = models.CharField(
                    help_text=("Data type of the question answer"),
                    verbose_name="Data Type",
                    max_length=200, null=False, blank=False, choices=DATA_TYPE_CHOICES)
    options = models.CharField(max_length=500,default=None,null=True)

    def __str__(self):
        return self.text    

    # Get the url for a question
    def get_absolute_url(self):
        return_cid = self.id
        return reverse('question_details', args=[str(return_cid)])

# In future, possibly add an instantiation of an assessment 
# (pointing to an entire assessment, and an answer for each question)

# Question Options belong to questions
class QuestionOption(models.Model):
    questions = models.ManyToManyField(Question)
    numerical_score = models.IntegerField()
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text    


