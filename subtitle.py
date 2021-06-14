import cv2
import export
from globalvar import *
from difflib import SequenceMatcher

# Define a class to store recognized text and time range of the text
class ocrResult:
   def __init__(self, string, time):
      self.string = string
      self.time = time 

# This function uses cv2 to save image for ocr module
def save_image(image,addr):
  address = addr + '.jpg'
  cv2.imwrite(address,image)

# This fucntion binarizes selected area
def binarize(frame):
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   #ret, gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   if(coor_x_left == -1):
     gray = gray[coor_y_top:coor_y_bottom, 0:width]
   else:
     gray = gray[coor_y_top:coor_y_bottom, coor_x_left:coor_x_right]

   return gray

# This function is tied with select function to get mouse action. It sets coordinate values of selected area.
def OnMouseAction(event,x,y,flags,param):
  global coor_y_top, coor_y_bottom, coor_x_left, coor_x_right, left, right
  
  if event == cv2.EVENT_LBUTTONDOWN:
      print("左键点击")
      print("%s" %x,y)
      coor_y_top = y * 2
      if(rectangleSelect):
        coor_x_left = x * 2
      left = True
  elif event==cv2.EVENT_RBUTTONDOWN :
      print("右键点击")
      print("%s" %x,y)
      coor_y_bottom = y * 2
      if (rectangleSelect):
        coor_x_right = x * 2
      right = True

# This function creates a new window to ask user to select the area that subtitle appears
def select(camera):
  global totalRead, rectangleSelect, left, right
  
  print("使用说明：\n如果不使用矩形选择请使用左键点击字幕的最上方，右键点击字幕的最下方。可以尽可能选择大一些，这样可以保证字幕不丢失。\n如果使用矩形选择，根据估计左键点击最长的字幕的左上方，右键点击最长的字幕的右下方。\n")
  rectangleSelect = True if int(input("是否需要开启矩形选择，是输入1，不是输入0. 开启矩形选择可以提升识别准确性，但如果没有选择准确会丢失字幕\n")) == 1 else False
  print("\n请在弹出框内选择字幕区域！选择完成后按空格退出。如果弹出窗口内没有字幕，可以按空格键跳转到下一帧！\n")

  while(not left or not right):
    totalRead += 1
    success, img = camera.read()
    cv2.namedWindow('Image')
    resize_img = cv2.resize(img,(0,0),fx = 0.5,fy = 0.5)
    cv2.setMouseCallback('Image',OnMouseAction)
    while(1):
        cv2.imshow('Image',resize_img)
        k=cv2.waitKey(1)
        if k==ord(' '):  
            break

  grayFirstFrame = binarize(img)
  save_image(grayFirstFrame, "image")
  ocrImage("image.jpg")
  
  cv2.destroyAllWindows()

# This function returns time in the format of hh:mm:ss,ms
def returnTime(seconds):
    ms = float(format(seconds % 1, '.3f')) * 1000
    minute = seconds / 60
    hour = minute / 60
    minute %= 60
    seconds %= 60

    return ("%02d:%02d:%02d,%03d" % (hour, minute, seconds, ms))

'''
This function returns the similarity value between two string.
Similarity value is greater than 0, lesser than 1.
If two strings are similar, it is closer to 1.
'''
def similarity(a, b):
  return SequenceMatcher(None, a, b).ratio()

# This function uses cnocr library to extract texts from selected area
def ocrImage(imagePath):
  global sentenceBefore, isSingleLine
  sentence = ""

  if(isSingleLine):
    res = ocr.ocr_for_single_line(imagePath)
    for i in range(len(res)):
      sentence += res[i]
  else:
    res = ocr.ocr(imagePath)
    for i in range(len(res)):
      for k in range(len(res[i])):
        sentence += res[i][k]

  similarValue = similarity(sentence, sentenceBefore)

  if(similarValue < 0.5):
    tmp = sentenceBefore
    sentenceBefore = sentence
    return tmp

  return 

'''
This function call binarize and ocr function to extract texts from selected area.
Then it appends the recognized texts and time into a list.
'''
def extract(frame, i):
    global fps, timeBefore
    
    gray = binarize(frame)
    save_image(gray,'image')
    
    print('save image:',i)
    tmp = ocrImage("image.jpg")

    if(tmp != None):
        tmpOcrResult = ocrResult(tmp, "")
        if(isSrt):
           seconds = (totalRead + i - 1) / fps
           time = returnTime(seconds)
           newseconds = (totalRead + i) / fps
           newTime = returnTime(newseconds)
           tmpOcrResult.time = timeBefore + " --> " + time
           timeBefore = newTime

        ocrResults.append(tmpOcrResult)

    print("完成度:", (totalRead + i) / FrameNumber * 100, "%")

# Initialize globar variale
isSingleLine = False if int(input("是否需要识别多行的字幕，是输入1，不是输入0. 如果需要识别多行的字幕会减慢识别速度。\n")) == 1 else True
isSrt = True if int(input("是否需要导出为srt，是输入1，不是输入0. 如果需要识别多行的字幕会减慢识别速度。\n")) == 1 else False
filename = input("请输入文件地址: 文件名+后缀名\n")
print("\n")

# Open video
camera = cv2.VideoCapture(filename)
# Check whether the video is opened
if (camera.isOpened()):
   fps = camera.get(cv2.CAP_PROP_FPS)# Get fps
   FrameNumber = camera.get(7)  # Get total frames

   width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) # Get width
   height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Get height

   select(camera)

   #Initialize timeBefore
   seconds = totalRead / fps
   initialTime = returnTime(seconds)
   timeBefore = initialTime

   # Starting to extract texts from selected area
   success, frame = camera.read()
   i = 0
   while success:
    i = i + 1

    if(isSrt):
        extract(frame, i)
    elif (i % int(fps // 2) == 1):
        extract(frame, i)
    success, frame = camera.read()

   seconds = (totalRead + i) / fps
   time = returnTime(seconds)
   finalResult = ocrResult(sentenceBefore, timeBefore + " --> " + time)
   ocrResults.append(finalResult)

   if(isSrt):
      export.exportAsSrt(ocrResults)
   else:
      export.exportAsString(ocrResults)
   
else:
    print('视频打开失败!')