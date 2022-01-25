import pytesseract
import numpy as np
from cv2 import cv2
import csv
import re

input_path="D:/project-tommy/test-8.mp4"
output_path="D:/project-tommy/output-8.csv"
sampling_freq=10


titles = ['Bus1-generator(MW)', 'Bus1-generator(MVR)', 'Bus1-load(MW)', 'Line Flow ( 1 to 2)', 'Line Flow (1 to 3)', 
 'Bus2-generator(MW)', 'Bus2-generator(MVR)', 'Bus2-load(MW)', 'Line Flow ( 2 to 1)', 'Line Flow (2 to 3)',
 'Bus3-generator(MW)', 'Bus3-generator(MVR)', 'Bus3-load(MW)', 'Line Flow ( 3 to 2)', 'Line Flow (3 to 1)',
 'Current Time']



def process_video(path):
    cap=cv2.VideoCapture(path)
    counter = 0
    filename = output_path
    with open(filename, 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(titles)   
    while True:
        ret,frame = cap.read()
        if not ret:
            print("Reached the end of the stream. Exiting ...")
            break
        
        if(counter%sampling_freq == 0):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            custom_oem_psm_config = r'--oem 3 --psm 12'
            data = pytesseract.image_to_string(gray, config=custom_oem_psm_config)
            arr = data.split('\n')
            arr2 = sanitize_array(arr)
            print(len(arr2))
            print(arr2)
            if(len(arr2) == 31):
                indices = [13, 14, 18, 2, 17, 8, 11, 4, 0, 9, 20, 21, 26, 15, 28, 30]
                selected_elements = []
                for index in indices:
                    selected_elements.append(arr2[index])
                with open(filename, 'a', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(selected_elements) 
        counter+=1
    cap.release()
    
def sanitize_array(arr):
    arr2 = []
    for var in arr:
        var = var.upper()
        if(len(var) > 1) and ( var.endswith('MW') or var.endswith('AM') or var.endswith('MVR') or var.endswith('AGC') or var.endswith('ON') or var.endswith('PU')):
            if(not var.endswith('06:00 AM') and not var.endswith('10:00 AM')):
                if(var.endswith('MW')):
                    if(var.endswith('4IMW') or var.endswith('I4MW')):
                        var = var[:-4]
                        var = re.sub(r'[A-Z]+', "", var, re.I)
                        arr2.append(var)
                    elif(var.endswith(' MW') or var.endswith('4MW') or var.endswith('IMW')):
                        var = var[:-3]
                        var = re.sub(r'[A-Z]+', "", var, re.I)
                        arr2.append(var)
                elif(var.endswith('MVR')):
                    if(var.endswith('4IMVR') or var.endswith('I4MVR')):
                        var = var[:-5]
                        var = re.sub(r'[A-Z]+', "", var, re.I)
                        arr2.append(var)
                    elif(var.endswith(' MVR') or var.endswith('4MVR') or var.endswith('IMVR')):
                        var = var[:-4]
                        var = re.sub(r'[A-Z]+', "", var, re.I)
                        arr2.append(var)
                else:
                    arr2.append(var)

    return arr2


if __name__ == "__main__":
    process_video(input_path)


# 1919 * 876