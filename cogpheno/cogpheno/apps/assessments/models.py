from django.db import models


# A behavioral assessment contains questions
class Assessment(models.Model):
    name = models.CharField(max_length=250)
    pub_date = models.DateTimeField('date published')
    cognitive_atlas_task = models.CharField(help_text="Link to <a href='http://www.cognitiveatlas.org/'>Cognitive Atlas</a> task", verbose_name="Cognitive Atlas task", max_length=200, null=True, blank=True)
    abbreviation = models.CharField(max_length=250,help_text="Assessment abbreviation")
    version = models.CharField(max_length=10,help_text="version")

# Questions belong to assessments
class Question(models.Model):

    DATA_TYPE_CHOICES = (
        ('LONGINT', 'Long Integer'),
        ('DATETIME', 'Date/Time'),
        ('TEXT', 'Text'),
        ('INT', 'Integer'),
    )

    assessment = models.ForeignKey(Assessment)
    text = models.CharField(max_length=500)
    label = models.CharField(max_length=250,help_text="question unique label",unique=True)
    required = models.BooleanField(choices=((False, 'Not required'),
                                                     (True, 'Required')),
                                                      default=True,verbose_name="Required")  
    data_type = models.CharField(
                    help_text=("Data type of the question answer"),
                    verbose_name="Data Type",
                    max_length=200, null=False, blank=False, choices=DATA_TYPE_CHOICES)

    def __str__(self):
        return self.text    


# Question Options belong to questions
class QuestionOption(models.Model):
    question = models.ForeignKey(Question)
    numerical_score = models.IntegerField()
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text    


# We can tag a question with a contrast and/or a concept
class Contrast(models.Model):
    question = models.ForeignKey(Question)
    cognitive_atlas_id = models.CharField(max_length=250,default=None)

    def __str__(self):
        return self.cogitive_atlas_id


class Concept(models.Model):
    question = models.ForeignKey(Question)
    cognitive_atlas_id = models.CharField(max_length=250,default=None)

    def __str__(self):
        return self.cogitive_atlas_id


# In future, possibly add an instantiation of an assessment 
# (pointing to an entire assessment, and an answer for each question)
