import network

import dht
from machine import Pin, ADC, PWM

import urequests as requests
import time
import utime
import json

frequency = 5000

oldTemperature = 10
oldHumidity = 50
oldSoilSensor_value_per = -1
oldM_Sensor_Value = 0
Temperature = 10
dTime = 0
pTime = 0

pPin = Pin(2,Pin.OUT)
pPin.off()
pPushbtn = Pin(12, Pin.IN, Pin.PULL_UP)
led = PWM(Pin(14), frequency)
pFan = Pin(27, Pin.OUT)
pPump = Pin(26, Pin.OUT)
SoilSensor = ADC(Pin(34)) #Define a pin for Soil Sensor
M_Sensor = Pin(25, Pin.IN, Pin.PULL_DOWN) #define pin 25 for PIR input
SoilSensor.atten(ADC.ATTN_11DB)       #Full range: 3.3v

led.duty(0) #set initial value to 0
pPump.off() #set intial pump state off
pFan.off() #set intial fan state off

# Replace these values with your Firebase project credentials
FIREBASE_URL = "https://iot-greenhouse-fb219-default-rtdb.firebaseio.com"
FIREBASE_KEY = "AIzaSyCRYmX_VwVX7j3_b2V9nAayLuEaa7NzCbI"

firebase_node = "Data"

p15 = Pin(15, Pin.IN) #define pin 15 as a INPUT
dht_Data = dht.DHT11(p15)


sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('JD', 'pgpw6050')
    while not sta_if.isconnected():
        pass
print('network config:', sta_if.ifconfig())
pPin.on()

def handle_interrupt(pin):
    global dTime
    if (not pPump.value()) and ((utime.ticks_ms() - pTime) < 1000):
        currentTime = utime.ticks_ms()
        diff = currentTime - dTime
        dTime = currentTime
        if diff > 5000: 
            print("Push button pressed")
            led.duty(0) #set value to 0
            pPump.off() #set pump state off
            pFan.off() #set fan state off
            data_to_send = {"Fan":0, "Pump status": 0, "Slider_val":0}
            send_to_firebase(data_to_send) # Call the function to send data to Firebase
    

    
pPushbtn.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

def map(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value

def send_to_firebase(data):
    try:
        # Create the Firebase Realtime Database endpoint URL
        endpoint_url = "{}/{firebase_node}.json?auth={firebase_key}".format(FIREBASE_URL, firebase_node=firebase_node, firebase_key=FIREBASE_KEY)

        # Convert data to JSON format
        json_data = json.dumps(data)

        # Make a PUT request to update the data in Firebase
        response = requests.patch(endpoint_url, data=json_data)

        # Print the response from Firebase (optional)
        print("Firebase response:", response.text)

        # Close the response to free up resources
        response.close()

    except Exception as e:
        print("Error:", e)

def read_data():
    try:
        endpoint_url = "{}/{firebase_node}.json?auth={firebase_key}".format(FIREBASE_URL, firebase_node=firebase_node, firebase_key=FIREBASE_KEY)
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Close the response to free up resources
            response.close()
                
                
            return data
        else:
            print("Error: Unable to fetch data from Firebase. Status Code:", response.status_code)
            return None


    except Exception as e:
        print("Error:", e)
        return None
# data send to Firebase
data_to_send = {"Temperature":Temperature, "Humidity": 50.0}

while True: 
    
    send_to_firebase(data_to_send) # Call the function to send data to Firebase
    data = read_data()
    
    Fan_Status = data.get("Fan")
    Pump_Status = data.get("Pump status")
    Mode = data.get("Operating Mode")
    Slider_val = data.get("Slider_val")
    Soil_Moisture_High = data.get("Soil_Moisture_High")
    Soil_Moisture_Low = data.get("Soil_Moisture_Low")
    
    SoilSensor_value = SoilSensor.read()
    SoilSensor_value_per = int(map(SoilSensor_value, 3800, 1850, 0, 100))
    
    if SoilSensor_value_per > 100:
        SoilSensor_value_per = 100
    elif SoilSensor_value_per < 0:
        SoilSensor_value_per = 0
        
    print("Fan status",Fan_Status)
    print("Pump_Status",Pump_Status)
    print("Slider_val",Slider_val)
    print("Soil_Moisture_High",Soil_Moisture_High)
    print("Soil_Moisture_Low",Soil_Moisture_Low)
    
    if Fan_Status:
        pFan.on()
    else:
        pFan.off()
    
    if Pump_Status:
        pPump.on()
    else:
        pPump.off()
        pTime = utime.ticks_ms()
    if Slider_val:
        led.duty(int(Slider_val/100*1023))
    if Slider_val ==0:
        led.duty(0)
    
    if SoilSensor_value_per < Soil_Moisture_Low:
        Soil_moisture_status = "LOW"
    elif SoilSensor_value_per > Soil_Moisture_High:
        Soil_moisture_status = "HIGH"
    else:
        Soil_moisture_status = "MEDIUM"

    try:
        M_Sensor_Value = M_Sensor.value()
        dht_Data.measure()
        Temperature = dht_Data.temperature()
        Humidity = dht_Data.humidity()
        
        print()
        print("SoilSensor_value ",SoilSensor_value)
        print("SoilSensor_value_per ",SoilSensor_value_per)
        print("Soil_Moisture ",Soil_moisture_status)
        print("Temperature",Temperature)
        print("Humidity",Humidity)
        print("Motion",M_Sensor_Value)
        print()
        
#         print()
#         print("oldSoil_Moisture ",oldSoilSensor_value)
#         print("oldTemperature",oldTemperature)
#         print("oldHumidity",oldHumidity)
#         print("oldMotion",oldM_Sensor_Value)
#         print()
        
        if((oldTemperature != Temperature) or (oldHumidity != Humidity) or (oldSoilSensor_value_per != SoilSensor_value_per) or (oldM_Sensor_Value != M_Sensor_Value)):
            print("sending data")
            data_to_send = {"Temperature":Temperature, "Humidity": Humidity, "Soil_Moisture":SoilSensor_value_per, "Motion":M_Sensor_Value}
        oldTemperature = Temperature
        oldHumidity = Humidity
        oldSoilSensor_value_per = SoilSensor_value_per
        oldM_Sensor_Value = M_Sensor_Value
        
        
    except Exception as e:
        print("DHT reading failed")
        pass
    
    # Wait for a moment before sending the next data
    time.sleep(0.1)