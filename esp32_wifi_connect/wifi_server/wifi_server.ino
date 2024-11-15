#include <WiFi.h>
int LED_blink = 2;

// Mobile Hotspot name and password
const char* ssid = "Nga Thinh"; // replace with your hotspot SSID
const char* password = "teongabinh"; // replace with your hotspot password

WiFiServer server(80);

#define ENA_PIN_1 5
#define IN1_PIN_1 7
#define IN2_PIN_1 8

#define ENA_PIN_2 16
#define IN1_PIN_2 17
#define IN2_PIN_2 18

void setup() {
  pinMode(ENA_PIN_1, OUTPUT);
  pinMode(IN1_PIN_1, OUTPUT);
  pinMode(IN2_PIN_1, OUTPUT);

  pinMode(ENA_PIN_2, OUTPUT);
  pinMode(IN1_PIN_2, OUTPUT);
  pinMode(IN2_PIN_2, OUTPUT);

  Serial.begin(115200);
  pinMode(LED_blink, OUTPUT);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop()
{
    if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi lost. Reconnecting...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nReconnected to WiFi.");
    
    server.begin(); // Restart the server after reconnecting
    Serial.println("Server restarted.");
  }

  WiFiClient client = server.available();   // Check if a client has connected
  if (!client) return;                      // Continue if no client is connected
  
  Serial.println("New client connected.");
  
  // Wait until the client sends some data
  while(!client.available()){
    delay(1);
  }
  
  // Read the request from the client
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Find and parse "left" and "right" parameters from the request
  int leftIndex = request.indexOf("left=");
  int rightIndex = request.indexOf("right=");
  
  int leftValue = 0;  // Default values if parameters are not found
  int rightValue = 0;

  if (leftIndex != -1) {
    leftValue = request.substring(leftIndex + 5).toInt();  // Convert the left param value to an integer
    Serial.print("Left parameter received: ");
    Serial.println(leftValue);
  }

  if (rightIndex != -1) {
    rightValue = request.substring(rightIndex + 6).toInt();  // Convert the right param value to an integer
    Serial.print("Right parameter received: ");
    Serial.println(rightValue);
  }

  // Control motor 1 with the "left" parameter
  digitalWrite(IN1_PIN_1, LOW);
  digitalWrite(IN2_PIN_1, HIGH);
  analogWrite(ENA_PIN_1, leftValue);

  // Control motor 2 with the "right" parameter
  digitalWrite(IN1_PIN_2, LOW);
  digitalWrite(IN2_PIN_2, HIGH);
  analogWrite(ENA_PIN_2, rightValue);

  client.stop(); 
  delay(10); 
}
