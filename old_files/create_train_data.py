import cv2

def thresh_img(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    r, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return img

camera = cv2.VideoCapture(0)
top, right, bottom, left = 150, 600, 400, 350
frames_count = 1000

frame_id = 0

while frame_id < frames_count:
    ret, frame = camera.read()

    frame = frame[top:bottom, left:right]
    cv2.flip(frame, 1, frame)
    
    thresh = thresh_img(frame)
    # cv2.imshow("frame", frame)
    cv2.imshow("th", thresh)

    cv2.imwrite("imgs/none/img{}.jpg".format(frame_id), thresh)
    frame_id += 1

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()