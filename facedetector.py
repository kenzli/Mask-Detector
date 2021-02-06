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

    print('Faces:' + str(len(faces)))
    for face in faces:
        print(face.bounding_poly.vertices[0])
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
    
    with Image.open(path) as im:
      counter = 0
      draw = ImageDraw.Draw(im)
      for face in faces:
        draw.rectangle([face.bounding_poly.vertices[counter].x, face.bounding_poly.vertices[counter].y,
          face.bounding_poly.vertices[counter + 2].x, face.bounding_poly.vertices[counter + 2].y], None, "#0000ff", 3)

      # write to stdout
      im.show()

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_faces("masks.jpg")