import requests

# Dirección IP de tu ESP32
ESP32_IP = ''  # Reemplaza con la IP de tu ESP32

# URL a la que enviar la solicitud
url = f'http://{ESP32_IP}/instrucciones'

# Instrucciones a enviar
instrucciones = {
    'comando': 'rotar_servo',
    'parametros': {
        'angulo': 90
    }
}

# Enviar solicitud POST con las instrucciones
response = requests.post(url, json=instrucciones)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    print("Instrucciones enviadas correctamente")
else:
    print("Error al enviar instrucciones:", response.status_code)
