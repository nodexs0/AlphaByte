import numpy as np
import cv2

# Cargar la URL de la cámara
url = ''

cap = cv2.VideoCapture(url) # Crear objeto VideoCapture

winName = 'CAMARA'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while(1):
    
    cap.open(url) # Antes de capturar el frame abrimos la url
    
    ret,frame = cap.read() # Captura de frame
    
    frame = cv2.rotate(frame,cv2.ROTATE_180)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face = face_cascade.detectMultiScale(gray, 1.6, 5)

    print(len(face))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow(winName,frame)
    
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:
        break
     
cv2.destroyAllWindows()
