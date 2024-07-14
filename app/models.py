from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Idea(models.Model):
    approved_choices = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    idea_title = models.CharField(max_length=255)
    idea_description = models.CharField(max_length=1000)
    idea_instant_investment = models.IntegerField()
    idea_total_investment = models.IntegerField()
    idea_industry = models.CharField(max_length=50,blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    idea_posted_by_name= models.CharField(max_length=50,blank=True, null=True)
    idea_posted_by_mail= models.CharField(max_length=50,blank=True, null=True)
    idea_posted_by_mobile= models.IntegerField(blank=True, null=True)
    idea_posted_by_address= models.CharField(max_length=1000,blank=True, null=True)
    posted_datetime = models.DateTimeField(auto_now=True)
    idea_approved= models.CharField(max_length=3,choices=approved_choices,default='No')

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=399)

class Extra_token_request(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Agent_call_request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    Idea = models.ForeignKey(Idea, on_delete=models.CASCADE, unique=False)

class Idea_viewed(models.Model):
    # deal_choices = [
    #     ('NONE', 'NONE'),
    #     ('ON', 'ON'),
    #     ('OFF', 'OFF'),
    # ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    # investor_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
    # idea_provider_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
    viewed_at = models.DateTimeField(auto_now_add=True)

class Idea_bought(models.Model):
    # deal_choices = [
    #     ('NONE', 'NONE'),
    #     ('ON', 'ON'),
    #     ('OFF', 'OFF'),
    # ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    # investor_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
    # idea_provider_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
    bought_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
   gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
   user = models.OneToOneField(User,on_delete=callable)
   mobile = models.IntegerField(blank=True,null=True)
   address = models.CharField(max_length=1000,blank=True,null=True)
   profession = models.CharField(max_length=50,blank=True,null=True)
   gender = models.CharField(max_length=10,choices=gender_choices, default= 'Male')

class bugs_and_messages(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    mail = models.CharField(max_length=50)
    message = models.CharField(max_length=99999,blank=True,null=True)


class deal_status(models.Model):
    deal_choices = [
        ('NONE', 'NONE'),
        ('ON', 'ON'),
        ('OFF', 'OFF'),
    ]
    idea_id = models.IntegerField(blank=True,null=True)
    investor_username = models.CharField(max_length=255,blank=True,null=True)
    idea_provider_username = models.CharField(max_length=255,blank=True,null=True)
    investor_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
    idea_provider_deal_status= models.CharField(max_length=4,choices=deal_choices,default='NONE')
   

   


    