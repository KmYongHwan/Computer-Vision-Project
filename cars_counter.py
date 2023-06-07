# importing libraries
import cv2
import numpy as np

# capturing or reading video
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('cars.mp4')

# adjusting frame rate
fps = cap.set(cv2.CAP_PROP_FPS,10)

# minimum contour width
min_contour_width=50  #40

# minimum contour height
min_contour_height=50  #40

offset=10   #10
line_height1= 100 #300  #550
line_height2= 530
matches1 =[]
matches2 =[]
cars1=0
cars2=0

# defining a function
def get_centroid(x, y, w, h):

    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx,cy
    return [cx, cy]


cap.set(3,1920)
cap.set(4,1080)

if cap.isOpened():
    ret,frame1 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame2 = cap.read()

while ret:
    d = cv2.absdiff(frame1,frame2)
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey,(5,5),0)

    ret , th = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(th,np.ones((3,3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

    # Fill any small holes
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    #객체의 외곽선 검출
    contours,h = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (
                h >= min_contour_height)

        if not contour_valid:
            continue

        cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)

        cv2.line(frame1, (450, line_height1), (900, line_height1), (0,255,0), 2)
        cv2.line(frame1, (100, line_height2), (1300, line_height2), (0,0,255), 2)

        centroid1 = get_centroid(x, y, w, h)
        matches1.append(centroid1)
        matches2.append(centroid1)
        cv2.circle(frame1,centroid1, 5, (0,255,0), -1)

        cx,cy= get_centroid(x, y, w, h)
        for (x,y) in matches1:
            if (line_height1) > y > (line_height1 - offset) and 450 < x < 900: # 400, 750
                cars1=cars1+1
                matches1.remove((x,y))
                print(x,y)

        for (x,y) in matches2:
            if (line_height2 + 5) > y > (line_height2 - offset) and 100 < x < 1300: # 100, 920
                cars2=cars2+1
                matches2.remove((x,y))
                #print(cars2)

    cv2.putText(frame1, "Total Vehicles Detected: " + str(cars2 - cars1 - 1), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 170, 0), 2) # cars1 - cars2 + 4

    #cv2.drawContours(frame1,contours,-1,(0,0,255),2)


    cv2.imshow("OUTPUT" , frame1)
    #cv2.imshow("Difference" , th)
    if cv2.waitKey(2) == ord('q'):
        break
    frame1 = frame2
    ret , frame2 = cap.read()

#print(matches)
cv2.destroyAllWindows()
cap.release()