from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *

import tensorflow as tf
from tensorflow import keras
from PIL import Image

# Create your views here. 
def face_image_view(request): 
  
    if request.method == 'POST': 
        form = FaceForm(request.POST, request.FILES)
        request.FILES['Upload_Image'].name = 'upload.jpg'
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = FaceForm() 
    return render(request, 'face_image_form.html', {'form' : form}) 
  
def success(request):
    image = Image.open('./media/images/upload.jpg')
    if(request.GET.get('mybtn')):
        return redirect('home')
    return render(request, 'analysis.html')
