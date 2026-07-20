from django.db import models

# Create your models here.
class roomtypedb(models.Model):
    ROOMTYPE=models.CharField(max_length=100,null=True,blank=True)
    ROOMTYPEIMAGE=models.ImageField(upload_to="roomtypeimages",null=True,blank=True)
    DESCRIPTION = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.ROOMTYPE or "No Type"

#
class roomnamedb(models.Model):
    ROOMTYPE = models.ForeignKey(roomtypedb, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')
    ROOMNAME=models.CharField(max_length=100,null=True,blank=True)
    ROOMIMAGE=models.ImageField(upload_to="roomimage",null=True,blank=True)
    ROOMPRICE=models.IntegerField(null=True,blank=True)
    ROOMDESCRIPTION=models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.ROOMNAME or "No Room Name"

class staffdb(models.Model):
    STAFFNAME = models.CharField(max_length=100, null=True, blank=True)
    STAFFDESIGNATION=models.CharField(max_length=100,null=True,blank=True)
    STAFFACEBOOK=models.CharField(max_length=100,null=True,blank=True)
    STAFFINSTA=models.CharField(max_length=100,null=True,blank=True)
    STAFFIMAGE=models.ImageField(upload_to="staffimage",null=True,blank=True)
    
    def __str__(self):
        return self.STAFFNAME or "No Name"

# Import chatbot models
from .chatbot_models import ChatbotResponse, ChatbotConversation, Notification