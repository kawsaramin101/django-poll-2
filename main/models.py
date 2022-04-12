import datetime 

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Voter(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, null=False, blank=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)


class Question(models.Model):
    creator = models.ForeignKey(User, related_name="polls", null=True, blank=False, on_delete=models.SET_NULL)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    voters = models.ManyToManyField(Voter, related_name="participated_question")
    vote_changeable = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question_text
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    @property
    def totol_votes(self):
        return self.voters.all().count()
        
        
class Choice(models.Model):
    creator = models.ForeignKey(User, related_name="created_choices", null=True, blank=False, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    voters = models.ManyToManyField(Voter, through='Vote')
    
    def __str__(self):
        return self.choice_text
        
    @property
    def votes(self):
        return self.voters.count()
    
    #def vote(self, voter):
        #for choice in self.question.choices.all():
            #if voter in choice.voters.all():
                #if not self.question.vote_changeable:
                    #raise Exception("You have already voted, vote cannot be changed for this poll") 
                #else:
                    #choice.voters.remove(voter)
        #self.voters.add(voter)
        #self.question.voters.add(voter)
    

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE, related_name="votes")
    
    class Meta:
        unique_together = ["choice", "voter"]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.choice.question.voters.add(self.voter)
        
    