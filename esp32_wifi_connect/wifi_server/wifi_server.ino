#include <WiFi.h>
int LED_blink = 2;
// Wifi name and password
const char* ssid = "Nga Thinh";
const char* password = "teongabinh";

// Define a static IP, Gateway, and Subnet
IPAddress local_IP(192, 168, 1, 184);     // Set static IP each time esp connect to wifi
IPAddress gateway(192, 168, 1, 1);        // Router's gateway
IPAddress subnet(255, 255, 255, 0);       // Subnet mask
WiFiServer server(80);

#define ENA_PIN 5
#define IN1_PIN 0
#define IN2_PIN 9

void setup() {
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  Serial.begin(115200);
  pinMode(LED_blink, OUTPUT);
  // Set a static IP address
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }
  // Connect to Wi-Fi network with name and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop()
{
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

  // Find the "param=" part in the request and extract the number following it
  int paramIndex = request.indexOf("param=");
  if (paramIndex != -1) {
    int paramValue = request.substring(paramIndex + 6).toInt();  // Convert the param value to an integer
    Serial.print("Parameter received: ");
    Serial.println(paramValue);
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
    analogWrite(ENA_PIN, paramValue);
  }
  
  client.stop(); 
}
