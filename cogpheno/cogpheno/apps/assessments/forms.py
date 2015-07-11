from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, TabHolder, Tab
from cogpheno.apps.assessments.models import Assessment, Question
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


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ("assessment","label","text","cognitive_atlas_concept","direction","data_type","options","required")

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):

        super(QuestionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout()
        tab_holder = TabHolder()
        self.helper.add_input(Submit("submit", "Save"))

