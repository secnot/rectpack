# -*- coding: utf-8 -*-
"""
Test 2D Bin Packing
Author: 
"""
from rectpack.packer import newPacker
from rectpack import *

import random 
import time


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
 


rectangles = [(100, 30), (40, 60), (30, 30),(70, 70), (100, 50), (30, 30),(55,77),(48,72)]
bins = [(150, 170)]#[(300, 450), (80, 40), (200, 150)]

packer = newPacker(mode=PackingMode.Online, 
         bin_algo=PackingBin.BBF, 
        pack_algo=MaxRectsBssf,
        sort_algo=SORT_AREA, 
        rotation=True)


 
plt.figure(figsize=(10,10)) 
plt.xlabel('Bin Packing 2D - SolPacker')
plt.xlim(0,bins[0][0])
plt.ylim(0,bins[0][1])
# Get the current reference
ax = plt.gca()

print("display finished!")

# Add the bins where the rectangles will be placed
for b in bins:
	packer.add_bin(*b)
    
count=0
# INITIALIZE
r_list=[(89, 36),( 49, 87),(84, 39),(69, 74)]
r_preset=[(0, 0, 36, 89),(36, 0, 87, 49),(36, 49, 39, 84),(75, 49, 74, 69)]

start= time.time()

#Octomap
packer.add_preset_rect(*r_preset[0])
packer.add_preset_rect(*r_preset[1]) #packer.py line 184
packer.add_preset_rect(*r_preset[2])
packer.add_preset_rect(*r_preset[3])

#Pack last item
rect=packer.add_rect(24, 36)
print("---",rect)
rect=packer.add_rect(240, 260)
print("---",rect)
rect=packer.add_rect(24, 46)
print("---",rect)
rect=packer.add_rect(24, 86)
print("---",rect)
#Display  
count=0
for abin in packer:
    print(abin.bid) # Bin id if it has one
    for rect in abin: 
        # Create a Rectangle patch
        rect2D = Rectangle((rect.x,rect.y),rect.width,rect.height,linewidth=2,edgecolor=(0,0,0),facecolor=(random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)))

        # Add the patch to the Axes
        ax.add_patch(rect2D)
        count+=1
        ax.text(rect.x+rect.width/2,rect.y+rect.height/2, str(count), fontsize=15)
        print(rect)
  
end = time.time()
print("Pack time=", end - start)
