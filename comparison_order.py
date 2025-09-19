import csv
import os
import shutil
import numpy as np
import cv2 as cv
from glob import glob

#map aangeven waar de inventarisnummers staan
mappen = glob("D:/image_similarity/*/", recursive = True)

#map aangeven waar de mogelijk dubbele scans naar verplaatst worden
outputdir = "D:/possible_double_scan/"

#csv aanmaken voor de resultaten
header = ['base_img', 'test_img', 'invr_nr', 'value']
with open(outputdir + 'image_compare_results.csv', 'a') as file:
    dw = csv.DictWriter(file, delimiter=',', fieldnames=header)
    dw.writeheader()

#map maken als die niet bestaat
try:
    os.makedirs(outputdir)
    print(f"Nested directories '{outputdir}' created successfully.")
except FileExistsError:
    print(f"One or more directories in '{outputdir}' already exist.")
except PermissionError:
    print(f"Permission denied: Unable to create '{outputdir}'.")
except Exception as e:
    print(f"An error occurred: {e}")

def compare_function():
    hsv_base = cv.cvtColor(src_base, cv.COLOR_BGR2HSV)
    hsv_test1 = cv.cvtColor(src_test1, cv.COLOR_BGR2HSV)

    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]

    # hue varies from 0 to 179, saturation from 0 to 255
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges  # concat lists

    # Use the 0-th and 1-st channels
    channels = [0, 1]

    hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    for compare_method in range(1):
        # base_base = cv.compareHist(hist_base, hist_base, compare_method)
        base_test1 = cv.compareHist(hist_base, hist_test1, compare_method)
        print('comparing', img_base, ' with ', img_test1, ' the value is: ', base_test1)

        # create CSV file and assign header for each value
        with open(outputdir + 'image_compare_results.csv', 'a') as file:
            file.write(f"{img_base}, {img_test1}, {map}, {base_test1}\n")

        if base_test1 > 0.999:
            shutil.copy(img_base, outputdir)
            shutil.copy(img_test1, outputdir)
            #print('The following images might be the same: ', img_base, ' and ', img_test1)

for map in mappen:
    filelist = os.listdir(map)
    full_paths = [os.path.join(map, file) for file in os.listdir(map)]
    full_paths.sort()
    print(f"\nProcessing folder: {map}")
    for i in tqdm.tqdm(range(len(full_paths) - 1), delay=2, colour='green', mininterval=1):
        img_base = full_paths[i]
        src_base = cv.imread(full_paths[i])
        img_test1 = full_paths[i + 1]
        src_test1 = cv.imread(full_paths[i + 1])
        #print(f"Comparing {img_base} to {img_test1}")
        if src_base is None or src_test1 is None:
            print("Cannot open or find the images!")
            exit(0)
        else:
            compare_function()
    print(f"Folder {map} is done.")





