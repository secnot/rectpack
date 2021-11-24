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

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
 


preset_cuboids =[]# [[0,0,0,50,50,60],[50,0,0,50,50,150],[200,200,0,50,50,300]]
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
success,pack_pose,pack_cuboid3D=pack3D.pack(preset_cuboids,pack_cuiboid,box_pose=np.identity(4),pick_pose=np.identity(4), level_num=20,display2D=True)
  
end = time.time()
print("Pack time=", end - start)
 
#DISPLAY by ROS scene 
if success:
    print("SUCCESS! \npack_pose=\n",pack_pose)
    print("pack_cuboid3D=\n",pack_cuboid3D)
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
    file1.writelines(str(pack_cuboid3D[3])+" "+str(pack_cuboid3D[4])+" "+str(pack_cuboid3D[5])+"\n")
    file1.writelines(str(pack_cuboid3D[0]+pack_cuboid3D[3]/2)+" "+str(pack_cuboid3D[1]+pack_cuboid3D[4]/2)+" "+str(pack_cuboid3D[2]+pack_cuboid3D[5]/2)+"\n")
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
'''
# prepare some coordinates
x, y, z = np.indices((28, 28,28))

# draw cuboids in the top left and bottom right corners, and a link between them
voxels = (x < 0) & (y < 0) & (z <0)



for i,cuboid in enumerate(preset_cuboids):
    #if i<4:
    c2 = (x >= cuboid[0]/step_w) &(x <(cuboid[0]+cuboid[3])/step_w)& (y >= cuboid[1]/step_h) &(y <(cuboid[1]+cuboid[4])/step_h)& (z >= cuboid[2]*8/bin_size[2]) &(z <(cuboid[2]+cuboid[5])*8/bin_size[2])
    voxels = voxels | c2  
 
# and plot everything
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels,  edgecolor='k')#colors  facecolors='y',

plt.show()
''' 
#===========================================
 