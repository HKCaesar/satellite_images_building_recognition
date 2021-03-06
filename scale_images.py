# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:04:13 2016

@author: to
"""

import glob
import cv2
import sys

if len(sys.argv) < 2:
    print "need at least 1 argument as (str) defining the image directory and file extension [png/txt] e.g. './images/*png' ./labels/*txt"
    exit()

#for 1024
#scaling_factor_x = 2.33
#scaling_factor_y = 2.52
#outputdim = 1024

#for 2048
#scaling_factor_x = 4.66
#scaling_factor_y = 5.04
#outputdim = 2048

#for 1280
#scaling_factor_x = 2.92
#scaling_factor_y = 3.15
#outputdim = 1280

original_x = 439.0 #remember some are 238
original_y = 406.0 #remember some are 407s

outputdim = sys.argv[1]
scaling_factor_x = float(outputdim)/original_x
scaling_factor_y = float(outputdim)/original_y


listdirectory = sys.argv[2:]


for directories in listdirectory:
    filenames = glob.glob(directories)


    for f in filenames:
        
        if str(f[-3:]) == 'png':
        
            im = cv2.imread(f)
            
            #h,w = im.shape[:2]
            im = cv2.resize(im,(outputdim,outputdim))
            
            cv2.imwrite(f,im)
            
        elif str(f[-3:]) == 'txt':


            newlabels = []
            lines = open(f,'r').read().split('\n')
            
            lines = lines[:-1]

            if len(lines) == 0:
                label_i = "dontcare 0.0 0 0.0 0.00 0.00 1.00 1.00 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n"
                newlabels.append(label_i)           


            for l in lines:
                _,_,_,_,c1x,c1y,c2x,c2y,_,_,_,_,_,_,_ = l.split()
                
                c1x = float(c1x)
                c1y = float(c1y)
                c2x = float(c2x)
                c2y = float(c2y)


                c1x = max(scaling_factor_x * c1x, 0)
                c1y = max(scaling_factor_y * c1y, 0)
                c2x = min(scaling_factor_x * c2x, outputdim)
                c2y = min(scaling_factor_y * c2y, outputdim)


                if (c1x != c2x and c1y !=c2y ):
                    label_i = 'building 0.0 0 0.0 {:.2f} {:.2f} {:.2f} {:.2f} 0.0 0.0 0.0 0.0 0.0 0.0 0.0\n'.format(abs(c1x),abs(c1y),abs(c2x),abs(c2y))
                    newlabels.append(label_i)


            if newlabels:
                newlabels[-1] = newlabels[-1][:-1]            

            #Write the feature labels into a file [same name required as input image]             
            #if this is the first building, write to a new file, otherwise append
            labelfile = open(f,'w')
     
            #write the label
            labelfile.writelines(newlabels)
            #close the document
            labelfile.close()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
