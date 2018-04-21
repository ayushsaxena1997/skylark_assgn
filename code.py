#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 11:59:23 2018

@author: ayush
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 04:39:16 2018

@author: ayush
"""

import cv2
import numpy as np
import csv
 
#Function to generate rotated versions of our GCP template
def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

img_op_list=[] #List to contain points found in a particular image
final_list=[] #The final list that contains all images and all points 
delta=100 #The minimum distance assumed between two GCPs

angle = 30 #Amount (in deg) by which our template GCP is rotated everytime. 
k=360/angle #Number of such angular variations of template GCP
rot_ang = [j*angle for j in range(int(k))]

#Our original template:
template_orig = cv2.imread('/home/ayush/Downloads/template.jpg',0)

for angle in rot_ang:
    rotated_img = rotateImage(template_orig, angle)
    pts=np.where(rotated_img<20)
    rotated_img[pts[0], pts[1]] = 40 #Filling up dark space generated due to rotation
    cv2.imwrite('rotated_%d.png'%(angle), rotated_img) #Saving rotated templates for visualization
    

#Names of the files for testing:
names= ['DSC01713.JPG', 'DSC01798.JPG', 'DSC01836.JPG', 'DSC01886.JPG', 'DSC01916.JPG', 'DSC02013.JPG', 'DSC02209.JPG', 'DSC02252.JPG', 'DSC02407.JPG', 'DSC02426.JPG']

for name in names:
    check=0 #Check counts the number of GCPs found in an image
    img_rgb = cv2.imread('/home/ayush/Downloads/for_assignment/%s'%(name))
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    main_list=[] #List containing points found at a particular anglular orientation of template
    print('Evaluation on image %s'%(name))
    
    for angle in rot_ang:
        template = cv2.imread('rotated_%d.png'%(angle), 0)
        w, h = template.shape[::-1]
    
        res = cv2.matchTemplate(img_gray,template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8 #Best suited acc to experiments
        loc = np.where( res >= threshold)
        if (len(loc[0]) == 0 & len(loc[1]) == 0): 
            print('No point found for %d rotation'%(angle))
    
        else:
            pt_list=[]
            
            check=1
            for pt in zip(*loc[::-1]):     
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 6)
                point=(pt[0] + w/2, pt[1] + h/2) #Centre of square approximated as inner corner of GCP
                if(len(pt_list)!=0):
                    list_1 = [x[0] for x in pt_list] #List of all abscissa of found coordinates
                    for comp in list_1:
                        if (abs(comp-pt[0])>delta): #To make sure that same GCP is not counted more than once
                            check+=1 
                            pt_list.append(point)
                else:
                    pt_list.append(point)
            print('%d Point(s) found for %d rotation'%(check,angle))
            for point in pt_list:
                cv2.circle(img_rgb, (int(point[0]), int(point[1])) , 3, (0,255,0), -1)                
                main_list.append(point)
            cv2.imwrite('result_%d_%s.png' %(angle, name), img_rgb) #View results!
            print(pt_list)
    if (check!=0):
        
        img_op_list = [name, main_list]
        final_list.append(img_op_list)
    print('......')
    
    print('*****************')
    
#Writing to 'output.csv' file:
with open('output.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['FileName', 'GCPLocation'])
    for m in final_list:
        filewriter.writerow(m)
        