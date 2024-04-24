#include "WifiCam.hpp"
#include <WiFi.h>
#include <WebServer.h>

static const char* WIFI_SSID = "**";
static const char* WIFI_PASS = "**";

esp32cam::Resolution initialResolution;

WebServer server(80);

void setup() {

  Serial.begin(115200);
  delay(2000);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
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

void
loop()
{
  server.handleClient();
}


void recibeInstrucciones() {
  server.on("/instrucciones", HTTP_POST, []() {
    String json = server.arg("plain");
    Serial.print("Instrucciones recibidas: ");
    Serial.println(json);
    
    server.send(200, "text/plain", "Instrucciones recibidas correctamente");
  });
}