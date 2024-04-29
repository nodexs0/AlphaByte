# Librerías
import numpy as np
import cv2

# URL de la cámara IP
url = ''

# Inicializar la captura de video
cap = cv2.VideoCapture(url)

# Cargar las clases de COCO
classNames = []

# Ruta del archivo de clases
classFile = 'C:/Users/nodex/OneDrive/Escritorio/AlphaByte/resources/coco.names'

# Leer las clases del archivo
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Crear una ventana para mostrar la cámara
winName = 'CAMARA'

# Crear la ventana
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# Cargar el modelo de detección de objetos pre-entrenado
configPath = 'C:\\Users\\nodex\\OneDrive\\Escritorio\\AlphaByte\\resources\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'C:\\Users\\nodex\\OneDrive\\Escritorio\\AlphaByte\\resources\\frozen_inference_graph.pb'

# Cargar el modelo y configurar la entrada
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Inicializar la caja delimitadora previa
prev_bbox = None
min_diff_threshold = 60

# Bucle principal
while True:
    # Abrir la cámara IP
    cap.open(url)

    # Leer un fotograma de la cámara
    ret, frame = cap.read()

    # Rotar el fotograma 180 grados
    frame = cv2.rotate(frame, cv2.ROTATE_180)

    # Detectar objetos en el fotograma
    classIds, confs, bbox = net.detect(frame, confThreshold=0.5)

    # Dibujar cajas delimitadoras y etiquetas de clase
    if len(classIds) > 0:
        for classId, confidence, box in zip(classIds[0].flatten(), confs.flatten(), bbox):
            if classId == 1:
                # Si tenemos una caja delimitadora previa, calculamos su diferencia con la actual
                if prev_bbox is not None:
                    prev_x, prev_y, prev_w, prev_h = prev_bbox
                    curr_x, curr_y, curr_w, curr_h = box

                    # Calcular la diferencia entre las coordenadas de la caja delimitadora actual y previa
                    diff_x = curr_x - prev_x
                    diff_y = curr_y - prev_y
                    diff_w = curr_w - prev_w
                    diff_h = curr_h - prev_h

                    # Actualizar la caja delimitadora previa si la diferencia es mayor que el umbral
                    if abs(diff_x) > min_diff_threshold or abs(diff_y) > min_diff_threshold or abs(diff_w) > min_diff_threshold or abs(diff_h) > min_diff_threshold:
                        prev_bbox = box

                else:
                    prev_bbox = box


                x, y, w, h = prev_bbox

                # Obtener el centro del fotograma
                frame_center_x = frame.shape[1] // 2
                frame_center_y = frame.shape[0] // 2

                # Obtener el centro del objeto detectado
                object_center_x = x + w // 2
                object_center_y = y + h // 2

                # Calcular la diferencia entre el centro del objeto y el centro del fotograma
                diff_x = frame_center_x - object_center_x
                diff_y = frame_center_y - object_center_y

                # Determinar si la cámara necesita moverse para centrar el objeto
                if object_center_x < frame_center_x - 10:
                    print("Mover la cámara hacia la derecha")
                elif object_center_x > frame_center_x + 10:
                    print("Mover la cámara hacia la izquierda")
                

                if object_center_y < frame_center_y - 100:
                    print("Mover la cámara hacia abajo")
                elif object_center_y > frame_center_y + 100:
                    print("Mover la cámara hacia arriba")


                # Dibujar la caja delimitadora y etiqueta de clase
                cv2.rectangle(frame, prev_bbox, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, 'Object detected', (prev_bbox[0]+10, prev_bbox[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (prev_bbox[0] + prev_bbox[2] // 2, prev_bbox[1] + prev_bbox[3] // 2), 5, (0, 255, 0), -1)

    cv2.imshow(winName, frame)
    
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:
        break
     
cv2.destroyAllWindows()