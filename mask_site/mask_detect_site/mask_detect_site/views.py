from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *

import os
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import cv2
import numpy as np

model = load_model('model')
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
    image = cv2.imread('./media/images/upload.jpg')
    image = cv2.resize(image, (128,128))
    image = np.reshape(image, [1,128,128,3])
    image = image/255.0
    
    prediction = model.predict(image)
    prediction = prediction[0][0]
    
    if(request.GET.get('mybtn')):
        os.remove('./media/images/upload.jpg')
        return redirect('home')
    return render(request, 'analysis.html', {'prediction' : prediction})
