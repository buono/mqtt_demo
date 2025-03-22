import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# ------------------------------
# GPIOの設定
# ------------------------------
LED_PIN = 18  # 使用するGPIOピン番号（必要に応じて変更）
GPIO.setmode(GPIO.BCM)        # BCM番号でピンを指定する
GPIO.setup(LED_PIN, GPIO.OUT) # LED_PINを出力モードに設定

# ------------------------------
# MQTTブローカー情報
# ------------------------------
# HiveMQのパブリックブローカーではなく、ローカルのMosquittoを利用
broker = "localhost"  # Mosquittoが同一Raspberry Pi上で動いている場合は"localhost"
port = 1883
topic = "home/led"

# ------------------------------
# コールバック関数
# ------------------------------
def on_connect(client, userdata, flags, rc):
    """
    MQTTブローカーに接続した際に呼び出されるコールバック関数。
    接続結果を表示し、指定したトピックをサブスクライブする。
    """
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    """
    サブスクライブしているトピックにメッセージが届いた際に呼び出されるコールバック関数。
    メッセージが"ON"ならLEDを点灯、"OFF"ならLEDを消灯する。
    """
    message = msg.payload.decode()  # バイナリデータを文字列に変換
    print(f"Received message: {message} on topic: {msg.topic}")
    if message == "ON":
        GPIO.output(LED_PIN, GPIO.HIGH)  # LEDを点灯
        print("LED ON")
    elif message == "OFF":
        GPIO.output(LED_PIN, GPIO.LOW)   # LEDを消灯
        print("LED OFF")

# ------------------------------
# MQTTクライアントの設定と接続開始
# ------------------------------
client = mqtt.Client("RaspberryPiClient")  # 任意のクライアントID
client.on_connect = on_connect
client.on_message = on_message

# ローカルのMosquittoブローカーに接続
client.connect(broker, port, 60)
client.loop_forever()
