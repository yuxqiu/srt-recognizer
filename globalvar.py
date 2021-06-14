from cnocr import CnOcr

#Global Variable
coor_y_top,coor_y_bottom, coor_x_left, coor_x_right = -1, -1, -1, -1 # Initialize coordinate value of selected area
left, right = False, False #
rectangleSelect = False # Indicate whether to use rectangle select
isSingleLine = True # Single line ocr or Multi-line
isSrt = False # whether or not export as srt
ocrResults = [] # Store the final result
totalRead = 0 # Store total frame read before starting ocr
sentenceBefore = "" # Store the sentence read before
ocr = CnOcr(model_name = 'densenet-lite-gru', root = 'cnocr') # Initialize ocr module
timeBefore = "" # Store the time
