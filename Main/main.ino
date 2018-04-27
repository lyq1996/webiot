
#include <aJSON.h>
const int LED = 4;//LED正极连接针脚4
const int EFAN = 5;
const int LIGHT = 6;
String inputString = "";
boolean stringComplete = false;
char* parseJson(char *jsonString);
void setup() {
  pinMode(LED, OUTPUT);
  pinMode(LIGHT, OUTPUT);
  pinMode(EFAN, OUTPUT);
  Serial.begin(115200);
  delay(5000);
}
void loop() {
  serialEvent();
    if (stringComplete) {
      inputString.trim();
        int len = inputString.length()+1;    
        if(inputString.startsWith("{") && inputString.endsWith("}")){
          char jsonString[len];
          inputString.toCharArray(jsonString,len);
          aJsonObject *msg = aJson.parse(jsonString);
          processMessage(msg);
          aJson.deleteItem(msg);
          }      
      // clear the string:
      inputString = "";
      stringComplete = false;   
  }
}

void processMessage(aJsonObject *msg){
  aJsonObject* object = aJson.getObjectItem(msg, "object");
  aJsonObject* contral = aJson.getObjectItem(msg, "control");
  //char* st = aJson.print(msg);
  if (!object) {
    return;
  }
    //Serial.println(st); 
    //free(st);
    String O=object->valuestring;
    String C=contral->valuestring;
    if(O=="led"){
      if(C=="open"){
        digitalWrite(LED, HIGH);
        sayToServer("LED on!");    
      }
      if(C=="close"){
        digitalWrite(LED, LOW);
        sayToServer("LED off!");    
      }
    }
    if(O=="efan"){
      if(C=="open"){
        digitalWrite(EFAN, HIGH);
        sayToServer("efan on!");    
      }
      if(C=="close"){
        digitalWrite(EFAN, LOW);
        sayToServer("efan off!");    
      }
    }
    if(O=="light"){
      if(C=="open"){
        digitalWrite(LIGHT, HIGH);
        sayToServer("light on!");    
      }
      if(C=="close"){
        digitalWrite(LIGHT, LOW);
        sayToServer("light off!");    
      }
    }
}
void sayToServer(String content){
  Serial.print("{\"M\":\"say\",\"C\":\"");
  Serial.print(content);
  Serial.print("\"}\r");
}
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
