from .maxrects import MaxRectsBssf

import operator
import itertools
import collections

import time
import decimal
from operator import itemgetter


import random 
import time

import numpy as np
from numpy.linalg import inv
from scipy.spatial.transform import Rotation as RotMat

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

# Float to Decimal helper
def float2dec(ft, decimal_digits):
    """
    Convert float (or int) to Decimal (rounding up) with the
    requested number of decimal digits.

    Arguments:
        ft (float, int): Number to convert
        decimal (int): Number of digits after decimal point

    Return:
        Decimal: Number converted to decima
    """
    with decimal.localcontext() as ctx:
        ctx.rounding = decimal.ROUND_UP
        places = decimal.Decimal(10)**(-decimal_digits)
        return decimal.Decimal.from_float(float(ft)).quantize(places)


# Sorting algos for rectangle lists
SORT_AREA  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: r[0]*r[1]) # Sort by area

SORT_PERI  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: r[0]+r[1]) # Sort by perimeter

SORT_DIFF  = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: abs(r[0]-r[1])) # Sort by Diff

SORT_SSIDE = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: (min(r[0], r[1]), max(r[0], r[1]))) # Sort by short side

SORT_LSIDE = lambda rectlist: sorted(rectlist, reverse=True, 
        key=lambda r: (max(r[0], r[1]), min(r[0], r[1]))) # Sort by long side

SORT_RATIO = lambda rectlist: sorted(rectlist, reverse=True,
        key=lambda r: r[0]/r[1]) # Sort by side ratio

SORT_NONE = lambda rectlist: list(rectlist) # Unsorted



class BinFactory(object):

    def __init__(self, width, height, count, pack_algo, *args, **kwargs):
        self._width = width
        self._height = height
        self._count = count
        
        self._pack_algo = pack_algo
        self._algo_kwargs = kwargs
        self._algo_args = args
        self._ref_bin = None # Reference bin used to calculate fitness
        
        self._bid = kwargs.get("bid", None)

    def _create_bin(self):
        return self._pack_algo(self._width, self._height, *self._algo_args, **self._algo_kwargs)

    def is_empty(self):
        return self._count<1

    def fitness(self, width, height):
        if not self._ref_bin:
            self._ref_bin = self._create_bin()

        return self._ref_bin.fitness(width, height)

    def fits_inside(self, width, height):
        # Determine if rectangle widthxheight will fit into empty bin
        if not self._ref_bin:
            self._ref_bin = self._create_bin()

        return self._ref_bin._fits_surface(width, height)

    def new_bin(self):
        if self._count > 0:
            self._count -= 1
            return self._create_bin()
        else:
            return None

    def __eq__(self, other):
        return self._width*self._height == other._width*other._height

    def __lt__(self, other):
        return self._width*self._height < other._width*other._height

    def __str__(self):
        return "Bin: {} {} {}".format(self._width, self._height, self._count)



class PackerBNFMixin(object):
    """
    BNF (Bin Next Fit): Only one open bin at a time.  If the rectangle
    doesn't fit, close the current bin and go to the next.
    """

    def add_rect(self, width, height, rid=None):
        while True:
            # if there are no open bins, try to open a new one
            if len(self._open_bins)==0:
                # can we find an unopened bin that will hold this rect?
                new_bin = self._new_open_bin(width, height, rid=rid)
                if new_bin is None:
                    return None

            # we have at least one open bin, so check if it can hold this rect
            rect = self._open_bins[0].add_rect(width, height, rid=rid)
            if rect is not None:
                return rect

            # since the rect doesn't fit, close this bin and try again
            closed_bin = self._open_bins.popleft()
            self._closed_bins.append(closed_bin)


class PackerBFFMixin(object):
    """
    BFF (Bin First Fit): Pack rectangle in first bin it fits
    """
 
    def add_rect(self, width, height, rid=None):
        # see if this rect will fit in any of the open bins
        for b in self._open_bins:
            rect = b.add_rect(width, height, rid=rid)
            if rect is not None:
                return rect

        while True:
            # can we find an unopened bin that will hold this rect?
            new_bin = self._new_open_bin(width, height, rid=rid)
            if new_bin is None:
                return None

            # _new_open_bin may return a bin that's too small,
            # so we have to double-check
            rect = new_bin.add_rect(width, height, rid=rid)
            if rect is not None:
                return rect


