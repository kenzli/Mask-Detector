from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
  
# Create your views here. 
def face_image_view(request): 
  
    if request.method == 'POST': 
        form = FaceForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('success') 
    else: 
        form = FaceForm() 
    return render(request, 'face_image_form.html', {'form' : form}) 
  
def success(request):
     
    return HttpResponse('Successfully uploaded') 
