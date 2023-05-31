# boot.py -- run on boot-up
import network, utime, machine
import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
import random
import config 

SSID = config.WIFI_SSID
SSID_PASSWORD = config.WIFI_PASSWD
HOST = config.HOST_ADR
HOST_PORT = config.HOST_PORT
CLIENT_ID = "ESP-8266"
TOPIC = b"temperature"
USER = 'esp'
PASSWORD = 'password'

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())

    
def connect_to_mqtt():
   with open("ca.crt", "r") as f: 
    cert = f.read()
    print("Got Cert")
    
    mqttClient = MQTTClient(CLIENT_ID, HOST, HOST_PORT, USER, PASSWORD, keepalive = 60, ssl=True, ssl_params={"cert":cert, "server_side":False})
     
    mqttClient.connect()
    print(f"Connected to MQTT  Broker :: {HOST}")
    
    for x in range(2):
        random_temp = 25
        print(f"Publishing temperature :: {random_temp}")
        mqttClient.publish(TOPIC, str(random_temp).encode())
        time.sleep(3)
    mqttClient.disconnect()
    
    
def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
    
print("Connecting to your wifi...")    
connect_to_wifi()

print ("Connecting to MQTT")
connect_to_mqtt()