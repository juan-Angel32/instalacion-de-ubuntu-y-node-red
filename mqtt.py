import network
from machine import Pin, ADC
from umqtt.simple import MQTTClient
import time

# Configura las credenciales de tu red WiFi
SSID = "ostion"
PASSWORD = "123456uu"

# Configura el servidor MQTT y el tópico
MQTT_SERVER = "192.168.26.219"
MQTT_TOPIC = "luminosidad"

# Configuración del pin de la fotorresistencia
fotorresistor_pin = 34
adc = ADC(Pin(fotorresistor_pin))
adc.width(ADC.WIDTH_10BIT)  # Resolución de 10 bits (0-1023)

# Función para conectar a la red WiFi
def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    try:
        if not sta_if.isconnected():
            print("Conectando a WiFi...")
            sta_if.active(True)
            sta_if.connect(SSID, PASSWORD)
            while not sta_if.isconnected():
                pass
        print("Conectado a WiFi")
        print("Dirección IP:", sta_if.ifconfig()[0])
    except OSError as e:
        print("Error al conectar a WiFi:", e)

# Función para conectar al servidor MQTT
def connect_mqtt():
    global client
    client = MQTTClient("esp32", MQTT_SERVER)
    try:
        client.connect()
        print("Conectado al servidor MQTT")
    except OSError as e:
        print("Error al conectar al servidor MQTT:", e)

# Función principal
def main():
    try:
        connect_wifi()
        connect_mqtt()
        
        while True:
            # Lectura de la fotorresistencia
            luminosidad = adc.read()
            print("Valor de luminosidad:", luminosidad)
            
            # Envío del valor a Node-RED a través de MQTT
            try:
                client.publish(MQTT_TOPIC, str(luminosidad))
                print("Mensaje MQTT enviado")
            except OSError as e:
                print("Error al publicar en MQTT:", e)
            
            time.sleep(1)  # Intervalo de envío (1 segundo)
    
    except KeyboardInterrupt:
        print("\nPrograma detenido manualmente")

if __name__ == "__main__":
    main()
