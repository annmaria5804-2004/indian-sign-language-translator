from django.db import models

# Create your models here.

class LoginTable(models.Model):
    username=models.CharField(max_length=100,null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    user_role=models.CharField(max_length=100,null=True,blank=True)
    
class UserTable(models.Model):
    fullname=models.CharField(max_length=100,null=True,blank=True)
    email=models.CharField(max_length=100,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,blank=True)
    phone_no=models.BigIntegerField(null=True,blank=True)
    LOGIN_ID=models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True,blank=True)
    
class ComplaintTable(models.Model):
    reply=models.CharField(max_length=100,null=True,blank=True)
    complaint=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField(auto_now_add=True,blank=True)
    USER_ID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    
class FeedbackTable(models.Model):
    date=models.DateField(auto_now_add=True,blank=True)
    feedback=models.CharField(max_length=100,null=True,blank=True)
    USER_ID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
