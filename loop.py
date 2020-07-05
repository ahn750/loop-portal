import cv2
import numpy as np
import time

def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colors = hsv[y,x]
        print("BRG Format: ",colors)
 
  
cv2.namedWindow('frame')
cv2.namedWindow('mask')
cv2.setMouseCallback('frame',mouseRGB)
cv2.setMouseCallback('mask',mouseRGB)
        

paths=['sample/first_frame.jpg','sample/titan_battle.mp4','sample/space.mp4']
img=cv2.imread('sample/loop.jpg')

cap=cv2.VideoCapture(0)
first_frame=cv2.imread(paths[0])
#cv2.imwrite('sample/first_frame.jpg',first_frame)

capVid=cv2.VideoCapture(paths[1])
frame2=first_frame.copy()



startTime=0
count=0
switch=0

while True:

	idx=count%3
	print(idx)
	if(switch==1):
		if(idx==0):
			frame2=first_frame.copy()
			
		else:
			path=paths[idx]
			capVid=cv2.VideoCapture(path)

	switch=0
			
		
	if idx!=0: frame2=capVid.read()[1]
		

	frame2=cv2.resize(frame2,(640,480))
	frame=cap.read()[1]

	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	S=[100,255]
	V=[100,255]
	

	lower_green = np.array([30, 130,80],dtype='uint8')
	upper_green = np.array([40,255,255],dtype='uint8')

	#mask for green belt
	mask=cv2.inRange(hsv,lower_green,upper_green)

	kernel=np.ones((12,12),np.uint8)
	mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	
	#mask of inner loop but along with backgnd(needs to be removed)
	inner=np.invert(mask)
	outer=inner.copy()

	#obtaining contour for outer loop and filling outer loop with black
	contours=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
	cv2.drawContours(outer, contours, -1,0, -1)
	#cv2.drawContours(frame, contours, -1,(0,0,255), 2)

	cv2.imshow('outer',outer)
	cv2.waitKey(0)
	outer=np.invert(outer)
	inner=cv2.bitwise_and(inner,outer)
	bgMask=np.invert(inner)

	bg=cv2.bitwise_and(frame,frame,mask=bgMask)

	roi=cv2.bitwise_and(frame2,frame2,mask=inner)

	final=cv2.bitwise_or(bg,roi)

	contours=cv2.findContours(inner,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]


	#For switching video if loop opened for more than 2s
	if (len(contours))==0 and startTime==0: startTime=time.time()

	if(len(contours)==1):
		if(startTime!=0): 
			elapsed=time.time()-startTime
			
			if(elapsed>2):
				
					print('switch')
					switch=1
					count+=1
					
				
					
			startTime=0

	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)
	cv2.imshow('inner',inner)
	cv2.imshow('final',final)
	if cv2.waitKey(1)==ord('q'):
		break
		
		
					




	
