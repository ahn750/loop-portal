import cv2
import numpy as np
import time


#for getting hsv color values of pixels by clicking to fix color range
def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colors = hsv[y,x]
        print("BRG Format: ",colors)
  
cv2.namedWindow('frame')
cv2.namedWindow('mask')
cv2.setMouseCallback('frame',mouseRGB)
cv2.setMouseCallback('mask',mouseRGB)
        
 
#paths to video files
paths=['sample/first_frame.jpg','sample/titan_battle.mp4','sample/space.mp4']

# live camera feed
cap=cv2.VideoCapture(0)

#backgnd that will be used for invisibility illusion
first_frame=cv2.imread(paths[0])
#cv2.imwrite('sample/first_frame.jpg',first_frame)

#default video path and frame from video
capVid=cv2.VideoCapture(paths[1])
frame2=first_frame.copy()

num_videos=len(paths)

startTime=0
count=0
switch=0

while True:

	#identifying which video to play
	idx=count%num_videos
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

	#expanding roi boundaries
	kernel=np.ones((12,12),np.uint8)
	mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	
	#mask of inner loop but along with backgnd(needs to be removed)*
	inner=np.invert(mask)
	
	
	#generating the outer loop mask
	outer=np.zeros((frame.shape[0],frame.shape[1]),dtype=np.uint8)
	contours=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
	cv2.drawContours(outer, contours, -1,255, -1)

	'''
	AND betwn the obtained outer and the inner (marked *) to remove the bckgnd.
	finally obtain inner loop and rest of the bckgnd seperately
	'''
	inner=cv2.bitwise_and(inner,outer)
	bgMask=np.invert(inner)

	#getting the bckgnd from live camera feed
	bg=cv2.bitwise_and(frame,frame,mask=bgMask)

	#patch from video
	roi=cv2.bitwise_and(frame2,frame2,mask=inner)

	#combining the roi from video with feed bckgnd
	final=cv2.bitwise_or(bg,roi)

	#finding contour to check if loop is opened or closed
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
		
		
					




	
