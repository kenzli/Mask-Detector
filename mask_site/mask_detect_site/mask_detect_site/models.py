from django.db import models

class Face(models.Model): 
    name = models.CharField(max_length=50) 
    Upload_Image = models.ImageField(upload_to='images/') 
    