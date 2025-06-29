
from django.forms import ModelForm

from questionapp.models import *


class User_Form(ModelForm):
    class Meta:
        model = User_Model
        fields = ['abbreviation', 'age', 'gender', 'cancer_type', 'cancer_stage', 'treatment', 'profile']

class Instruction_Form(ModelForm):
    class Meta:
        model = Instructions_Model
        fields = ['title', 'content']

class Question_Form(ModelForm):
    class Meta:
        model = Question
        fields = [ 'category', 'option1', 'option2', 'option3', 'image']

class Result_Form(ModelForm):
    class Meta:
        model = Result
        fields = ['USERID', 'QUESTIONID', 'response_time', 'is_correct']