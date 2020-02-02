#!/usr/bin/python
import paho.mqtt.client as paho
import sys
import Adafruit_DHT

hostname='Iteration'

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


broker="sufi.io"
topic="test_topic"
port=1883
client1 = paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print("Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4")
    sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
temperature = temperature * 9/5.0 + 32

if humidity is not None and temperature is not None:
    data = 'Sensor={0} Temp={1:0.1f}*  Humidity={2:0.1f}%'.format(hostname, temperature, humidity)
    ret= client1.publish(topic,data)
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)