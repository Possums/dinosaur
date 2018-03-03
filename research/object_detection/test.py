import time
import cv2
import mss
import numpy


with mss.mss() as sct:

    box = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
    
    while 'Screen capturing':
        t = time.time()
        img = numpy.array(sct.grab(box))

              # Display the picture
        cv2.imshow('test', img)
             # Display the picture in grayscale
             # cv2.imshow('test', cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
        print('fps: {0}'.format(1 / (time.time()-t)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
