from PyQt6.QtCore import QThread,pyqtSignal
from eggdetector import Eggdector
import numpy
class Dectation(QThread):
    signal_frame_drawed=pyqtSignal(
        numpy.ndarray,int
    )
    
    def __init__(self):
        super().__init__()
        self.eggdetector=Eggdector("yolo/weights.pt")
        self.frame=None
        print("membuat dectection")
    def start(self):
        super().start()
        self.running=True
        print("Start")
    def setFrame(self,frame):
        self.frame=frame
    def run(self):
        while self.running:
            if self.frame is not None:
                drawed_frame,egg_count=self.eggdetector.draw(self.frame)
                self.signal_frame_drawed.emit(drawed_frame,egg_count)
        print("run ")
    def stop(self):
        self.running=False
        print("stop") 