from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi
from api_client import Apiclient
import json

class Weather(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("cuaca/awan.ui", self)
        self.api_client = Apiclient()
        self.cek_button.clicked.connect(self.on_cek_button)
        self.api_client.signal_finished.connect(self.on_data_received)

    def on_data_received(self, data):
        data = json.loads(data)
        hasil = "waktu saat ini: "+str(data["currentTime"])
        hasil += "kondisi: "+str(data["weatherCondition"]["description"]["text"])+"()"+"feels like: "+str(data["feelsLikeTemperature"]["degrees"])+str(data["feelsLikeTemperature"]["unit"])+"\n"
        hasil += "suhu: "+str(data["temperature"]["degrees"])+str(data["temperature"]["unit"])+"\n"
        hasil += "kelembapan:"+str(data["relativeHumidity"])+"\n"
        hasil += "angin: "+str(data["wind"]["direction"]["degrees"])+str(data["wind"]["direction"]["cardinal"])+str(data["wind"]["speed"]["value"])+str(data["wind"]["speed"]["unit"])+"\n"
        hasil += "jarak pandang: "+str(data["visibility"]["distance"])+str(data["visibility"]["unit"])+"\n"
        hasil += "tingkat awan: "+str(data["cloudCover"])+"\n"
        hasil += "tekanan udara: "+str(data["airPressure"]["meanSeaLevelMillibars"])+"\n"
        hasil += "peluang udara: "+str(data["precipitation"]["probability"]["percent"])+"\n"
        hasil += "peluang hujan badai: "+str(data["thunderstormProbability"])+"%"+"\n"
        hasil += "suhu maksimum hari ini: "+str(data["currentConditionsHistory"]["maxTemperature"]["degrees"])+str(data["currentConditionsHistory"]["maxTemperature"]["unit"])+"\n"
        hasil += "suhu minimum hari ini: "+str(data["currentConditionsHistory"]["minTemperature"]["degrees"])+str(data["currentConditionsHistory"]["minTemperature"]["unit"])+"\n"
        hasil += "perubahan suhu terakhir: "+str(data["currentConditionsHistory"]["temperatureChange"]["degrees"])+str(data["currentConditionsHistory"]["temperatureChange"]["unit"])+"\n"
        self.deskripsi_label.setText(hasil)
    def on_cek_button(self):
        LATITUDE = self.latitude_sb.value()
        LONGITUDE = self.longtitude_sb.value()
        API_KEY = "AIzaSyDpmaYZeO7WOFWkcIeC3Ej-Y5dDa1FDxZs"
        API_URL = f"https://weather.googleapis.com/v1/currentConditions:lookup?location.latitude={LATITUDE}&location.longitude={LONGITUDE}&key={API_KEY}"
        self.api_client.get(API_URL)
        print("button clicked")

    def latitude(self):
        return self.latitude_sb.value()

    def longitude(self):
        return self.longtitude_sb.value()
   
