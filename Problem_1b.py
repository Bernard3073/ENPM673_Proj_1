#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 11:05:53 2021

@author: bernard
"""

import numpy as np 
import cv2 




def find_tag(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    squares = []
    # ===========================================================================
    # Check the dimension of the square
    # for c in contours:
    #     x,y,w,h = cv2.boundingRect(c)
    #     cv2.putText(frame, str(w*h), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 1)
    # =============================================================================
    
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.1*cnt_len, True) 
        squares.append(cnt)
        
    return squares



def is_cell_white(cell):
    threshold = 200
    cell_to_gray = cv2.cvtColor((cell), cv2.COLOR_BGR2GRAY) if len(cell.shape) > 2 else cell
    return 1 if (np.mean(cell_to_gray) >= threshold) else 0

def get_ar_tag_id(tag_image):
    _, binary = cv2.threshold(tag_image, 200, 255, cv2.THRESH_BINARY_INV)
    
    tag_corners_map = {}
    tag_corners_map["TL"] = tag_image[20:30, 20:30] 
    tag_corners_map["TR"] = tag_image[20:30, 50:60] 
    tag_corners_map["BR"] = tag_image[50:60, 50:60] 
    tag_corners_map["BL"] = tag_image[50:60, 20:30] 
    
    inner_corners_map = {}
    inner_corners_map["TL"] = tag_image[30:40, 30:40]
    inner_corners_map["TR"] = tag_image[30:40, 40:50] 
    inner_corners_map["BR"] = tag_image[40:50, 40:50] 
    inner_corners_map["BL"] = tag_image[40:50, 30:40] 
    
    white_cell_corner = ''
    for cell_key in tag_corners_map:
        if is_cell_white(tag_corners_map[cell_key]):
            white_cell_corner = cell_key
            break
    if white_cell_corner == '':
        return None
    
    re_orient_action_map = {'TR': [3, 0, 1, 2], 'TL': [2, 3, 0, 1], 'BL': [1, 2, 3, 0], 'BR': [0, 1, 2, 3]}
    print('White Cell Corner: ', white_cell_corner)
    id_number = [(is_cell_white(inner_corners_map[cell_key])) for cell_key in inner_corners_map]
    print('id_number', id_number)   
    tag_id = 0
    for index, swap_ind in enumerate(re_orient_action_map[white_cell_corner]):
        tag_id = tag_id + id_number[swap_ind] * np.power(2, (index))
        
    return tag_id


def main():
    frame = cv2.imread('./ref_marker.png')   
    dim = 80
    frame = cv2.resize(frame, (dim, dim), interpolation = cv2.INTER_AREA)
    
    
    contour = find_tag(frame) 
    
    cv2.drawContours(frame, contour, -1, (0,255,0), thickness = 2)
    tag_id = get_ar_tag_id(frame)
    print(tag_id)

    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()