class PackerBBFMixin(object):
    """
    BBF (Bin Best Fit): Pack rectangle in bin that gives best fitness
    """

    # only create this getter once
    first_item = operator.itemgetter(0)

    def add_rect(self, width, height, rid=None):
 
        # Try packing into open bins
        fit = ((b.fitness(width, height),  b) for b in self._open_bins)
        fit = (b for b in fit if b[0] is not None)
        try:
            _, best_bin = min(fit, key=self.first_item)
            
            return best_bin.add_rect(width, height, rid)
            #return True
        except ValueError:
            pass    

        # Try packing into one of the empty bins
        while True:
            # can we find an unopened bin that will hold this rect?
            new_bin = self._new_open_bin(width, height, rid=rid)
            if new_bin is None:
                return False

            # _new_open_bin may return a bin that's too small,
            # so we have to double-check
            return new_bin.add_rect(width, height, rid)
            #if self.result2D:
            #    return True

    def add_preset_rect(self, x, y , width, height, rid=None):
 
        # Try packing into open bins
        fit = ((b.fitness(width, height),  b) for b in self._open_bins)
        fit = (b for b in fit if b[0] is not None)
        try:
            _, best_bin = min(fit, key=self.first_item)
            best_bin.add_preset_rect(x,y,width, height, rid)
            return True
        except ValueError:
            pass    

        # Try packing into one of the empty bins
        while True:
            # can we find an unopened bin that will hold this rect?
            new_bin = self._new_open_bin(width, height, rid=rid)
            if new_bin is None:
                return False

            # _new_open_bin may return a bin that's too small,
            # so we have to double-check   
            if new_bin.add_preset_rect(x,y,width, height, rid):
                return True

class PackerOnline(object):
    """
    Rectangles are packed as soon are they are added
    """

    def __init__(self, pack_algo=MaxRectsBssf, rotation=True):
        """
        Arguments:
            pack_algo (PackingAlgorithm): What packing algo to use
            rotation (bool): Enable/Disable rectangle rotation
        """
        self._rotation = rotation
        self._pack_algo = pack_algo
        self.reset()

    def __iter__(self):
        return itertools.chain(self._closed_bins, self._open_bins)

    def __len__(self):
        return len(self._closed_bins)+len(self._open_bins)
    
    def __getitem__(self, key):
        """
        Return bin in selected position. (excluding empty bins)
        """
        if not isinstance(key, int):
            raise TypeError("Indices must be integers")

        size = len(self)  # avoid recalulations

        if key < 0:
            key += size

        if not 0 <= key < size:
            raise IndexError("Index out of range")
        
        if key < len(self._closed_bins):
            return self._closed_bins[key]
        else:
            return self._open_bins[key-len(self._closed_bins)]

    def _new_open_bin(self, width=None, height=None, rid=None):
        """
        Extract the next empty bin and append it to open bins

        Returns:
            PackingAlgorithm: Initialized empty packing bin.
            None: No bin big enough for the rectangle was found
        """
        factories_to_delete = set() #
        new_bin = None

        for key, binfac in self._empty_bins.items():

            # Only return the new bin if the rect fits.
            # (If width or height is None, caller doesn't know the size.)
            if not binfac.fits_inside(width, height):
                continue
           
            # Create bin and add to open_bins
            new_bin = binfac.new_bin()
            if new_bin is None:
                continue
            self._open_bins.append(new_bin)

            # If the factory was depleted mark for deletion
            if binfac.is_empty():
                factories_to_delete.add(key)
       
            break

        # Delete marked factories
        for f in factories_to_delete:
            del self._empty_bins[f]

        return new_bin 

    def add_bin(self, width, height, count=1, **kwargs):
        # accept the same parameters as PackingAlgorithm objects
        kwargs['rot'] = self._rotation
        bin_factory = BinFactory(width, height, count, self._pack_algo, **kwargs)
        self._empty_bins[next(self._bin_count)] = bin_factory

    def rect_list(self):
        rectangles = []
        bin_count = 0

        for abin in self:
            for rect in abin:
                rectangles.append((bin_count, rect.x, rect.y, rect.width, rect.height, rect.rid))
            bin_count += 1

        return rectangles

    def bin_list(self):
        """
        Return a list of the dimmensions of the bins in use, that is closed
        or open containing at least one rectangle
        """
        return [(b.width, b.height) for b in self]

    def validate_packing(self):
        for b in self:
            b.validate_packing()

    def reset(self): 
        # Bins fully packed and closed.
        self._closed_bins = collections.deque()

        # Bins ready to pack rectangles
        self._open_bins = collections.deque()

        # User provided bins not in current use
        self._empty_bins = collections.OrderedDict() # O(1) deletion of arbitrary elem
        self._bin_count = itertools.count()


