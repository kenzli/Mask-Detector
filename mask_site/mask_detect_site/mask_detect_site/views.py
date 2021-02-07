from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *

import os
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import cv2
import numpy as np
import math

model = load_model('model')

def dist(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

def area(v1, v2, v3):
    return (v2[0] - v1[0]) * (v3[1] - v2[1])

def detect_faces(path):
    """Detects faces in an image, and outlines them with rectangles"""
    from google.cloud import vision
    from PIL import Image, ImageDraw
    import io

    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    face_distance = [10000000] * len(faces)
    face_area = []
    face_vertices = []

    counter = 0
    for face in faces:
        face_vertices.append((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y))
        face_area.append(area((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y), 
            (face.bounding_poly.vertices[1].x, face.bounding_poly.vertices[1].y),
            (face.bounding_poly.vertices[2].x, face.bounding_poly.vertices[2].y)))
        im = Image.open(path)
        cropped = im.crop((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y, face.bounding_poly.vertices[2].x, face.bounding_poly.vertices[2].y))
        #cropped.show()
        cropped.save("./media/images/" + str(counter) + ".jpg")
        counter += 1
    
    for i in range(len(faces)):
        min_dist = 0
        for j in range(len(faces)):
            distance = dist(face_vertices[i], face_vertices[j])
            if distance > 0 and (face_area[i] + face_area[j]) / distance < face_distance[i]: 
                face_distance[i] = (face_area[i] + face_area[j]) / distance
        
    
    with Image.open(path) as im:
      counter = 0
      
      draw = ImageDraw.Draw(im)
      for face in faces:
        draw.rectangle([face.bounding_poly.vertices[counter].x, face.bounding_poly.vertices[counter].y,
          face.bounding_poly.vertices[counter + 2].x, face.bounding_poly.vertices[counter + 2].y], None, "#0000ff", 3)
      for i in range(len(faces)):
        if face_distance[i] < 30 or len(faces) == 1: colour = "#00ff00"
        else: colour = "#ff0000"
        draw.rectangle([faces[i].bounding_poly.vertices[0].x, faces[i].bounding_poly.vertices[0].y,
          faces[i].bounding_poly.vertices[2].x, faces[i].bounding_poly.vertices[2].y], None, colour, 3)
        draw.text((faces[i].bounding_poly.vertices[0].x - 10, faces[i].bounding_poly.vertices[0].y - 10), str(i+1), "#ff0000",font=None, anchor=None, spacing=4, align='left', direction=None, features=None, language=None, stroke_width=1, stroke_fill=None, embedded_color=False)

      im.save("./media/images/upload.jpg")
    return len(faces)
    if response.error.message:
        raise Exception('Error')

# Create your views here. 
def face_image_view(request): 
    #os.remove('./media/images/upload.jpg')
    if request.method == 'POST': 
        form = FaceForm(request.POST, request.FILES)
        request.FILES['Upload_Image'].name = 'upload.jpg'
  
        if form.is_valid(): 
            form.save() 
            #print("TO SUCCESS ")
            return redirect('success')
    else: 
        #print("TO HOME ")
        form = FaceForm() 
    return render(request, 'face_image_form.html', {'form' : form}) 
  
def success(request):
    #print("ABOUT TO RUN DETECT_FACES")
    nums = detect_faces('./media/images/upload.jpg')
    
    prediction = []
    output = ""
    for i in range(nums):
        image = cv2.imread('./media/images/' + str(i) + '.jpg')
        image = cv2.resize(image, (128,128))
        image = np.reshape(image, [1,128,128,3])
        image = image/255.0
        prediction.append(round(model.predict(image)[0][0]*100))
        if prediction[i] > 50: output += "Person " + str(i+1) + " has a mask on. \n"  
        else: output += "Person " + str(i+1) + " does not have a mask on. \n"  
    if(request.GET.get('mybtn')):
        os.remove('./media/images/upload.jpg')
        #for i in range(nums - 1):
            #os.remove('./media/images/' + str(i) + '.jpg')
        return redirect('home')
    return render(request, 'analysis.html', {'output' : output})
