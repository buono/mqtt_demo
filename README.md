# mqtt_demo

## 事前準備

ラズパイ上にmosquittoをインストール
```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

別デバイスからの通信を許可する（デフォルトではオフ）
```
vim /etc/mosquitto/mosquitto.conf
```

下記を末尾に追加
```
listener 1883
allow_anonymous true
```

その後再起動して設定を反映
```
sudo systemctl restart mosquitto
```

pythonでmqttを扱うためのライブラリをインストール
```
pip install paho-mqtt
```