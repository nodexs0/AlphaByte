import numpy as np
import cv2

# Cargar la URL de la cámara
url = 'http://192.168.137.208/640x480.jpg'

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

# Crear el objeto del tracker
tracker = cv2.TrackerBoosting_create()

# Capturar el primer fotograma del video
ret, frame = cap.read()

# Seleccionar la región de interés (ROI) para el seguimiento
bbox = cv2.selectROI(winName, frame, fromCenter=False, showCrosshair=True)

# Inicializar el tracker con la ROI seleccionada
tracker.init(frame, bbox)

while True:
    cap.open(url) # Antes de capturar el frame abrimos la url
    ret, frame = cap.read() # Captura de frame
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Actualizar el tracker y obtener la nueva posición de la caja delimitadora
    success, bbox = tracker.update(frame)

    if success:
        # Dibujar la caja delimitadora en el fotograma
        (x, y, w, h) = [int(i) for i in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, 'Object tracked', (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
        cv2.circle(frame, (x+w//2, y+h//2), 5, (0, 255, 0), -1)
    else:
        cv2.putText(frame, 'Tracking failure detected', (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Detectar objetos en el fotograma
    classIds, confs, bbox = net.detect(frame, confThreshold=0.5)

    # Dibujar cajas delimitadoras y etiquetas de clase
    if len(classIds) > 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classId == 1:
                cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, 'Object detected', (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (x+w//2, y+h//2), 5, (0, 255, 0), -1)

    cv2.imshow(winName, frame)
    
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:
        break
     
cv2.destroyAllWindows()
