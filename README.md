# rectpack [![Build Status](https://travis-ci.org/secnot/rectpack.svg?branch=master)](https://travis-ci.org/secnot/rectpack)

Improvement of RectPack with preset items - Loc Nguyen

Rectpack is a collection of heuristic algorithms for solving the 2D knapsack problem,
also known as the bin packing problem. In essence packing a set of rectangles into the 
smallest number of bins.

![alt tag](docs/maxrects.png)


## Installation

Download the package or clone the repository, and then install with:

```bash
python setup.py install
```

or use pypi:

```bash
pip install rectpack
```

## Basic Usage
 
# -*- coding: utf-8 -*-
"""
Test 3D Bin Packing
Author: Loc Nguyen
"""
from rectpack.packer import SolPalletization
from rectpack import *

import random 
import time
import random 
  

import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.patches import Rectangle
from PIL import Image
  
preset_cuboids =[[0,0,0,50,50,60],[50,0,0,50,50,150],[200,200,0,50,50,300]]
pack_cuiboid=[0,0,0,40,50,10]
bin_size = (300,300,450) 

#generate grid
grid_size_w=28
grid_size_h=28

step_w=bin_size[0]/grid_size_w
step_h=bin_size[1]/grid_size_h

for i in range(grid_size_w):
    for j in range(grid_size_h):
        if random.uniform(0,1)>0.5:
            preset_cuboids.append([step_w*i,step_h*j,0,step_w,step_h,random.uniform(bin_size[2]/5, bin_size[2]*5/6) ])

pack3D=SolPalletization(_bin_size=bin_size)
print("Bin Size (W,H,D)=",pack3D.bin_size)
#print("free rect number=",len(pack3D.packer2D._max_rects))
start= time.time()
success,pack_pose=pack3D.pack(preset_cuboids,pack_cuiboid,box_pose=np.identity(4),pick_pose=np.identity(4), level_num=20,display2D=True)
  
end = time.time()
print("Pack time=", end - start)
 
#DISPLAY by ROS scene 
if success:
    print("SUCCESS! pack_pose=\n",pack_pose)
    file1 = open("D:\\packing.scene","w")  
      
    # \n is placed to indicate EOL (End of Line) 
    file1.write("Scene Objects for ROS \n") 
    
    file1.writelines("BIN\n\n")  
    file1.writelines("1\nbox\n")    
    file1.writelines(str(bin_size[0])+" "+str(bin_size[1])+" "+str(bin_size[2])+"\n")
    file1.writelines(str(bin_size[0]/2)+" "+str(bin_size[1]/2)+" "+str(bin_size[2]/2)+"\n")
    file1.writelines("0 0 0 1"+"\n")
    file1.writelines("0 0 0 0"+"\n")
    
    file1.writelines("PACKED_CUIBOID\n\n")  
    file1.writelines("1\nbox\n")    
    file1.writelines(str(pack3D.result[3])+" "+str(pack3D.result[4])+" "+str(pack3D.result[5])+"\n")
    file1.writelines(str(pack3D.result[0]+pack3D.result[3]/2)+" "+str(pack3D.result[1]+pack3D.result[4]/2)+" "+str(pack3D.result[2]+pack3D.result[5]/2)+"\n")
    file1.writelines("0 0 0 1"+"\n")
    file1.writelines("0 0 0 0"+"\n")
        
    
    for i,cuboid in enumerate(preset_cuboids):
        file1.writelines("cuboid "+str(i)+"\n\n")  
        file1.writelines("1\nbox\n")    
        file1.writelines(str(cuboid[3])+" "+str(cuboid[4])+" "+str(cuboid[5])+"\n")
        file1.writelines(str(cuboid[0]+cuboid[3]/2)+" "+str(cuboid[1]+cuboid[4]/2)+" "+str(cuboid[2]+cuboid[5]/2)+"\n")
        file1.writelines("0 0 0 1"+"\n")
        file1.writelines("0 0 0 0"+"\n")
    file1.close() #to change file access modes 

#===========================================
## References

[1] Jukka Jylang - A Thousand Ways to Pack the Bin - A Practical Approach to Two-Dimensional
Rectangle Bin Packing (2010)

[2] Huang, E. Korf - Optimal Rectangle Packing: An Absolute Placement Approach (2013)
