from ultralytics import YOLO
import cv2
class Eggdector:
    def __init__(self,model_path):        
        self.model_path=model_path
        self.model=YOLO(model_path)
        self.count=0

    def proses(self,frame):
        detections=[]
        results=self.model( frame, verbose=False)
        names=self.model.names
        for i in results:
            for box in i.boxes:
                x1,y1,x2,y2=box.xyxy.cpu().numpy()[0]
                conf=box.conf.cpu().numpy()[0] 
                cls=box.cls.cpu().numpy()[0]
                cls_name=names[int(cls)]
                if conf < 0.5:
                    continue
                detections.append({
                    "box":[x1,y1,x2,y2],
                    "conf":conf,
                    "class":cls_name
                })
                self.count+=1

        return detections
    def draw(self,frame):
        draw_frame=frame.copy()
        detections=self.proses(frame)
        comment="count:"+ str(len(detections))
        cv2.putText(draw_frame,comment,(0,50    ),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        
        for det in detections:
            if(det["conf"] > 0.5):
                x1,y1,x2,y2=map(int,det["box"])
                cv2.rectangle(
                    draw_frame,
                    (x1,y1),
                    (x2,y2),
                    (0,255,0)
                )
                cv2.putText(
                    draw_frame,
                    f"{det['class']} {det['conf']:.2f}",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (36,255,12),
                    2,
                )
        return draw_frame,len(detections)