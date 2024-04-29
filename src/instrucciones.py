import requests

# Dirección IP de tu ESP32
ESP32_IP = ''

# URL a la que enviar la solicitud
url = f'http://{ESP32_IP}/instrucciones'

def enviar_instrucciones(instrucciones):
    # Enviar solicitud POST con las instrucciones
    response = requests.post(url, json=instrucciones)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        print("Instrucciones enviadas correctamente")
    else:
        print("Error al enviar instrucciones:", response.status_code)

def crear_instrucciones(luz):
    instrucciones = {
        'Luz': luz,
    }
    return instrucciones

while True:
    entrada = int(input(""))
    if entrada == 1:
        instrucciones = crear_instrucciones("encender")
        enviar_instrucciones(instrucciones)
    elif entrada == 2:
        instrucciones = crear_instrucciones("apagar")
        enviar_instrucciones(instrucciones)
    else:
        break
