from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab
from cogpheno.apps.assessments.models import Assessment, Question, BehavioralTrait
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from django import forms



class AssessmentForm(ModelForm):

    class Meta:
        model = Assessment
        fields = ("name","pub_date","cognitive_atlas_task","abbreviation","version")
        widgets = {
            'pub_date': forms.DateInput(attrs={'class':'datepicker'}),
        }


    def clean(self):
        cleaned_data = super(AssessmentForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):

        super(AssessmentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout()
        tab_holder = TabHolder()
        self.helper.add_input(Submit("submit", "Save"))


class BehaviorForm(ModelForm):

    class Meta:
        model = BehavioralTrait
        fields = ("name","definition")

    def clean(self):
        cleaned_data = super(BehaviorForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):

        super(BehaviorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout()
        tab_holder = TabHolder()
        self.helper.add_input(Submit("submit", "Save"))


class AddConceptForm(forms.Form):
    new_concept = forms.CharField(label='Concept Name', max_length=100)

    def __init__(self, *args, **kwargs):

        super(AddConceptForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout()
        tab_holder = TabHolder()
        self.helper.add_input(Submit("submit", "Save"))


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ("assessment","label","text","behavioral_trait","direction","data_type","options","required")

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):

        super(QuestionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_id = "questionform"
        self.helper.layout = Layout()
        tab_holder = TabHolder()
        self.helper.add_input(Submit("submit", "Save"))

