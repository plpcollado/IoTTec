import paho.mqtt.client as mqtt
import time

#MQTT Broker setup
broker_address = "192.168.1.128" # or the IP address of the broker
broker_port = 1883
sensor_topic = "rover/sensor"
command_topic = "rover/command"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sensor_topic)

def on_message(client, userdata, message):
    sensor_data = str(message.payload.decode("utf-8"))
    print(f"Sensor data received: {sensor_data}")

    # Example decision logic
    try:
        distance = float(sensor_data)
        if distance < 15:
            client.publish(command_topic, "stop")
        else:
            client.publish(command_topic, "forward")
    except ValueError:
        print("Invalid sensor data received")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, broker_port, 60)
    client.loop_start()

    try:
        while True:
            time.sleep(1) # Keep the script running
    except KeyboardInterrupt:
        print("Program stopped")
        client.loop_stop()

if __name__ == "__main__":
    main()