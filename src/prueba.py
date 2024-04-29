import numpy as np
import cv2

# Cargar la URL de la cámara
url = 'http://192.168.137.129/640x480.jpg'

cap = cv2.VideoCapture(url) # Crear objeto VideoCapture

classNames = []
classFile = 'C:/Users/nodex/OneDrive/Escritorio/AlphaByte/resources/coco.names'

with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

winName = 'CAMARA'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# Cargar el modelo de detección de objetos pre-entrenado
configPath = 'C:\\Users\\nodex\\OneDrive\\Escritorio\\AlphaByte\\resources\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'

weightsPath = 'C:\\Users\\nodex\\OneDrive\\Escritorio\\AlphaByte\\resources\\frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    cap.open(url) # Antes de capturar el frame abrimos la url
    ret, frame = cap.read() # Captura de frame
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Detectar objetos en el fotograma
    classIds, confs, bbox = net.detect(frame, confThreshold=0.5)

    # Dibujar cajas delimitadoras y etiquetas de clase
    if len(classIds) > 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
            cv2.putText(frame, f'{classNames[classId-1]}: {confidence}', (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow(winName, frame)
    
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:
        break
     
cv2.destroyAllWindows()
