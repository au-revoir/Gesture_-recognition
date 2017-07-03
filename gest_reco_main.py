import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, bg = cap.read()

resdict = {0: 'Black', 1:'R', 2:'G', 3:'RG', 4:'B', 5:'BR', 6:'BG', 7:'RGB', 8:'', 9:'', 10:'', 11:'', 12:'', 13:'', 14:'', 15:'', 16:'',17:'', 18:'', 19:'', 20:'', 21:'', 22:'', 23:'', 24:'', 25:'', 26:'', 27:'', 28:''}

file = open("dictionary.txt","r")
for i in range(0,13):
	resdict[i] = file.readline()
file.close()	
RED_MIN = np.array([0, 0, 50], np.uint8)
RED_MAX = np.array([40, 36, 255], np.uint8)

GREEN_MIN = np.array([0, 50, 0], np.uint8)
GREEN_MAX = np.array([40, 255, 36], np.uint8)

BLUE_MIN = np.array([50, 0, 0], np.uint8)
BLUE_MAX = np.array([255, 40, 36], np.uint8)

YELLOW_MIN = np.array([0, 50, 50], np.uint8)
YELLOW_MAX = np.array([30, 255, 255], np.uint8)

min_area = 200

red = 1
green = 2
blue = 4
yellow = 8
violet = 16

def bgselect():
	global bg
	global root
	#root.hide()
	root.iconify()
	#temp = Toplevel()
	while(cap.isOpened()):
		ret, bg = cap.read()
		bg = cv2.flip(bg, 1)
		cv2.imshow("Background",bg)
		k = cv2.waitKey(10)
		if k == ord('s'):
			break
	cv2.destroyAllWindows()
	for i in range (1,5):
		cv2.waitKey(1)
	#root.show()
	#temp.destroy()
	#root.update()
	root.deiconify()

def colorcode():	
	max_area = 0
	img = image
	global res
	res = 0
	frame_threshed = cv2.inRange(img, RED_MIN, RED_MAX)
	contours,hierarchy = cv2.findContours(frame_threshed, 1, 2)
	if contours:
		for i in contours:
			area = cv2.contourArea(i)
			if area > max_area:
				max_area = area
				cnt = i

			if max_area > min_area:
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(imageview,(x,y),(x+w,y+h),(0,0,255),2)
				res = res | red
		
	max_area = 0
	img = image
	frame_threshed = cv2.inRange(img, GREEN_MIN, GREEN_MAX)
	contours,hierarchy = cv2.findContours(frame_threshed, 1, 2)
	if contours:
		for i in contours:
			area = cv2.contourArea(i)
			if area > max_area:
				max_area = area
				cnt = i
			if max_area > min_area:
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(imageview,(x,y),(x+w,y+h),(0,255,0),2)
				res = res | green
	max_area = 0
	img = image
	frame_threshed = cv2.inRange(img, BLUE_MIN, BLUE_MAX)
	contours,hierarchy = cv2.findContours(frame_threshed, 1, 2)
	if contours:
		for i in contours:
			area = cv2.contourArea(i)
			if area > max_area:
				max_area = area
				cnt = i
			if max_area > min_area:
				x,y,w,h = cv2.boundingRect(cnt)
				cv2.rectangle(imageview,(x,y),(x+w,y+h),(255,0,0),2)
				res = res | blue

def action():
	global bg
	global root
	root.hide()
	while(cap.isOpened()):
		max_area = 0
		cnt = 0	
		global res
		res = 0
		ret, img = cap.read()
		img = cv2.flip(img, 1)
		global imageview
		imageview = img
		img = cv2.subtract(img, bg)
		global image 
		image = img
		colorcode()
		cv2.imshow("Feed",imageview)
		T.insert(END,resdict[res])
		T.insert(END," ")
		T.update_idletasks()
		T.delete('1.0', END)
		#T.configure(scrollregion = T.bbox("all"))
		k = cv2.waitKey(10)
		if k == ord("q") or k == 27:
			cv2.destroyAllWindows()
			for l in range (1,5):
				cv2.waitKey(1)
			break
	root.show()

def insert():
	file = open("dictionary.txt","w")
	global root
	#root.hide()
	root.iconify()
	while(cap.isOpened()):
		max_area = 0
		cnt = 0	
		global res
		res = 0
		ret, img = cap.read()
		img = cv2.flip(img, 1)
		global imageview
		imageview = img
		img = cv2.subtract(img, bg)
		global image 
		image = img
		colorcode()
		cv2.imshow("Feed",imageview)
		k = cv2.waitKey(10)
		if k == ord("s"):
			resdict[res] = raw_input("> ")
			resdict[res] = resdict[res] + '\n'
		elif k == ord("q") or k == 27:
			break
	cv2.destroyAllWindows()
	for i in range (1,5):
		cv2.waitKey(1)
	for i in resdict:
		file.write(resdict[i])
	file.close()
	root.deiconify()

def text_enter():
    global e
    string = e.get() 
    print string  

def __init__(self,master):
    master.minsize(width = 100, height = 100)
    master.maxsize(width = 100, height = 100)

from Tkinter import *
root = Tk()
root.geometry("800x400")
root.configure(background = 'blue')
root.title("Gesture Recognition")

topFrame = Frame(root)
topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side = BOTTOM)

#root.window = window

button2 = Button(master = bottomFrame, text = "BG Select", command = bgselect)

button2.pack(side = LEFT,fill = X)

button1 = Button(master = bottomFrame, text = "Start", command = action) 

button1.pack(side = LEFT,fill = X)

button2 = Button(master = bottomFrame, text = "Insert", command = insert)

button2.pack(side = LEFT,fill = X)

button2 = Button(master = bottomFrame, text = "Exit", command = root.quit)

button2.pack(side = LEFT,fill = X)

#step= root.attributes('-fullscreen', True)
#step.grid(row=0, columnspan=7, sticky='W',padx=100, pady=5, ipadx=130, ipady=25)
S = Scrollbar(root)
T = Text(root, height = 5, width = 30)
S.pack(side = RIGHT, fill = Y)
T.pack(side = LEFT, fill = Y)
S.config(command = T.yview)
T.config(yscrollcommand = S.set)



#T.insert(END, resdict[res])
root.mainloop()


#parentWindow.maxsize(500,500);
#parentWindow.minsize(500,500);

