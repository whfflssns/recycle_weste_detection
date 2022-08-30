from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import torch
import time

app = Flask(__name__)

current_label = ""
final_result = ""
split = "AAAA"

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


def made_dataset(name, confi):
    global current_label
    current_label += name
    current_label += ","
    current_label += confi
    current_label += split

def gen_frames(camera):
    n = 0
    model = torch.hub.load('D:/pythonProj/waste_data_processing/yolov5/', 'custom', path='D:/pythonProj/waste_data_processing/best.pt', source='local')
    while True:
        if n == 0:
            start = time.time()
            n += 1
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            to_time = time.time() - start
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
                        confi = str(a.loc[i]['confidence'])
                        color = return_color(a.loc[i])
                        frame = cv2.rectangle(frame, (c1), (c2), color, 3)
                        cv2.putText(frame, name, (c1[0], c1[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                        if to_time >= 0.5:
                            made_dataset(name, confi)
                    else:
                        continue
            if to_time >= 0.5:
                start = time.time()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    # count = 0
    # model = torch.hub.load('D:/pythonProj/waste_data_processing/yolov5/', 'custom', path='D:/pythonProj/waste_data_processing/best.pt', source='local')
    # while True:
    #     # Capture frame-by-frame
    #     success, frame = camera.read()  # read the camera frame
    #     if not success:
    #         break
    #     else:
    #         count += 1
    #         result = model(frame)
    #         a = result.pandas().xyxy[0]
    #         if a.size == 0:
    #             continue
    #         else:
    #             for i in range(int(a.size / 7)):
    #                 if float(a.loc[i]['confidence']) >= 0.5:
    #                     c1 = (int(a.loc[i]['xmin']), int(a.loc[i]['ymin']))
    #                     c2 = (int(a.loc[i]['xmax']), int(a.loc[i]['ymax']))
    #                     name = a.loc[i]['name']
    #                     confi = str(a.loc[i]['confidence'])
    #                     color = return_color(a.loc[i])
    #                     frame = cv2.rectangle(frame, (c1), (c2), color, 3)
    #                     cv2.putText(frame, name, (c1[0], c1[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
    #                     global current_label
    #                     global current_confi
    #                     if count == 6:
    #                         current_label += name
    #                         current_label += "."
    #                         current_label += confi
    #                         current_label += split
    #                 else:
    #                     continue
    #             if count == 6:
    #                 count = 0
    #         ret, buffer = cv2.imencode('.jpg', frame)
    #         frame = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return redirect(url_for('start_webcam'))
    else:
        return render_template('index.html')

@app.route('/start_webcam')
def start_webcam():
    return render_template('start_webcam.html')

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    camera = cv2.VideoCapture(0)
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/getlabel')
def getLabel():
    global current_label
    global final_result
    final_result = current_label
    current_label = "" # 초기화
    return final_result

if __name__ == '__main__':
    app.run(debug=True)