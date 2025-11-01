from PyQt6.QtNetwork import QNetworkAccessManager,QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QUrl,QObject, pyqtSignal
import json
class Apiclient(QObject):
    signal_finished=pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.manager=QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_finished)
    def on_finished(self,reply: QNetworkReply):
        err=reply.error()
        print(err)
        if err == QNetworkReply.NetworkError.NoError:
            data=reply.readAll().data()
            print("Data recevied")
            self.signal_finished.emit(data)
        else:print("Error:",reply.errorString())
    def post(self,url,data):
        request_url=QNetworkRequest(QUrl(url))
        request_url.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,"application/json")
        data_json=json.dumps(data).encode("utf-8")
        self.manager.post(request_url,data_json)
    def get(self,url):
        request_url=QNetworkRequest(QUrl(url))
        self.manager.get(request_url)
        print("get data from",url)