class Packer(PackerOnline):
    """
    Rectangles aren't packed untils pack() is called
    """

    def __init__(self, pack_algo=MaxRectsBssf, sort_algo=SORT_NONE, 
            rotation=True):
        """
        """
        super(Packer, self).__init__(pack_algo=pack_algo, rotation=rotation)
        
        self._sort_algo = sort_algo

        # User provided bins and Rectangles
        self._avail_bins = collections.deque()
        self._avail_rect = collections.deque()

        # Aux vars used during packing
        self._sorted_rect = []

    def add_bin(self, width, height, count=1, **kwargs):
        self._avail_bins.append((width, height, count, kwargs))

    def add_rect(self, width, height, rid=None):
        self._avail_rect.append((width, height, rid))

    def _is_everything_ready(self):
        return self._avail_rect and self._avail_bins

    def pack(self):

        self.reset()

        if not self._is_everything_ready():
            # maybe we should throw an error here?
            return

        # Add available bins to packer
        for b in self._avail_bins:
            width, height, count, extra_kwargs = b
            super(Packer, self).add_bin(width, height, count, **extra_kwargs)

        # If enabled sort rectangles
        self._sorted_rect = self._sort_algo(self._avail_rect)

        # Start packing
        for r in self._sorted_rect:
            super(Packer, self).add_rect(*r)


 
class PackerBNF(Packer, PackerBNFMixin):
    """
    BNF (Bin Next Fit): Only one open bin, if rectangle doesn't fit
    go to next bin and close current one.
    """
    pass

class PackerBFF(Packer, PackerBFFMixin):
    """
    BFF (Bin First Fit): Pack rectangle in first bin it fits
    """
    pass
    
class PackerBBF(Packer, PackerBBFMixin):
    """
    BBF (Bin Best Fit): Pack rectangle in bin that gives best fitness
    """
    pass 

class PackerOnlineBNF(PackerOnline, PackerBNFMixin):
    """
    BNF Bin Next Fit Online variant
    """
    pass 

class PackerOnlineBFF(PackerOnline, PackerBFFMixin):
    """ 
    BFF Bin First Fit Online variant
    """
    pass

class PackerOnlineBBF(PackerOnline, PackerBBFMixin):
    """ 
    BBF Bin Best Fit Online variant
    """
    pass


