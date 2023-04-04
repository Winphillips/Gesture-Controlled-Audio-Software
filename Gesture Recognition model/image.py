import cv2
import os
import sys

cam = cv2.VideoCapture(0)

start = False
counter = 0
num_samples = int(sys.argv[1])
IMG_SAVE_PATH = 'images'

try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    if counter == num_samples:
       break

    cv2.rectangle(frame, (10, 30), (310, 330), (0, 255, 0), 2)

    k = cv2.waitKey(1)
    if k == ord('c'):
            name = 'gesture1'
            IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, name)
            os.mkdir(IMG_CLASS_PATH)
                        
    if k == ord('n'):
            name = 'nothing'
            IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, name)
            os.mkdir(IMG_CLASS_PATH)
            
    if start:
        roi = frame[25:335, 8:315]
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(counter + 1))
        print(save_path)
        cv2.imwrite(save_path, roi)
        counter += 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,"Collecting {}".format(counter),
            (10, 20), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)


    if k == ord('s'):
        start = not start

    if k == ord('q'):
            break

print("\n{} image(s) saved to {}".format(counter, IMG_CLASS_PATH))
cam.release()
cv2.destroyAllWindows()
