import cv2
import sched, time
import torch
cam = cv2.VideoCapture(0)

def printa(a):
    print(a)

# s = sched.scheduler()
#
# s.enter()
n = 0
while True:
    if n == 0:
        start = time.time()
        n += 1
    check, frame = cam.read()

    cv2.imshow('video', frame)
    a = time.time() - start
    if a >= 0.5:
        printa(a)
        start = time.time()

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()