class PackerGlobal(Packer, PackerBNFMixin):
    """ 
    GLOBAL: For each bin pack the rectangle with the best fitness.
    """
    first_item = operator.itemgetter(0)
    
    def __init__(self, pack_algo=MaxRectsBssf, rotation=True):
        """
        """
        super(PackerGlobal, self).__init__(pack_algo=pack_algo,
            sort_algo=SORT_NONE, rotation=rotation)

    def _find_best_fit(self, pbin):
        """
        Return best fitness rectangle from rectangles packing _sorted_rect list

        Arguments:
            pbin (PackingAlgorithm): Packing bin

        Returns:
            key of the rectangle with best fitness
        """
        fit = ((pbin.fitness(r[0], r[1]), k) for k, r in self._sorted_rect.items())
        fit = (f for f in fit if f[0] is not None)
        try:
            _, rect = min(fit, key=self.first_item)
            return rect
        except ValueError:
            return None


    def _new_open_bin(self, remaining_rect):
        """
        Extract the next bin where at least one of the rectangles in
        rem

        Arguments:
            remaining_rect (dict): rectangles not placed yet

        Returns:
            PackingAlgorithm: Initialized empty packing bin.
            None: No bin big enough for the rectangle was found
        """
        factories_to_delete = set() #
        new_bin = None

        for key, binfac in self._empty_bins.items():

            # Only return the new bin if at least one of the remaining 
            # rectangles fit inside.
            a_rectangle_fits = False
            for _, rect in remaining_rect.items():
                if binfac.fits_inside(rect[0], rect[1]):
                    a_rectangle_fits = True
                    break

            if not a_rectangle_fits:
                factories_to_delete.add(key)
                continue
           
            # Create bin and add to open_bins
            new_bin = binfac.new_bin()
            if new_bin is None:
                continue
            self._open_bins.append(new_bin)

            # If the factory was depleted mark for deletion
            if binfac.is_empty():
                factories_to_delete.add(key)
       
            break

        # Delete marked factories
        for f in factories_to_delete:
            del self._empty_bins[f]

        return new_bin 

    def pack(self):
       
        self.reset()

        if not self._is_everything_ready():
            return
        
        # Add available bins to packer
        for b in self._avail_bins:
            width, height, count, extra_kwargs = b
            super(Packer, self).add_bin(width, height, count, **extra_kwargs)
    
        # Store rectangles into dict for fast deletion
        self._sorted_rect = collections.OrderedDict(
                enumerate(self._sort_algo(self._avail_rect)))
        
        # For each bin pack the rectangles with lowest fitness until it is filled or
        # the rectangles exhausted, then open the next bin where at least one rectangle 
        # will fit and repeat the process until there aren't more rectangles or bins 
        # available.
        while len(self._sorted_rect) > 0:

            # Find one bin where at least one of the remaining rectangles fit
            pbin = self._new_open_bin(self._sorted_rect)
            if pbin is None:
                break

            # Pack as many rectangles as possible into the open bin
            while True:
              
                # Find 'fittest' rectangle
                best_rect_key = self._find_best_fit(pbin)
                if best_rect_key is None:
                    closed_bin = self._open_bins.popleft()
                    self._closed_bins.append(closed_bin)
                    break # None of the remaining rectangles can be packed in this bin

                best_rect = self._sorted_rect[best_rect_key]
                del self._sorted_rect[best_rect_key]

                PackerBNFMixin.add_rect(self, *best_rect)





# Packer factory
class Enum(tuple): 
    __getattr__ = tuple.index

PackingMode = Enum(["Online", "Offline"])
PackingBin = Enum(["BNF", "BFF", "BBF", "Global"])


def newPacker(mode=PackingMode.Offline, 
         bin_algo=PackingBin.BBF, 
        pack_algo=MaxRectsBssf,
        sort_algo=SORT_AREA, 
        rotation=True):
    """
    Packer factory helper function

    Arguments:
        mode (PackingMode): Packing mode
            Online: Rectangles are packed as soon are they are added
            Offline: Rectangles aren't packed untils pack() is called
        bin_algo (PackingBin): Bin selection heuristic
        pack_algo (PackingAlgorithm): Algorithm used
        rotation (boolean): Enable or disable rectangle rotation. 

    Returns:
        Packer: Initialized packer instance.
    """
    packer_class = None

    # Online Mode
    if mode == PackingMode.Online:
        sort_algo=None
        if bin_algo == PackingBin.BNF:
            packer_class = PackerOnlineBNF
        elif bin_algo == PackingBin.BFF:
            packer_class = PackerOnlineBFF
        elif bin_algo == PackingBin.BBF:
            packer_class = PackerOnlineBBF
        else:
            raise AttributeError("Unsupported bin selection heuristic")

    # Offline Mode
    elif mode == PackingMode.Offline:
        if bin_algo == PackingBin.BNF:
            packer_class = PackerBNF
        elif bin_algo == PackingBin.BFF:
            packer_class = PackerBFF
        elif bin_algo == PackingBin.BBF:
            packer_class = PackerBBF
        elif bin_algo == PackingBin.Global:
            packer_class = PackerGlobal
            sort_algo=None
        else:
            raise AttributeError("Unsupported bin selection heuristic")

    else:
        raise AttributeError("Unknown packing mode.")

    if sort_algo:
        return packer_class(pack_algo=pack_algo, sort_algo=sort_algo, 
            rotation=rotation)
    else:
        return packer_class(pack_algo=pack_algo, rotation=rotation)


