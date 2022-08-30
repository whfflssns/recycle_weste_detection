import torch
import cv2
import time

camera = cv2.VideoCapture(0)
model = torch.hub.load('D:/pythonProj/waste_data_processing/yolov5/', 'custom', path='D:/pythonProj/waste_data_processing/best.pt',source='local')

def return_color(a):
    ## 파,초,빨
    if a['class'] == 0:
        color = (255,0,0)
    elif a['class'] == 1:
        color = (0,255,0)
    elif a['class'] == 2:
        color = (0,0,255)
    elif a['class'] == 3:
        color = (0,255,255)
    elif a['class'] == 4:
        color = (255,0,255)
    return color

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
# With webcam get(CV_CAP_PROP_FPS) does not work.
# Let's see for ourselves.
if int(major_ver) < 3:
    fps = camera.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else:
    fps = camera.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
# Number of frames to capture
num_frames = 120;
print("Capturing {0} frames".format(num_frames))
# Start time
start = time.time()
for i in range(0, num_frames) :
    ret, frame = camera.read()
end = time.time()
seconds = end - start
print("Time taken : {0} seconds".format(seconds))
fps = num_frames / seconds
print("Estimated frames per second : {0}".format(fps))

while cv2.waitKey(33) < 0:
    success, frame = camera.read()  # read the camera frame
    if not success:
        break
    else:
        result = model(frame)
        a = result.pandas().xyxy[0]
        if a.size == 0:
            continue
        else:
            for i in range(int(a.size / 7)):
                if float(a.loc[i]['confidence']) >= 0.5:
                    c1 = (int(a.loc[i]['xmin']), int(a.loc[i]['ymin']))
                    c2 = (int(a.loc[i]['xmax']), int(a.loc[i]['ymax']))
                    name = a.loc[i]['name']
                    color = return_color(a.loc[i])
                    frame = cv2.rectangle(frame, (c1), (c2), color, 3)
                    cv2.putText(frame, name, (c1[0], c1[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                else:
                    continue

        cv2.imshow("webcam", frame)

camera.release()
cv2.destoryAllWindows()