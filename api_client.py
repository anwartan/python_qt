from PyQt6.QtNetwork import QNetworkAccessManager,QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QUrl,QObject
import json
class Apiclient(QObject):
    def __init__(self):
        super().__init__()
        self.manager=QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_finished)
    def on_finished(self,reply: QNetworkReply):
        err=reply.error()
        if err == QNetworkReply.NetworkError.NoError:
            data=reply.readAll().data()
            print("Data recevied")
        else:print("Error:",reply.errorString())
    def post(self,url,data):
        request_url=QNetworkRequest(QUrl(url))
        request_url.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader,"application/json")
        data_json=json.dumps(data).encode("utf-8")
        self.manager.post(request_url,data_json)