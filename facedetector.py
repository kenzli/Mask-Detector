#def detect_distance()
import math

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

    for face in faces:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        face_vertices.append((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y))
        face_area.append(area((face.bounding_poly.vertices[0].x, face.bounding_poly.vertices[0].y), 
            (face.bounding_poly.vertices[1].x, face.bounding_poly.vertices[1].y),
            (face.bounding_poly.vertices[2].x, face.bounding_poly.vertices[2].y)))

    
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

      # write to stdout
      #im.save(path)
      im.show()

    if response.error.message:
        raise Exception('Error')

detect_faces("ex1.JPG")
detect_faces("ex2.JPG")
detect_faces("ex3.JPG")