class SolPalletization:
    """
    SolPalletization for 3D packing with point cloud
    
    Note: Rotation is Euler Angle following Fanuc Robot definition: rx,ry,rz
    cuboid(x,y,z,w,h,d)
    Arguments:
        Bin Size: (Width,Height,Depth)
        Preset Cuboids: [(x,y,z,w,h,d)]
        Pack N Cuboids:[(w,h,d)]        
        Robot N Picking Pose: [(x,y,z,rx,ry,rz)]

    Returns:
        Pack N Cuboids Pose:[(x,y,z,rx,ry,rz)]
    """
    def __init__(self, _bin_size=(600,380,450),_bin_pose=np.identity(4), rot=True):
        self.bin_size=_bin_size
        self.bin_width=_bin_size[0]
        self.bin_height=_bin_size[1]
        self.bin_depth=_bin_size[2]
        self.bin_pose=_bin_pose
        self.result=None
    def get_level_list(self,  preset_cuboid=[],pack_cuboid=[], level_num=20):
        search_list=[]
        total_area = self.bin_width * self.bin_height
        pack_cuboid_area=pack_cuboid[3]*pack_cuboid[4]
        
        #get list of (depth, area) for cuboid
        level_list= [ [x[2]+x[5],x[3]*x[4]] for x in preset_cuboid if (x[2]+x[5])>0 and (x[2]+x[5]+pack_cuboid[5])<self.bin_depth] #(z+d,w*h) for (depth,area) of cuboid 
        
        #sort decrease by depth
        level_list.sort(key=itemgetter(0), reverse=True)
        
        # append the bottom of bin with Zero Area
        level_list.append([0,0])
        
        #calculate occupied area at each level
        delete_indices=[]
        for i in range(1,len(level_list)):
            level_list[i][1]+=level_list[i-1][1]  
            if (level_list[i][0]==level_list[i-1][0]):
                delete_indices.append(i-1)
            if (level_list[i][1]+pack_cuboid_area>total_area):
                delete_indices.append( list(range(i,len(level_list)))  )
                break #skip checking other cuboids
              
        #keep level only
        level_list_filter = [v for i,v in enumerate(level_list) if i not in delete_indices] 
        
        #remove level that available not fit
        if len(level_list_filter)>level_num and level_num>0:
            max_level=self.bin_depth#level_list_filter[0][0]
            min_level=0#level_list_filter[len(level_list_filter)-1][0]
            #Loop for level_num
            step=(max_level-min_level)/level_num
            
            start_index=0 
            
            # search all 
            for i in range(-1,level_num):
                group_i=[v[0] for v in level_list_filter if v[0]>min_level+i*step and v[0]<=min_level+(i+1)*step] 
                if (len(group_i)>0):
                    search_list.append(max(group_i))
            return search_list
        else:
            level_list_filter.sort(key=itemgetter(0))
            return  [v[0] for v in level_list_filter]
             
        
    def pack(self, preset_cuboid=[],pack_cuboid=[],box_pose=np.identity(4),pick_pose=np.identity(4),level_num=20, display2D=False): 
        #Get level list
        level_list=self.get_level_list(preset_cuboid,pack_cuboid,level_num)
        print("Number of searching level=",len(level_list))
        print("List of searching level=",level_list)
         
        #Start Packing 
        for i,level in enumerate(level_list):   
            start= time.time() 
            packer = newPacker(mode=PackingMode.Online, 
                               bin_algo=PackingBin.BBF, 
                               pack_algo=MaxRectsBssf,#( self.bin_width,self.bin_height),
                               sort_algo=SORT_AREA, 
                               rotation=True)
            packer.add_bin(self.bin_width,self.bin_height)
            
            
            #Note: packer._pack_alg is a class name 
            #minWH is class attribute
            packer._pack_algo.minWH= min(pack_cuboid[3],pack_cuboid[4])
            
            for cuboid in preset_cuboid:
                if(cuboid[2]+cuboid[5]>level):
                    packer.add_preset_rect(cuboid[0],cuboid[1],cuboid[3],cuboid[4])
                    
            print("packer._pack_algo.minWH=",packer._pack_algo.minWH)
            
            end_preset = time.time() 
            
            #print("pack2d result=",packer._pack_algo.current_pack2D_result)
            if (packer.add_rect(pack_cuboid[3], pack_cuboid[4])):
                print("SUCCESS level=",i,"  depth value=",level)
                current_pack2D_result=packer[0][len(packer[0])-1]
                self.result=[current_pack2D_result.x,current_pack2D_result.y,level,current_pack2D_result.width, current_pack2D_result.height,pack_cuboid[5]]
                
                #pick pose in box pose coordinate
                pick_pose_2_box_pose=(inv(box_pose)).dot(pick_pose)
                 
                pack_pose=np.identity(4)
                #checking rotatation of box
                if abs(current_pack2D_result.width-pack_cuboid[3])<0.00001 and abs(current_pack2D_result.height-pack_cuboid[4])<0.00001:
                    #NOT rotated
                    #cuboid pose in bin coordinate
                    cuboid_2_bin_pose_tran= np.identity(4)
                    cuboid_2_bin_pose_tran[:3, 3] = [current_pack2D_result.x,current_pack2D_result.y,level] 
                 
                    pack_pose=self.bin_pose.dot(cuboid_2_bin_pose_tran.dot(pick_pose_2_box_pose))
                else:
                    print("NOTE: Box is rotated 90 degrees!")
                    cuboid_2_bin_pose_tran= np.identity(4)
                    cuboid_2_bin_pose_tran[:3, 3] = [current_pack2D_result.x+current_pack2D_result.width,current_pack2D_result.y,level] 
                 
                    cuboid_2_bin_pose_rot= np.identity(4)
                    cuboid_2_bin_pose_rot[:3, :3] = RotMat.from_euler('z', 90, degrees=True).as_matrix()
                  
                    pack_pose=self.bin_pose.dot(cuboid_2_bin_pose_tran.dot(cuboid_2_bin_pose_rot.dot(pick_pose_2_box_pose)))
                  
  
                #DRAWING for DEBUG
                if (display2D):
                    plt.figure(figsize=(10,10)) 
                    plt.xlabel('Bin Packing 2D - SolPacker')
                    plt.xlim(0,self.bin_width)
                    plt.ylim(0,self.bin_height)
                    # Get the current reference
                    ax = plt.gca()
                    
                    print("packer[0]=",packer[0])
                    for abin in packer:
                        print("abin.bid=",abin.bid) # Bin id if it has one
                        for count,rect in enumerate(abin): 
                            # Create a Rectangle patch
                            rect2D = Rectangle((rect.x,rect.y),rect.width,rect.height,linewidth=2,edgecolor=(0,0,0),facecolor=(random.uniform(0.2, 1), random.uniform(0.2, 1), random.uniform(0.2, 1)))
                    
                            # Add the patch to the Axes
                            ax.add_patch(rect2D)
                            
                            ax.text(rect.x+rect.width/2,rect.y+rect.height/2, str(count), fontsize=15)
                            #print(rect)
               
                return True,pack_pose
            #print("============",packer._pack_algo.minWH)
        
            print("Retry Fail",i,"Preset Time (s)=", end_preset - start,"Packing 1 cuboid Time (s)=", time.time() -end_preset)
        self.result=None
        print("PACKING FAIL!")    
        return False,None
             


 
   
