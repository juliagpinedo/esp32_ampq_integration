#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 5

MD_Parola Display = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

String message;

void setup() {
    Serial.begin(115200);  
    Display.begin();
    Display.setIntensity(0);
    Display.displayClear();
}

void loop() {
    if (Serial.available() > 0) {
        message = Serial.readStringUntil('\n');  // Guarda el mensaje
        Serial.println("Mensaje para display: " + message);  
        Display.displayClear();
        Display.displayScroll(message.c_str(), PA_RIGHT, PA_SCROLL_LEFT, 150);
    }
    
    if (Display.displayAnimate()) {  
        Display.displayReset();
    }
}
