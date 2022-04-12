from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from main.models import Question

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreateQuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'vote_changeable']
        labels = {
            'question_text': _('Question Text'),
            'pub_date': _('Publish date and Time'),
            'vote_changeable': _('Can voters change their vote?')
        }
        
        
        
class EditQuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question 
        fields = ['pub_date']