#include <WiFi.h>
int LED_blink = 2;
// Replace with your network credentials
const char* ssid = "Nga Thinh";
const char* password = "teongabinh";

// Define a static IP, Gateway, and Subnet
IPAddress local_IP(192, 168, 1, 184);     // Set your desired IP
IPAddress gateway(192, 168, 1, 1);        // Set your router's gateway
IPAddress subnet(255, 255, 255, 0);       // Set your subnet mask
WiFiServer server(80);
void setup() {
  Serial.begin(115200);
  pinMode(LED_blink, OUTPUT);
  // Set a static IP address
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  // Connect to Wi-Fi network with SSID and password
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

  // Handle the request to control the LED
  if (request.indexOf("/LED=ON") != -1) {
    digitalWrite(LED_blink, HIGH); // Turn LED on
    Serial.println("LED turned ON");
  }
  if (request.indexOf("/LED=OFF") != -1) {
    digitalWrite(LED_blink, LOW);  // Turn LED off
    Serial.println("LED turned OFF");
  }

  // HTML content to send to the client
  String htmlPage = R"rawliteral(
    <!DOCTYPE html>
    <html>
    <head>
      <title>ESP32 LED Control</title>
      <style>
        body { font-family: Arial; text-align: center; }
        button { font-size: 1.2em; padding: 10px 20px; margin: 20px; }
      </style>
    </head>
    <body>
      <h1>ESP32 LED Control</h1>
      <button onclick="toggleLED('ON')">Turn LED On</button>
      <button onclick="toggleLED('OFF')">Turn LED Off</button>

      <script>
        function toggleLED(state) {
          fetch('/LED=' + state);
        }
      </script>
    </body>
    </html>
  )rawliteral";

  // Send the response to the client
  client.print("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n");
  client.print(htmlPage);
  
  delay(1);
  client.stop(); // Close the connection
  Serial.println("Client disconnected.");
}
