#include <XBee.h>

// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

#include "DHT.h"
#include "XBee.h"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>

#define DHTPIN 2     // what pin we're connected to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);
// NOTE: For working with a faster chip, like an Arduino Due or Teensy, you
// might need to increase the threshold for cycle counts considered a 1 or 0.
// You can do this by passing a 3rd parameter for this threshold.  It's a bit
// of fiddling to find the right value, but in general the faster the CPU the
// higher the value.  The default for a 16mhz AVR is a value of 6.  For an
// Arduino Due that runs at 84mhz a value of 30 works.
// Example to initialize DHT sensor for Arduino Due:
//DHT dht(DHTPIN, DHTTYPE, 30);

//create the XBee object
XBee xbee = XBee();

Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

//payload we are sending; two floats of four bytes each
//but with the BMP180 we are sending two more floats (pressure and altitude)
//so 16 byte array
uint8_t payload[16] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

// union to convert float to byte string
union u_tag {
    uint8_t arrayString[4];
    float fval;
} u;
 
 
// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40BF060D);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));
ZBTxStatusResponse txStatus = ZBTxStatusResponse();
 
int statusLed = 7;
int errorLed = 8;
 
void flashLed(int pin, int times, int wait) {
 
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(wait);
    digitalWrite(pin, LOW);
 
    if (i + 1 < times) {
      delay(wait);
    }
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("DHTxx test!");
  
  xbee.setSerial(Serial);
  
  pinMode(statusLed, OUTPUT);
  pinMode(errorLed, OUTPUT);
  
  Serial.println("Pressure Sensor Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!bmp.begin())
  {
    /* There was a problem detecting the BMP085 ... check your connections */
    Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  dht.begin();
  
}

void loop() {
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

 
  // check if returns are valid, if they are NaN (not a number) then something went wrong!
  if (!isnan(t) && !isnan(h)) {
     
    // convert humidity into a byte array and copy it into the payload array
    u.fval = h;
    for (int i=0;i<4;i++){
      payload[i]=u.arrayString[i];
    }
     
    // same for the temperature
    u.fval = t;
    for (int i=0;i<4;i++){
      payload[i+4]=u.arrayString[i];
    }
    
    //Serial.println(payload[0]);
    
    ///////////////////////////////////BEGIN BMP180//////////////////////////////
  
  /* Get a new sensor event */ 
  sensors_event_t event;
  bmp.getEvent(&event);
 
  /* Display the results (barometric pressure is measure in hPa) */
  if (event.pressure)
  {
    /* Display atmospheric pressue in hPa */
    Serial.print("Pressure:    ");
    float pressure = event.pressure;
    Serial.print(pressure);
    Serial.println(" hPa");
    
    /* Calculating altitude with reasonable accuracy requires pressure    *
     * sea level pressure for your position at the moment the data is     *
     * converted, as well as the ambient temperature in degress           *
     * celcius.  If you don't have these values, a 'generic' value of     *
     * 1013.25 hPa can be used (defined as SENSORS_PRESSURE_SEALEVELHPA   *
     * in sensors.h), but this isn't ideal and will give variable         *
     * results from one day to the next.                                  *
     *                                                                    *
     * You can usually find the current SLP value by looking at weather   *
     * websites or from environmental information centers near any major  *
     * airport.                                                           *
     *                                                                    *
     * For example, for Paris, France you can check the current mean      *
     * pressure and sea level at: http://bit.ly/16Au8ol                   */
     
    /* First we get the current temperature from the BMP085 */
    float temperature;
    bmp.getTemperature(&temperature);
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" C");

    /* Then convert the atmospheric pressure, SLP and temp to altitude    */
    /* Update this next line with the current SLP for better results      */
    float seaLevelPressure = 1023;    //SENSORS_PRESSURE_SEALEVELHPA;
    Serial.print("Altitude:    "); 
    
    float altitude = bmp.pressureToAltitude(seaLevelPressure, event.pressure, temperature);
    
    Serial.print(altitude); 
    Serial.println(" m");
    Serial.println("");
    
    // convert pressure into a byte array and copy it into the payload array
    u.fval = pressure;
    for (int i=0;i<4;i++){
      payload[i]=u.arrayString[i];
      //Serial.print("HERE in pressure");
    }
     
    // same for the altitude
    u.fval = altitude;
    for (int i=0;i<4;i++){
      payload[i+4]=u.arrayString[i];
      //Serial.print("HERE in altitude");
    }
    
  }
  else
  {
    Serial.println("Sensor error");
  }
  
  ///////////////////////////////////END BMP180//////////////////////////////
     
    xbee.send(zbTx);
 
    // flash TX indicator
    flashLed(statusLed, 1, 100);
 
    // after sending a tx request, we expect a status response
    // wait up to half second for the status response
    if (xbee.readPacket(500)) {
      // got a response!
 
      // should be a znet tx status             
      if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
        xbee.getResponse().getZBTxStatusResponse(txStatus);
 
        // get the delivery status, the fifth byte
        if (txStatus.getDeliveryStatus() == SUCCESS) {
          // success.  time to celebrate
          flashLed(statusLed, 5, 50);
        } else {
          // the remote XBee did not receive our packet. is it powered on?
          flashLed(errorLed, 3, 500);
        }
      }
    } else if (xbee.getResponse().isError()) {
        Serial.print("Error reading packet.  Error code: ");  
        Serial.println(xbee.getResponse().getErrorCode());
    } else {
      // local XBee did not provide a timely TX Status Response -- should not happen
      flashLed(errorLed, 2, 50);
    }
  }
  
    
  
  // Compute heat index
  // Must send in temp in Fahrenheit!
  float hi = dht.computeHeatIndex(f, h);

  Serial.print("Humidity: "); 
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: "); 
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.print(" *F\t");
  Serial.print("Heat index: ");
  Serial.print(hi);
  Serial.println(" *F");
  
  delay(1000);
}
