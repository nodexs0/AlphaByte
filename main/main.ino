#include "WifiCam.hpp"
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

static const char* WIFI_SSID = "**";
static const char* WIFI_PASS = "**";

static const IPAddress STATIC_IP(192, 168, 137, 72);
static const IPAddress GATEWAY(192, 168, 1, 1);
static const IPAddress SUBNET(255, 255, 255, 0);

int pin = 4;

esp32cam::Resolution initialResolution;

WebServer server(80);

void setup() {
  
  pinMode(pin, OUTPUT);

  Serial.begin(115200);
  delay(2000);

  WiFi.persistent(false);

   // Configura la dirección IP estática
  WiFi.mode(WIFI_STA);
  WiFi.config(STATIC_IP, GATEWAY, SUBNET);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Falló la conexión a WiFi");
    delay(5000);
    ESP.restart();
  }

  Serial.println("Wifi conectado");

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("Inicialización de la cámara fallida");
      delay(5000);
      ESP.restart();
    }
    Serial.println("Cámara inicializada");
  }

  Serial.println("Servidor iniciado");
  Serial.print("http://");
  Serial.println(WiFi.localIP());
  addRequestHandlers();
  recibeInstrucciones();
  server.begin();
}

void loop() {
  server.handleClient();
}

void recibeInstrucciones() {
  server.on("/instrucciones", HTTP_POST, []() {
    String json = server.arg("plain");
    Serial.print("Instrucciones recibidas: ");
    Serial.println(json);

    // Crear un objeto DynamicJsonDocument para almacenar el JSON recibido
    DynamicJsonDocument doc(1024); // Tamaño máximo del JSON recibido

    // Deserializar el JSON
    DeserializationError error = deserializeJson(doc, json);

    // Verificar si hubo un error en la deserialización
    if (error) {
      Serial.print("Error al analizar JSON: ");
      Serial.println(error.c_str());
      server.send(400, "text/plain", "Error al analizar JSON");
      return;
    }

    if (doc.containsKey("Luz")) {
      String comando = doc["Luz"].as<String>();
      if (comando == "encender") {
        digitalWrite(pin, HIGH);
      } else if (comando == "apagar") {
        digitalWrite(pin, LOW);
      }
    } else {
      Serial.println("Comando no reconocido");
    }
    
    server.send(200, "text/plain", "Instrucciones recibidas correctamente");
  });
}
