import cv2
import numpy as np

hsv,frame= None,None
ix,iy = -1,-1

def nothing(x):
    pass

cap = cv2.VideoCapture(1)
cv2.namedWindow('img',cv2.WINDOW_NORMAL)
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global hsv, frame
        H, S, V = hsv[y, x]
        print(f"\rH:{H}, S:{S}, V:{V}\tX:{x},Y:{y}", end='', flush=True)

        global ix,iy
        ix, iy = x, y
cv2.setMouseCallback('frame', draw_circle)

cv2.createTrackbar('H_min', 'img', 0, 179, nothing)
cv2.createTrackbar('S_min', 'img', 0, 255, nothing)
cv2.createTrackbar('V_min', 'img', 0, 255, nothing)
cv2.createTrackbar('H_max', 'img', 0, 179, nothing)
cv2.createTrackbar('S_max', 'img', 0, 255, nothing)
cv2.createTrackbar('V_max', 'img', 0, 255, nothing)

try:
    while True:
        ret,frame = cap.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos('H_min', 'img')
        s_min = cv2.getTrackbarPos('S_min', 'img')
        v_min = cv2.getTrackbarPos('V_min', 'img')
        h_max = cv2.getTrackbarPos('H_max', 'img')
        s_max = cv2.getTrackbarPos('S_max', 'img')
        v_max = cv2.getTrackbarPos('V_max', 'img')

        lower = np.array([h_min,s_min,v_min])
        upper = np.array([h_max,s_max,v_max])

        mask = cv2.inRange(hsv,lower,upper)
        res = cv2.bitwise_and(frame,frame,mask=mask)

        if ix != -1 and iy != -1:
            cv2.circle(frame, (ix, iy), 5, (0, 0, 255), 2)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)

        if cv2.waitKey(1) == ord('q'):
            break

        try:
             value = cv2.getWindowProperty('img', cv2.WND_PROP_VISIBLE)
             if value == 0:
                 print("value is 0")
                 break
        except cv2.error :
             print("cv2 error")
             break



finally:
    cap.release()
    cv2.destroyAllWindows()